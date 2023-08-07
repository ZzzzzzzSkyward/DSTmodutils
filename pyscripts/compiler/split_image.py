from klei.util import *
from PIL import Image
from xml.etree.ElementTree import Element, ElementTree

def SpitImage(xml_path, out_path, image_path):
    tree = ElementTree(file=xml_path) if isinstance(xml_path, str) else xml_path
    root = tree.getroot() if not isinstance(tree, Element) else tree

    data = {}
    for element in root.findall(".//Element"):
        name = element.get("name").replace(".tex", ".png")
        data[name] = {
            "x0": float(element.get("u1")),
            "x1": float(element.get("u2")),
            "y0": 1 - float(element.get("v2")),
            "y1": 1 - float(element.get("v1")),
        }

    with Image.open(image_path) as image:
        image = image.convert("RGBA")
        width, hight = image.size

        print("Spliting", len(data.keys()), "images")

        out_path = out_path + "/" + root.find("Texture").get("filename").replace(".tex", "")
        try_makedirs(out_path)
        for name in data.keys():
            box = (data[name]["x0"] * width, data[name]["y0"] * hight, data[name]["x1"] * width, data[name]["y1"] * hight)
            image.crop(box).save(out_path + "/" + name, format="PNG")
