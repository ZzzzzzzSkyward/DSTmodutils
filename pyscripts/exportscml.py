#istransparent:判断图片全透明
from istransparent import istransparent
#裁剪图片并返回裁剪后的节点值pivot_x、pivot_y
from crop import crop
from lxml import etree as ET
import sys
import shutil
def assign_new_ids(root):
    id = 0
    for folder in root.iter('folder'):
        if folder is not None:
            if folder.get('toremove'):
                for i in root.iter('obj_info'):
                    if i.get('updated'):
                        continue
                    if i.get('realname')==folder.get('name'):
                        i.getparent().remove(i)
                for i in root.iter('object'):
                    if i.get('updated'):
                        continue
                    if i.get('folder')==folder.get('id'):
                        i.getparent().getparent().remove(i.getparent())
                for i in root.iter('object_ref'):
                    if i.get('updated'):
                        continue
                    if i.get('folder')==folder.get('id'):
                        for j in i.getparent().getparent().iter('object_ref'):
                            if j.get('id')==i.get('id'):
                                j.getparent().remove(j)
                folder.getparent().remove(folder)
            else:
                folder.set('id', str(id))
                # 更新相关XML文件中的i节点folder属性
                for i in root.iter('i'):
                    if i.get('updated'):
                        continue
                    if i.get('folder') == folder.get('id'):
                        i.set('folder', str(id))
                        i.set('updated','1')
                for i in root.iter('object'):
                    if i.get('updated'):
                        continue
                    if i.get('folder') == folder.get('id'):
                        i.set('folder', str(id))
                        i.set('updated','1')
                id += 1
    # 删除已删除folder对应的i节点
    for i in root.iter('i'):
        try:
            del i.attrib['updated']
        except:
            pass
    for i in root.iter('object'):
        try:
            del i.attrib['updated']
        except:
            pass
def exportscml(xml_file,nocrop=False):
    #解析XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    #遍历所有folder节点
    for folder in root.iter('folder'):
        remove = True
        #遍历folder下的所有file节点
        for file in folder.iter('file'):
            filename = file.get('name')
            if not istransparent(filename):
                remove = False
                pivot_x = float(file.get('pivot_x'))
                pivot_y = float(file.get('pivot_y'))
                try:
                    pivot_x_new, pivot_y_new,w,h = crop(filename, pivot_x, 1-pivot_y,nocrop)
                    file.set('pivot_x', str(pivot_x_new))
                    file.set('pivot_y', str(pivot_y_new))
                    file.set('width', str(w))
                    file.set('height', str(h))
                    print(filename,w,h)
                except Exception:
                    pass
            else:
                print(filename,"是透明的")
        #如果所有图片都是全透明,则删除整个folder节点
        if remove:
            print("文件夹",folder.get('name'),'全透明')
            #folder.set('toremove','1')
            #删除文件夹
            if not nocrop:
                shutil.rmtree(folder.get('name'))
    #assign_new_ids(root)
    if not nocrop:
        tree.write(xml_file, encoding='utf-8')

if __name__=='__main__':
    if len(sys.argv) < 2:
        print(
            "Usage: python exportscml.py [scml file name] [nocrop]\n Crop the images and calculate the new pivot point coordinates and update image width, height."
        )
        exit(1)
    scml = sys.argv[1]
    nocrop=len(sys.argv)>2
    exportscml(scml,nocrop)
