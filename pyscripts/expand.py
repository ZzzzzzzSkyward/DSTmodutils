from PIL import Image
import sys


def expand(filename, x, y, ratio=2.0):
    # open image
    img = Image.open(filename)
    width, height = img.size
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    image_expand = Image.new("RGBA", (new_width, new_height))
    image_expand.paste(img, (int(width * x), int(height * y)))
    image_expand.save(filename)
    return x, y


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python expand.py [filename] [pivot_x] [pivot_y] [ratio]\n expand the image by ratio, default is 2"
        )
        exit(1)
    im = sys.argv[1]
    px = float(sys.argv[2])
    x = px
    py = float(sys.argv[3])
    y = 1 - py
    r = float(sys.argv[4] if len(sys.argv) > 4 else 2)
    expand(im, x, y, r)
