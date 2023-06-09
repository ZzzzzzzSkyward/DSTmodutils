import struct
from xml.dom.minidom import parseString
import sys
BUILDVERSION = 6

def strhash(str, hash_dict):
    hash = 0
    for c in str:
        v = ord(c.lower())
        hash = (v + (hash << 6) + (hash << 16) - hash) & 0xFFFFFFFF
    hash_dict[hash] = str
    return hash

def XmlToBuild( xml_path, output_path,endianstring="<"):
    hash_dict = {}

    xml_file = open(xml_path, "r")
    xml = parseString(xml_file.read())

    outfile = open(output_path, "wb")
    outfile.write(struct.pack(endianstring + "cccci", b"B", b"I", b"L", b"D", BUILDVERSION))

    symbols = xml.getElementsByTagName("Symbol")
    outfile.write(struct.pack(endianstring + "I", len(symbols)))
    outfile.write(struct.pack(endianstring + "I", len(xml.getElementsByTagName("Frame"))))

    buildname = xml.getElementsByTagName("Build")[0].getAttribute("name").encode("ascii")
    outfile.write(struct.pack(endianstring + "i" + str(len(buildname)) + "s", len(buildname), buildname))

    atlases = xml.getElementsByTagName("atlas")
    outfile.write(struct.pack(endianstring + "I", len(atlases)))
    for atlas in atlases:
        atlas_name = atlas.getAttribute("name")
        outfile.write(struct.pack(endianstring + "i" + str(len(atlas_name)) + "s", len(atlas_name), atlas_name.encode("ascii")))

    symbol_nodes = sorted(symbols, key=lambda x: strhash(x.getAttribute("name"), hash_dict))
    for symbol_node in symbol_nodes:
        symbolname = symbol_node.getAttribute("name")
        print(symbolname, strhash(symbolname, hash_dict))
        frames = symbol_node.getElementsByTagName("Frame")
        outfile.write(struct.pack(endianstring + "I", strhash(symbolname, hash_dict)))
        outfile.write(struct.pack(endianstring + "I", len(frames)))

        for frame_node in frames:
            framenum = int(frame_node.getAttribute("framenum"))
            duration = int(frame_node.getAttribute("duration"))
            w = float(frame_node.getAttribute("w"))
            h = float(frame_node.getAttribute("h"))
            x = float(frame_node.getAttribute("x"))
            y = float(frame_node.getAttribute("y"))
            alphaidx = int(frame_node.getAttribute("alphaidx"))
            alphacount = int(frame_node.getAttribute("alphacount"))

            outfile.write(struct.pack(endianstring + 'I', framenum))
            outfile.write(struct.pack(endianstring + 'I', duration))
            outfile.write(struct.pack(endianstring + 'ffff', x, y, w, h))

            outfile.write(struct.pack(endianstring + 'I', alphaidx))
            outfile.write(struct.pack(endianstring + 'I', alphacount))

    alphaverts = xml.getElementsByTagName("Vert")
    outfile.write(struct.pack(endianstring + 'I', len(alphaverts)))
    for vert in alphaverts:
        x = float(vert.getAttribute("x"))
        y = float(vert.getAttribute("y"))
        z = float(vert.getAttribute("z"))
        u = float(vert.getAttribute("u"))
        v = float(vert.getAttribute("v"))
        w = float(vert.getAttribute("w"))

        outfile.write(struct.pack(endianstring + 'ffffff', x, y, z, u, v, w))

    outfile.write(struct.pack(endianstring + 'I', len(hash_dict)))
    for hash_idx, name in hash_dict.items():
        outfile.write(struct.pack(endianstring + 'I', hash_idx))
        outfile.write(struct.pack(endianstring + 'i' + str(len(name)) + 's', len(name), name.encode("ascii")))

    outfile.close()
    xml_file.close()

if __name__=="__main__":
    if len(sys.argv)<2:
         print("Usage: xmltobuild.py in.xml out.bin")
    f=sys.argv[1]
    t=""
    if len(sys.argv)<3:
        t=f.replace(".xml",".bin")
    else:
        t=sys.argv[2]
    XmlToBuild(f,t)