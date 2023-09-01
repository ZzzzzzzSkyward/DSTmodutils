from istransparent import istransparent
import os
from PIL import Image
from crop import crop_abs


def clip_symbols(symbols: dict, name, path):
    flag = True
    for symbol in symbols:
        x, y, h, w = symbol.get(
            "x", 0), symbol.get(
            "y", 0), symbol.get(
                "h", 0), symbol.get(
                    "w", 0)
        frame = symbol.get("framenum")
        if frame is None:
            frame = symbol.get("frame")
        if frame is None:
            print("图片", name, "没有frame")
            continue
        img_path = os.path.join(path, name, name + "-" + str(frame) + ".png")
        img_path = os.path.abspath(img_path)
        if not os.path.exists(img_path):
            print("图片", img_path, "不存在")
            continue
        with Image.open(img_path) as image:
            if image.width != w:
                #print("Image", name, "-", frame, "has wrong record width")
                print("图片", name, "-", frame, "宽度记录有误")
                symbol["w"] = image.width
                w = symbol["w"]
            if image.height != h:
                print("图片", name, "-", frame, "高度记录有误")
                symbol["h"] = image.height
                h = symbol["h"]
        if not istransparent(img_path):
            flag = False
            # 裁剪
            px, py = w / 2 - x, h / 2 - y
            _px, _py, _w, _h = crop_abs(img_path, px, py)
            if _px and _py and _w and _h:
                _x, _y = (_w / 2 - _px), (_h / 2 - _py)
                symbol["x"] = _x
                symbol["y"] = _y
                symbol["w"] = _w
                symbol["h"] = _h
                print(
                    name,
                    frame,
                    "\n",
                    x,
                    y,
                    w,
                    h,
                    "\n",
                    _x,
                    _y,
                    _w,
                    _h,
                    px,
                    py,
                    _px,
                    _py)

    return flag


def clip(data: dict):
    if "Symbol"not in data:
        print("json数据不是build")
        return False
    path = data.get("Path", "")
    if not os.path.exists(path):
        path = ""
    keys = list(data["Symbol"].keys())
    for symbol in keys:
        symdata = data["Symbol"][symbol]
        flag = clip_symbols(symdata, symbol, path)
        if flag:
            print("删除透明文件夹", symbol)
            del data["Symbol"][symbol]
    return True
