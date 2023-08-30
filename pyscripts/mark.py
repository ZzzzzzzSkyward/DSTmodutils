"""
添加红点
"""
from PIL import Image
import numpy as np
import xml.etree.ElementTree as ET
import os
import sys


def mark(filename, radius=1):
    # Parse the .scml file
    tree = ET.parse(filename)
    root = tree.getroot()

    # Iterate through each file element
    for folder in root.iter("folder"):
        folder_name = folder.get("name")

        for file in folder.iter("file"):
            file_name = file.get("name") or ""
            file_path = os.path.join(os.path.dirname(filename), file_name).replace(
                "/", "\\"
            )
            # Read the image file

            # Open the image file using Pillow
            try:
                img_pil = Image.open(file_path, formats=["PNG"])
                if img_pil.mode != "RGBA":
                    img_pil = img_pil.convert("RGBA")

            # Convert the image to a numpy array
            except IOError:
                print("Error: cannot read image file: " + file_path)
                continue

            img = np.array(img_pil)
            # Get pivot_x and pivot_y
            pivot_x = int(float(file.get("pivot_x") or 0) * img.shape[1])
            pivot_y = int(float(file.get("pivot_y") or 0) * img.shape[0])

            # Add a red pixel at the pivot point
            for i in range(-radius, radius):
                for j in range(-radius, radius):
                    if i**2 + j**2 <= radius**2:
                        try:
                            img[pivot_y + j, pivot_x +
                                i] = np.array([255, 0, 0, 255])
                        except IndexError:
                            pass

            # Save the modified image
            img_pil = Image.fromarray(img, mode="RGBA")
            img_pil.save(file_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python mark.py [filename]\n Mark the pivot points of the Spriter project file (.scml)"
        )
        sys.exit(1)
    filename = sys.argv[1]
    radius = len(sys.argv) > 2 and int(sys.argv[2]) or 1
    mark(filename, radius)
