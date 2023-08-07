import sys, os, math
from PIL import Image
from functools import reduce
from collections import namedtuple
from xml.etree.ElementTree import Element, ElementTree, SubElement, indent

BBox = namedtuple("Bbox", 'x y w h')
OutImage = namedtuple("OutImage", "name im")
FullBox = namedtuple("FullBox", "image, outidx, bbox, name")
AtlasData = namedtuple("Atlas", "src_images, mips, bboxes")

def Clamp(lower, upper, val):
    return max(lower, min(upper, val))

def NextMultipleOf(n: int, target: int) -> int:
    mod = n % target
    if mod == 0:
        return n
    return n + (target - mod)

def GetDim(images: list[Image.Image], alignto: int, maxtexturesize: int=2048, scale_factor: int=1) -> int:
    area = reduce(lambda tally, next : tally + next.size[0] * next.size[1] * scale_factor * scale_factor, images, 0)
    maxdim = NextMultipleOf(max([max(img.size[0], img.size[1]) * scale_factor for img in images]), alignto)
    dim = min(maxtexturesize, max( math.pow(2, math.ceil( math.log(math.sqrt(area * 1.25), 2)) ), math.pow(2, math.ceil(math.log(maxdim, 2))) ) )
    # print("GETDIM:", area, maxdim, dim)

    return dim / scale_factor

def BBoxIntersects(bb1: BBox, bb2: BBox) -> bool:
    return not (bb2.x >= bb1.x + bb1.w or bb2.x + bb2.w <= bb1.x or bb2.y + bb2.h <= bb1.y or bb2.y >= bb1.y + bb1.h)

def TryInsertImage(w, h, fblist: list, atlassize) -> None|BBox:
    align = 4
    x = 0
    y = 0

    while y + h < atlassize:
        min_y = None
        ytestbb = BBox(0, y, atlassize, h)
        temp_list = [fb for fb in fblist if BBoxIntersects(fb.bbox, ytestbb)]
        while x + w <= atlassize:
            testbb = BBox(x, y, w, h)
            intersects = False
            for fb in temp_list:
                if BBoxIntersects(fb.bbox, testbb):
                    x = NextMultipleOf(fb.bbox.x + fb.bbox.w, align)
                    if not min_y:
                        min_y = fb.bbox.h + fb.bbox.y
                    else:
                        min_y = min(min_y, fb.bbox.h + fb.bbox.y)
                    intersects = True
                    break
            if not intersects:
                return BBox(x, y, w, h)
        if min_y:
            y = max(NextMultipleOf(min_y, align), y + align)
        else:
            y += align
        x = 0
        # mylist = [fb for fb in mylist if BBoxIntersects(fb.bbox, BBox(0, y, atlassize, atlassize-y))]

    return None

# images: list of subimages
# outname: prefix name for output image

# returns dest, atlases
# dest = {image_name: [ (origbbox, destbbox, destatlasidx) ]
# atlases = {index : (name, image) ]
def Atlas(images, out_name, max_size=2048, scale_factor=1, force_square=False) -> list[AtlasData]:
    blocksize = 4
    dim = GetDim(images, blocksize, max_size, scale_factor)
    size = (dim, dim)

    # sort by image area
    images = sorted(images, key = lambda image : image.size[0] * image.size[1], reverse=True)

    # Full boxes are areas where we have placed images in the atlas
    fullboxes = [(size, [])]

    # Do the actual atlasing by sticking the largest images we can have into the smallest valid free boxes
    source_idx = 0

    def LocalAtlas(image: Image.Image, source_idx: int) -> int:
        nonlocal dim
        if image.size[0] > size[0] or image.size[1] > size[1]:
            sys.stderr.write("Error: image " + image.name + " is larger than the atlas size!\n")
            sys.exit(2)

        inserted = False
        for idx, fb in enumerate(fullboxes):
            fblist = fb[1]
            insertbbox = TryInsertImage(image.size[0], image.size[1], fblist, dim)
            if insertbbox:
                inserted = True
                fblist.append(FullBox(image, idx, insertbbox, image.name))
                break

        if not inserted:
            dim = newsize = GetDim(images[source_idx:], blocksize, max_size, scale_factor)
            fullboxes.append(((newsize, newsize), [FullBox(image, len(fullboxes), BBox(0, 0, image.size[0], image.size[1]), image.name)]))

        return source_idx + 1


    for image in images:
        source_idx = LocalAtlas(image, source_idx)

    # now that we've figured out where everything goes, make the output images and blit the source images to the appropriate locations

    atlases = []
    for idx, fb in enumerate(fullboxes):
        w = int(fb[0][0])
        h = int(fb[0][1])

        if not force_square:
            # figure out if we can reduce our w or h:
            sz = fb[0][0]
            fblist = fb[1]
            maxy = 0
            maxx = 0
            for b in fblist:
                fbmaxy = b.bbox.y + b.bbox.h
                fbmaxx = b.bbox.x + b.bbox.w
                maxy = max(maxy, fbmaxy)
                maxx = max(maxx, fbmaxx)
            if maxy <= h // 2:
                h = int(h // 2)
            if maxx <= w // 2:
                w = int(w // 2)

        # now generate mips and such...
        mips = []

        divisor = 1

        contained_images = {}

        # Generate mips and their positions
        # while w >= 1 or h >= 1:
        outim = OutImage("{0}-{1}".format(out_name, idx), Image.new("RGBA", (w, h)))

        for b in fb[1]:
            # b_w, b_h = b.image.size
            # b_w, b_h = b_w // divisor, b_h // divisor
            # if b_w > 0 and b_h > 0:
            # resized_b = b.image.resize((b_w, b_h), Image.LANCZOS)
            outim[1].paste(b.image, (b.bbox.x, b.bbox.y))
            if b.image.name not in contained_images:
                contained_images[b.image.name] = b.image

            # mips.append(outim)

            # divisor = divisor << 1

            # if w == 1 and h == 1:
            #     break

            # w = max(1, w >> 1)
            # h = max(1, h >> 1)

        atlases.append(AtlasData(contained_images, outim, {b.name : b.bbox for b in fb[1]}))

    return atlases

def GenerateXMLTree(texture_filename, texture_size, bboxes, offset_amount=None, element_prefix="") ->ElementTree:
    root = Element("Atlas")
    tex_elem = SubElement(root, "Texture")
    tex_elem.set("filename", os.path.basename(texture_filename))

    elem_root = SubElement(root, "Elements")

    # pull in the UVs by a half pixel from the edge to avoid some sampling issues, unless told otherwise
    offset_amount_x = offset_amount if offset_amount != None else 0.5
    offset_amount_y = offset_amount if offset_amount != None else 0.5

    border_uv_offset = (offset_amount_x / texture_size[0], offset_amount_y / texture_size[1])

    for name, bbox in bboxes.items():
        elem = SubElement(elem_root, "Element")
        elem.set("name", element_prefix + name)

        u1 = Clamp(0.0, 1.0, bbox.x / float(texture_size[0]) + border_uv_offset[0])
        v1 = Clamp(0.0, 1.0, 1.0 - (bbox.y + bbox.h) / float(texture_size[1]) + border_uv_offset[1])

        u2 = Clamp(0.0, 1.0, (bbox.x + bbox.w) / float(texture_size[0]) - border_uv_offset[0])
        v2 = Clamp(0.0, 1.0, 1.0 - bbox.y / float(texture_size[1]) - border_uv_offset[1])

        elem.set("u1", str(u1))
        elem.set("v1", str(v1))

        elem.set("u2", str(u2))
        elem.set("v2", str(v2))

    tree = ElementTree(root)
    indent(tree, space="    ")

    return tree
