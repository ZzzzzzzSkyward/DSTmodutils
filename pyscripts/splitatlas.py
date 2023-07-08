import os, struct, argparse
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from xml.etree.ElementTree import indent, SubElement, Element, ElementTree

def try_makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def SplitAltas(images: list, symbols: list[Element], alphaverts: list[dict], output_path):
    atlases = []
    for image in images:
        atlases.append(Image.open(image))

    try:
        for symbol in symbols:
            symbol_name = symbol.get("name")
            symbol_path = f"{output_path}/{symbol_name}"
            try_makedirs(symbol_path)

            for frame in symbol.findall(".//Frame"):
                alpha_idx = int(frame.get("alphaidx"))
                frame_path = f"{symbol_path}/{symbol_name}-{frame.get('framenum')}.png"

                w = int(float(frame.get("w")))
                h = int(float(frame.get("h")))
                x = float(frame.get("x"))
                y = float(frame.get("y"))

                x_offset = x - w // 2
                y_offset = y - h // 2

                verticies = alphaverts[alpha_idx: alpha_idx + int(frame.get("alphacount"))]

                if (verticies_len := len(verticies)) == 0 or max(u_list := [v[3] for v in verticies] or [0]) == min(u_list):
                    with open(frame_path, "w") as file:
                        file.write("")
                else:
                    region_verts = [verticies[i: i + 6] for i in range(0, verticies_len, 6)]

                    region_left = min(verts[0][0] for verts in region_verts)
                    region_right = max(verts[1][0] for verts in region_verts)
                    region_top = min(verts[0][1] for verts in region_verts)
                    region_bottom = max(verts[2][1] for verts in region_verts)

                    region_x = round(region_left - x_offset)
                    region_y = round(region_top - y_offset)
                    region_w = round(region_right - region_left)
                    region_h = round(region_bottom - region_top)

                    atlas = atlases[int(verticies[0][5])]
                    width, height = atlas.size

                    cropped = atlas.crop((
                        round(min(u_list) * width),
                        round((1 - max(v_list := [v[4] for v in verticies] or [0])) * height),
                        round(max(u_list) * width),
                        round((1 - min(v_list)) * height)
                    ))
                    if cropped.width != region_w or cropped.height != region_h:
                        cropped = cropped.resize((region_w, region_h))
                    if cropped.width != w or cropped.height != h:
                        new_image = Image.new("RGBA", (w, h))
                        new_image.paste(cropped, (region_x, region_y))
                        cropped = new_image
                    cropped.save(frame_path, format="png")

    finally:
        for atlas in atlases:
            atlas.close()

def BuildToXml(endianstring, build_path, output_path, images=[]):
    build = build_path
    if type(build_path) == str:
        build = open(build_path, "rb")
    elif not issubclass(build_path, BytesIO):
        return

    try:
        hash_dict = {}

        head = struct.unpack(endianstring + "cccci", build.read(8))

        symbol_num = struct.unpack(endianstring + "I", build.read(4))[0]
        frame_num = struct.unpack(endianstring + "I", build.read(4))[0]
        build_name_len = struct.unpack(endianstring + "I", build.read(4))[0]
        build_name = struct.unpack(endianstring + str(build_name_len) + "s", build.read(build_name_len))[0].decode("utf-8")
        atlas_num = struct.unpack(endianstring + "I", build.read(4))[0]

        root = Element("Build", name=build_name, version=str(head[4]))

        Atlas = SubElement(root, "Atlas", num=str(atlas_num))
        for atlas_idx in range(atlas_num):
            atlas_name_len = struct.unpack(endianstring + "I", build.read(4))[0]
            atlas_name = struct.unpack(endianstring + str(atlas_name_len) + "s", build.read(atlas_name_len))[0].decode("utf-8")

            SubElement(Atlas, "atlas", name=atlas_name)

        Symbols = SubElement(root, "Symbols", num=str(symbol_num))
        for symbol_idx in range(symbol_num):
            symbolname_hash = struct.unpack(endianstring + "I", build.read(4))[0]
            frames_len = struct.unpack(endianstring + "I", build.read(4))[0]
            symbol = SubElement(Symbols, "Symbol", name=symbolname_hash)

            for frame_idx in range(frames_len):
                framenum = struct.unpack(endianstring + "I", build.read(4))[0]
                duration = struct.unpack(endianstring + "I", build.read(4))[0]
                x, y, w, h = struct.unpack(endianstring + "ffff", build.read(16))
                alphaidx = struct.unpack(endianstring + "I", build.read(4))[0]
                alphacount = struct.unpack(endianstring + "I", build.read(4))[0]

                SubElement(symbol, "Frame", framenum=str(framenum), duration=str(duration), x=str(x), y=str(y), w=str(w), h=str(h), alphaidx=str(alphaidx), alphacount=str(alphacount))

        alphaverts = []
        alphaverts_len = struct.unpack(endianstring + "I", build.read(4))[0]
        Alphavert = SubElement(root, "AlphaVert", num=str(alphaverts_len))
        for vert_idx in range(alphaverts_len):
            x, y, z, u, v, w = struct.unpack(endianstring + "ffffff", build.read(24))
            alphaverts.append((x, y, z, u, v, w))
            SubElement(Alphavert, "Vert", x=str(x), y=str(y), z=str(z) , u=str(u), v=str(v), w=str(w))

        hash_dict_len = struct.unpack(endianstring + "I", build.read(4))[0]
        for hash_idx in range(hash_dict_len):
            hash = struct.unpack(endianstring + "I", build.read(4))[0]
            hash_str_len = struct.unpack(endianstring + "i", build.read(4))[0]

            hash_str = struct.unpack(endianstring + str(hash_str_len) + "s", build.read(hash_str_len))[0]

            hash_dict[hash] = hash_str

        symbols = Symbols.findall(".//Symbol")
        for symbol in symbols:
            symbolname_hash = symbol.get("name")
            symbol_name = hash_dict[symbolname_hash]
            symbol.set("name", symbol_name.decode("utf-8"))

        if len(images) > 0:
            output_path = f"{output_path}/{build_name}"
            try_makedirs(output_path)
            SplitAltas(images, symbols, alphaverts, output_path)

        tree = ElementTree(root)
        indent(tree, space="    ")
        tree.write(output_path + "/build.xml", encoding="utf-8")

    finally:
        build.close()


TOOL_PATH = os.path.dirname(__file__)
KTECH_CONVERTER = os.path.abspath(os.path.join(TOOL_PATH, "Z_ktools-4.4/ktech.exe"))
import sys
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert build.bin or build.xml file")
    parser.add_argument("dir")
    args = parser.parse_args()

    endianstring = "<"
    input_path = sys.argv[1] or parser.dir
    file_type = os.path.splitext(input_path)[1]
    root_part = os.path.split(input_path)[0]

    if file_type == ".zip":
        with TemporaryDirectory()as temp_dir, ZipFile(input_path) as input_zip:
            namelist = input_zip.namelist()
            if "build.bin" in namelist:
                images = []
                input_zip.extractall(path=temp_dir)
                for tex in [name for name in namelist if name.find(".tex") != -1]:
                    images.append(os.path.splitext(tex)[0] + ".png")
                    os.system(f"\" \"{KTECH_CONVERTER}\" \"{temp_dir}\\{tex}\" \"{temp_dir}\" \"")

                BuildToXml(endianstring, f"{temp_dir}/build.bin", root_part, images=[f"{temp_dir}/{image}" for image in images])

    #

    if file_type == ".bin":
        BuildToXml(endianstring, input_path, root_part,[os.path.abspath(root_part+"/"+i) for i in os.listdir(root_part) if i.endswith(".png")])
    #     print("Success to xml")
    # elif file_type == ".xml":
    #     XmlToBuild(endianstring, input_path, root_part + "_new.bin")
    #     print("Success to build")
    # else:
    #     print("not supported file type")
