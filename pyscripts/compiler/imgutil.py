from PIL import Image, ImageOps

def compare_images(image1: str|Image.Image, image2: str|Image.Image):
    image1 = Image.open(image1).convert("RGBA") if isinstance(image1, str) else image1
    image2 = Image.open(image2).convert("RGBA") if isinstance(image2, str) else image2

    if image1.size != image2.size or image1.mode != image2.mode:
        return False

    pixel_pairs = zip(image1.getdata(), image2.getdata())
    if any(p1 != p2 for p1, p2 in pixel_pairs):
        return False

    return True

def Expand(image, border_size):
    new_img = ImageOps.expand(image, border=border_size)

    for i in range(border_size):
        left = border_size - i
        right = border_size + image.size[0] + i
        top = border_size - i
        bottom = border_size + image.size[1] + i - 1

        top_line = new_img.crop((left, top, right, top + 1))
        bottom_line = new_img.crop((left, bottom, right, bottom + 1))

        new_img.paste(top_line, (left, top - 1, right, top))
        new_img.paste(bottom_line, (left, bottom + 1, right, bottom + 2))

        left_line = new_img.crop((left, top - 1, left + 1, bottom + 2))
        right_line = new_img.crop((right-1, top - 1, right, bottom + 2))

        new_img.paste(left_line, (left - 1, top - 1, left, bottom + 2))
        new_img.paste(right_line, (right, top - 1, right + 1, bottom + 2))

    return new_img

def OpenImage(filename, size=None, border_size = 0):
    image = Image.open(filename).convert("RGBA")

    if size != None:
        image = image.resize(size, Image.LANCZOS)

    image = Expand(image, border_size)

    return image
