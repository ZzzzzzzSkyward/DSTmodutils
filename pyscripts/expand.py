from PIL import Image
import sys


def expand(filename, x, y, ratio=2.0,width=None,height=None):
    # open image
    img = Image.open(filename)
    owidth, oheight = img.size
    new_width = width or int(owidth * ratio)
    new_height = height or int(oheight * ratio)
    opivx,opivy=owidth*x,oheight*y
    npivx,npivy=new_width*x,new_height*y
    dx,dy=npivx-opivx,npivy-opivy
    image_expand = Image.new("RGBA", (new_width, new_height))
    image_expand.paste(img, (int(dx), int(dy)))
    image_expand.save(filename+".png")
    return x, y


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python expand.py [filename] [pivot_x] [pivot_y] [ratio|width] [height]\n expand the image by ratio, default is 2"
        )
        exit(1)
    im = sys.argv[1]
    px = float(sys.argv[2])
    x = px
    py = float(sys.argv[3])
    y = 1 - py
    r = float(sys.argv[4] if len(sys.argv) > 4 else 2)
    h=int(sys.argv[5]) if len(sys.argv)>5 else None
    if h:
        expand(im, x, y, width=int(r),height=h)
    else:
        expand(im, x, y, ratio=r)
