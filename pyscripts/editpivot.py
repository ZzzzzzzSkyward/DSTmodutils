import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 4:
    print("Usage: python editpivot.py filename.scml name id x,y")
    sys.exit(1)

filename = sys.argv[1]
if not filename.endswith(".scml"):
    filename += ".scml"
tree = ET.parse(filename)
root = tree.getroot()

name = sys.argv[2]
id = sys.argv[3]
xy = sys.argv[4]
x, y = xy.split(",")
for folder in root.iter("folder"):
    if folder.get("name") == name:
        for file in folder.iter("file"):
            if file.get("id") == id:
                file.set("pivot_x", x)
                file.set("pivot_y", str(1 - float(y)))

tree.write(filename)
