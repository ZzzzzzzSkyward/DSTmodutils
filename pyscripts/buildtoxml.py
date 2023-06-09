import struct
from xml.etree.ElementTree import indent, SubElement, Element, ElementTree
import sys
def BuildToXml(build_path, output_path,endianstring="<"):
    hash_dict = {}

    build = open(build_path, "rb")
    head = struct.unpack(endianstring + "cccci", build.read(8))

    symbol_num = struct.unpack(endianstring + "I", build.read(4))[0]
    frame_num = struct.unpack(endianstring + "I", build.read(4))[0]
    build_name_len = struct.unpack(endianstring + "I", build.read(4))[0]
    buildname = struct.unpack(endianstring + str(build_name_len) + "s", build.read(build_name_len))[0]
    atlas_num = struct.unpack(endianstring + "I", build.read(4))[0]

    root = Element("Build", name=buildname.decode("utf-8"))

    Atlas = SubElement(root, "Atlas", num=str(atlas_num))
    for atlas_idx in range(atlas_num):
        atlas_name_len = struct.unpack(endianstring + "I", build.read(4))[0]
        atlas_name = struct.unpack(endianstring + str(atlas_name_len) + "s", build.read(atlas_name_len))[0]

        SubElement(Atlas, "atlas", name=atlas_name.decode("utf-8"))

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

    alphaverts_len = struct.unpack(endianstring + "I", build.read(4))[0]
    Alphavert = SubElement(root, "AlphaVert", num=str(alphaverts_len))
    for vert_idx in range(alphaverts_len):
        vert = struct.unpack(endianstring + "ffffff", build.read(24))
        SubElement(Alphavert, "Vert", x=str(vert[0]), y=str(vert[1]), z=str(vert[2]) , u=str(vert[3]), v=str(vert[4]), w=str(vert[5]))

    hash_dict_len = struct.unpack(endianstring + "I", build.read(4))[0]
    for hash_idx in range(hash_dict_len):
        hash = struct.unpack(endianstring + "I", build.read(4))[0]
        hash_str_len = struct.unpack(endianstring + "i", build.read(4))[0]

        hash_str = struct.unpack(endianstring + str(hash_str_len) + "s", build.read(hash_str_len))[0]

        hash_dict[hash] = hash_str

        # print("hash_str_len", hash_str_len)
        # print("hash_str", hash_str)

    symbols = Symbols.findall("Symbol")
    for symbol in symbols:
        symbolname_hash = symbol.get("name")
        symbolname = hash_dict[symbolname_hash]
        symbol.set("name", symbolname.decode("utf-8"))

    tree = ElementTree(root)
    indent(tree, space="    ")
    tree.write(output_path, encoding="utf-8")
    build.close()

    # print(struct.calcsize(endianstring + "ffffff"))
if __name__=="__main__":
    if len(sys.argv)<2:
         print("Usage: buildtoxml.py in.bin out.xml")
    f=sys.argv[1]
    t=""
    if len(sys.argv)<3:
        t=f.replace(".bin",".xml")
    else:
        t=sys.argv[2]
    BuildToXml(f,t)