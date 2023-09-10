from PIL.Image import Image
from .anim_util import round_up
from collections import namedtuple

BBox = namedtuple("Bbox", "x y w h")
Regions = namedtuple("Regions", "alpha, opaque")

class BlockType:
    OPAQUE = 1
    EMPTY = 2
    ALPHA = 3
    UNKNOWN = 4

def BlockName(block):
    if block == BlockType.OPAQUE:
        return "Opaque"
    elif block == BlockType.EMPTY:
        return "Empty"
    elif block == BlockType.ALPHA:
        return "Alpha"
    return "Unknown"

def Analyze(image: Image, bbox: BBox):
    numalpha = 0
    numblank = 0
    numopaque = 0

    pixels = image.load()
    if image.mode!="RGBA":
        image=image.convert("RGBA")
    for y in range(bbox.y, bbox.y + bbox.h):
        for x in range(bbox.x, bbox.x + bbox.w):
            p = pixels[x, y]
            if type(p) is not int:
                p = p[-1] # A for RGBA, B for RGB, ? for index, K for CMYK
            if p == 0:
                numblank += 1
            elif p == 255:
                numopaque += 1
            else:
                numalpha += 1

    if numalpha == 0 and numblank == 0:
        return BlockType.OPAQUE
    elif numalpha == 0 and numopaque == 0:
        return BlockType.EMPTY
    else:
        return BlockType.ALPHA


class QuadTreeNode:
    def __init__(self, image: Image, bbox = None, depth = 0, blocksize = 32):
        if bbox == None:
            bbox = BBox(0, 0, image.width, image.height)
        self.blocksize = blocksize
        self.depth = depth
        self.bbox = bbox
        self.im = image
        self.children = None
        self.type = BlockType.UNKNOWN

        if bbox.w > self.blocksize and bbox.h > self.blocksize:
            # if we are far enough up the tree to consider splitting:

            # generate the child bboxes
            childboxes = [
                BBox(bbox.x, bbox.y, bbox.w // 2, bbox.h // 2),
                BBox(bbox.x + bbox.w // 2, bbox.y, bbox.w - bbox.w // 2, bbox.h // 2),
                BBox(bbox.x, bbox.y + bbox.h // 2, bbox.w // 2, bbox.h - bbox.h // 2),
                BBox(bbox.x + bbox.w // 2, bbox.y + bbox.h // 2, bbox.w - bbox.w // 2, bbox.h - bbox.h // 2)
            ]

            # figure out the child image types
            childtypes = [
                Analyze(image, childboxes[0]),
                Analyze(image, childboxes[1]),
                Analyze(image, childboxes[2]),
                Analyze(image, childboxes[3])
            ]

            same_type = childtypes[0] == childtypes[1] == childtypes[2] == childtypes[3]
            last_div = (bbox.w // 2) < self.blocksize or (bbox.h // 2 )< self.blocksize

            if same_type and (childtypes[0] != BlockType.ALPHA or last_div):
                # stop iterating, we've hit the bottom
                self.type = childtypes[0]
            else:
                # otherwise, split up the children
                self.children = (
                    QuadTreeNode(image, childboxes[0], depth + 1, self.blocksize),
                    QuadTreeNode(image, childboxes[1], depth + 1, self.blocksize),
                    QuadTreeNode(image, childboxes[2], depth + 1, self.blocksize),
                    QuadTreeNode(image, childboxes[3], depth + 1, self.blocksize)
                )

            if self.children and len(self.children) == 4 and self.children[0].type == self.children[1].type == self.children[2].type == self.children[3].type == BlockType.ALPHA:
                self.children = None
                self.type = BlockType.ALPHA
        else:
            self.type = Analyze(image, bbox)

    def __repr__(self):
        if self.children == None:
            return "\t" * self.depth + BlockName(self.type) + " " +  str(self.bbox)
        else:
            l = [str(x) for x in self.children]
            return "\t" * self.depth + "->\n" + "\n".join(l)

    def printme(self):
        print("\t" * self.depth + BlockName(self.type) + " " +  str(self.bbox))
        if self.children:
            for child in self.children:
                child.printme()

    def GetBBox(self, fn):
        if self.children != None:
            ret = []
            for child in self.children:
                op = child.GetBBox(fn)
                if op != None:
                    ret.extend(op)
            if len(ret) > 0:
                return ret
        elif fn(self):
            return [self.bbox]
        return []

def optlist(orig):
    newlist = []
    for o in orig:
        added = False
        for n in newlist:
            if n.w == o.w and n.x == o.x and (n.y + n.h == o.y or o.y + o.h == n.y):
                newlist.remove(n)
                newlist.append(BBox(n.x, min(o.y, n.y), n.w, o.h+n.h))
                added = True
                break
            if n.h == o.h and n.y == o.y and (n.x + n.w == o.x or o.x + o.w == n.x):
                newlist.remove(n)
                newlist.append(BBox(min(o.x, n.x), n.y, n.w + o.w, o.h))
                added = True
                break

        if not added:
            newlist.append(o)
    return newlist

# fix up the list so that adjacent similarly sized images are joined
def doopt(orig):
    while True:
        newlist = optlist(orig)
        if len(newlist) == len(orig):
            return newlist
        orig = newlist

def CorpImageByRegion(image: Image, regions: Regions):
    really_size = image.size
    left, right, upper, lower = image.width, 0, image.height, 0

    for region in regions.alpha:
        left = round_up(min(left, min(region.x,  image.width)))
        upper = round_up(min(upper, min(region.y, image.height)))
        right = round_up(max(right, min(region.x + region.w, image.width)))
        lower = round_up(max(lower, min(region.y + region.h, image.height)))
    if (right - left) > 0 and (lower - upper) > 0:
        image = image.crop((left, upper, right, lower))
        setattr(image, "x_offset", left)
        setattr(image, "y_offset", upper)

    setattr(image, "regions", regions)
    setattr(image, "really_size", really_size)

    return image

def OptimizeImage(image :Image, blocksize=16):
    rootNode = QuadTreeNode(image, None, 0, blocksize)
    opaque = doopt(sorted(rootNode.GetBBox(lambda x: x.type == BlockType.OPAQUE), key = lambda x : x.w * x.h, reverse=True))
    alpha = doopt(sorted(rootNode.GetBBox(lambda x: x.type == BlockType.ALPHA), key = lambda x : x.w * x.h, reverse=True))

    return CorpImageByRegion(image, Regions(alpha, opaque))