'''
修改坐标
'''
import xml.etree.ElementTree as ET

filename = input("请输入文件名：")
if not filename.endswith(".scml"):
    filename += ".scml"
tree = ET.parse(filename)
root = tree.getroot()


while True:
    name = input("请输入名称：")
    if not name:
        break

    id = input("请输入ID ")
    xy = input("请输入X,Y ")
    x, y = xy.split(",")
    if not x or not y:
        break
    for folder in root.iter("folder"):
        if folder.get("name") == name:
            for file in folder.iter("file"):
                if file.get("id") == id:
                    file.set("pivot_x", x)
                    file.set("pivot_y", str(1 - float(y)))

    tree.write(filename + ".scml")
