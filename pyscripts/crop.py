from PIL import Image
import sys


def crop(filename, x, y, nosave=False):
    # open image
    img = Image.open(filename)
    # 获取图片的 alpha 通道
    alpha = img.split()[-1]

    # 获取 alpha 通道中不透明的部分
    bbox = alpha.getbbox()

    # 裁剪图片
    img_cropped = img.crop(bbox)
    w, h = img.size
    w_, h_ = img_cropped.size
    wx = x * w
    hy = y * h
    bw = bbox[0]
    bh = bbox[1]
    if bw == 0 and bh == 0:
        print("Warning: the image is already cropped.")
        return
    x_final = (wx - bw) / w_
    y_final = (hy - bh) / h_
    y_final = 1 - y_final
    # 打印最终的红点坐标
    print(f"({x:.4f},{1-y:.4f})-> ({x_final:.4f}, {y_final:.4f})")
    # save image
    if not nosave:
        img_cropped.save(filename)
    return x_final,y_final


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python crop.py [filename] [pivot_x] [pivot_y] [nosave]\n Crop the image and calculate the new pivot point coordinates.\nnosave: do not crop image."
        )
        exit(1)
    im = sys.argv[1]
    px = float(sys.argv[2])
    x = px
    py = float(sys.argv[3])
    y = 1 - py
    nosave = len(sys.argv) > 4 and sys.argv[4][0] == "n"
    crop(im, x, y, nosave)
