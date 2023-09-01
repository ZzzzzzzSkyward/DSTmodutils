import os, glob
from PIL import Image
from .anim_util import *
from . import atlas_image, imgutil
from .properties import ImageProperties
from tempfile import TemporaryDirectory
from xml.etree.ElementTree import ElementTree
from .ktech import tex_to_png
from .stex import png_to_tex

def AtlasImages(image_dir):
    with TemporaryDirectory() as temp_path:
        dir_name = os.path.split(image_dir)[1]

        output = image_dir + "/output"
        try_makedirs(output)

        images_paths = glob.glob(os.path.join(image_dir, "*.png"))
        dest_filename = os.path.join(output, dir_name + ".tex")
        xml_filename = os.path.join(output, dir_name + ".xml")

        print("Processing " + dir_name)

        size = None
        border_size = 0
        element_prefix = ""

        for propertie in ImageProperties:
            if dir_name.find(propertie) != -1:

                width = ImageProperties[propertie].get("width", None)
                height = ImageProperties[propertie].get("height", None)
                border_size = ImageProperties[propertie].get("border", 0)
                element_prefix = ImageProperties[propertie].get("prefix", "")

                if width is not None and height is not None:
                    size = (width, height)

                break

        images = []
        for image_path in images_paths:
            image = imgutil.OpenImage(image_path, size=size, border_size=border_size)
            image.name = os.path.splitext(os.path.basename(image_path))[0] + ".tex"
            images.append(image)

        atlas_data = atlas_image.Atlas(images, dir_name)
        assert len(atlas_data) == 1
        page = atlas_data[0]

        mip = atlas_data[0].mips
        mip.im.save(os.path.join(temp_path, dir_name + ".png"))
        png_to_tex(os.path.join(temp_path, dir_name + ".png"), dest_filename)

        xml = atlas_image.GenerateXMLTree(dest_filename, mip.im.size, page.bboxes, border_size + 0.5,  element_prefix=element_prefix)
        xml.write(xml_filename)


def SpitImage(xml_path, out_path, tex_path: str):
    root = ElementTree(file=xml_path).getroot()

    data = {}
    for element in root.findall(".//Element"):
        name = element.get("name").replace(".tex", ".png")
        data[name] = {
            "x0": float(element.get("u1")),
            "x1": float(element.get("u2")),
            "y0": 1 - float(element.get("v2")),
            "y1": 1 - float(element.get("v1")),
        }

    tex_to_png(tex_path, os.path.split(tex_path)[0])

    with Image.open(tex_path.replace(".tex", ".png")) as image:
        image = image.convert("RGBA")
        width, hight = image.size

        print("Spliting", len(data.keys()), "images")

        out_path = out_path + "/" + root.find("Texture").get("filename").replace(".tex", "")
        try_makedirs(out_path)
        for name in data.keys():
            box = (data[name]["x0"] * width, data[name]["y0"] * hight, data[name]["x1"] * width, data[name]["y1"] * hight)
            image.crop(box).save(out_path + "/" + name, format="PNG")
