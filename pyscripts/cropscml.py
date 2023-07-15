import xml.etree.ElementTree as ET
import sys
from crop import crop as crop_func
def crop_pivot_values(xml_file):
    # 解析XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 遍历所有的file节点
    for file_node in root.iter('file'):
        # 获取pivot_x和pivot_y属性的值
        pivot_x = float(file_node.get('pivot_x'))
        pivot_y = float(file_node.get('pivot_y'))
        filename=file_node.get('name')
        # 使用crop_func函数处理pivot_x和pivot_y的值
        try:
            pivot_x_new, pivot_y_new = crop_func(filename, pivot_x, 1-pivot_y)
        except:
            continue
        # 更新file节点的pivot_x和pivot_y属性
        file_node.set('pivot_x', str(pivot_x_new))
        file_node.set('pivot_y', str(pivot_y_new))

    # 保存更改后的XML文件
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

if __name__=='__main__':
    if len(sys.argv) < 2:
        print(
            "Usage: python cropscml.py [scml file name]\n Crop the images and calculate the new pivot point coordinates."
        )
        exit(1)
    scml = sys.argv[1]
    crop_pivot_values(scml)
