from PIL import Image
import sys


def crop_abs(filename, x, y):
    # open image
    img = Image.open(filename)
    # 获取 alpha 通道中不透明的部分
    bbox = img.split()[-1].getbbox()
    if not bbox:
        # print("不可裁剪的图片")
        return None, None, None, None
    # 裁剪图片
    img_cropped = img.crop(bbox)
    w, h = img_cropped.size
    bw = bbox[0]
    bh = bbox[1]
    if bw == 0 and bh == 0:
        print("不可裁剪的图片")
        return None, None, None, None
    x_final = x - bw
    y_final = y - bh
    # save image
    img_cropped.save(filename)
    return x_final, y_final, w, h


def crop(filename, x=None, y=None, nosave=False):
    shouldprint = __name__ == "__main__"
    # open image
    img = Image.open(filename)
    # 获取图片的 alpha 通道
    alpha = img.split()[-1]

    # 获取 alpha 通道中不透明的部分
    bbox = alpha.getbbox()

    # 裁剪图片
    img_cropped = img.crop(bbox)
    if x is not None and y is not None:
        w, h = img.size
        w_, h_ = img_cropped.size
        wx = x * w
        hy = y * h
        bw = bbox[0] if bbox else 0
        bh = bbox[1] if bbox else 0
        if bw == 0 and bh == 0:
            if shouldprint:
                print("Warning: the image is already cropped.")
            return None, None, None, None
        x_final = (wx - bw) / w_
        y_final = (hy - bh) / h_
        y_final = 1 - y_final
        # 打印最终的红点坐标
        if shouldprint:
            print(f"({x:.4f},{1-y:.4f})-> ({x_final:.4f}, {y_final:.4f})")
    # save image
    if not nosave:
        img_cropped.save(filename)
    if x is not None and y is not None:
        return x_final, y_final, w_, h_
    return None, None, None, None


def crop_image(filename, max_width=None, max_height=None,
               target_width=None, target_height=None):
    img = Image.open(filename).convert("RGBA")
    width, height = img.size

    # 计算裁剪后的尺寸
    if target_width and target_height:
        new_width, new_height = target_width, target_height
    elif max_width and max_height:
        aspect_ratio = min(
            1, min(
                float(max_width) / width, float(max_height) / height))
        new_width = int(width * aspect_ratio)
        new_height = int(height * aspect_ratio)
    else:
        new_width, new_height = width, height

    # 裁剪图像
    img_cropped = img.resize((new_width, new_height), Image.LANCZOS)
    img_cropped.save(filename)
    return img_cropped


def uncrop(filename, x, y, nosave=False):
    # 打开图片
    img = Image.open(filename)
    w, h = img.size

    # 计算出映射后图片的最小宽高
    new_width = int(2 * max(x, 1 - x) * w)
    new_height = int(2 * max(y, 1 - y) * h)
    # 放大画布以容纳原图片
    min_width = new_width
    min_height = new_height
    if min_height == h and min_width == w:
        return

    # 新建 RGBA 格式图片
    new_img = Image.new('RGBA', (min_width, min_height))

    # 计算偏移量,使(x, y)变为中心
    offset_x = 0 if x > 0.5 else min_width - w
    offset_y = 0 if y > 0.5 else min_height - h

    # 粘贴图片
    new_img.paste(img, (offset_x, offset_y))

    # Save new image
    if not nosave:
        new_img.save(filename)

    return 0.5, 0.5


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python crop.py [filename] ([pivot_x] [pivot_y] [nosave] [uncrop])\n Crop the image and calculate the new pivot point coordinates.\nnosave: do not crop image.\nuncrop: crop image so that pivot is (0.5,0.5)"
        )
        exit(1)
    im = sys.argv[1]
    if len(sys.argv) < 4:
        crop_image(im)
        exit(0)
    px = float(sys.argv[2])
    x = px
    py = float(sys.argv[3])
    if x > 10:
        crop_image(im, px, py)
        exit(0)
    y = 1 - py
    nosave = len(sys.argv) > 4 and sys.argv[4][0] == "n"
    un = len(sys.argv) > 5 and sys.argv[5][0] == "u"
    if un:
        uncrop(im, x, y, nosave)
    else:
        crop(im, x, y, nosave)
