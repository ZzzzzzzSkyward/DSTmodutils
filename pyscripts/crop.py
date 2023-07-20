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

def uncrop(filename, x, y, nosave=False):
    # 打开图片
    img = Image.open(filename)
    w, h = img.size
    
    # 计算出映射后图片的最小宽高     
    new_width = int(2 * max(x,1-x) * w)
    new_height = int(2 * max(y,1-y) * h)
    #放大画布以容纳原图片
    min_width=new_width
    min_height=new_height
    if min_height==h and min_width==w:
        return
    
    # 新建 RGBA 格式图片    
    new_img = Image.new('RGBA', (min_width, min_height))
    
    # 计算偏移量,使(x, y)变为中心      
    offset_x = 0 if x>0.5 else min_width-w
    offset_y = 0 if y>0.5 else min_height-h
            
    # 粘贴图片      
    new_img.paste(img,(offset_x, offset_y))
  
    # Save new image  
    if not nosave:
        new_img.save(filename)

    return 0.5,0.5

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python crop.py [filename] [pivot_x] [pivot_y] [nosave] [uncrop]\n Crop the image and calculate the new pivot point coordinates.\nnosave: do not crop image.\nuncrop: crop image so that pivot is (0.5,0.5)"
        )
        exit(1)
    im = sys.argv[1]
    px = float(sys.argv[2])
    x = px
    py = float(sys.argv[3])
    y = 1 - py
    nosave = len(sys.argv) > 4 and sys.argv[4][0] == "n"
    un = len(sys.argv) > 5 and sys.argv[5][0] == "u"
    if un:
        uncrop(im,x,y,nosave)
    else:
        crop(im, x, y, nosave)
