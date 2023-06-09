import os
import argparse
from buildtoxml import BuildToXml
from xmltobuild import XmlToBuild

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert build.bin or build.xml file")
    parser.add_argument("dir")
    args = parser.parse_args()

    endianstring = "<"
    input_path = args.dir
    root_part, file_type = os.path.splitext(input_path)

    if file_type == ".bin":
        BuildToXml(input_path, root_part + ".xml",endianstring)
    elif file_type == ".xml":
        XmlToBuild(input_path, root_part + ".bin",endianstring)
    else:
        print("not supported file type")