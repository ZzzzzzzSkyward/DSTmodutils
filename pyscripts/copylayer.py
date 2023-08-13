from lxml import etree
import sys

def copy_layername(file1, file2):
    # 使用lxml解析第一个XML文件
    tree1 = etree.parse(file1)
    root1 = tree1.getroot()

    # 使用lxml解析第二个XML文件
    tree2 = etree.parse(file2)
    root2 = tree2.getroot()

    # 遍历第二个XML中的每个<anim>元素
    for anim2 in root2.iter("anim"):
        name2 = anim2.attrib['name']

        # 在第一个XML中查找具有相同'name'属性值的<anim>元素
        anims1_with_same_name = root1.xpath('//anim[@name="' + name2 + '"]')

        if len(anims1_with_same_name) > 0:
            anim1 = anims1_with_same_name[0]

            # 遍历每对对应的<frame>
            frames_list_01 = list(anim1.iter("frame"))
            frames_list_02= list(anim2.iter("frame"))

            src_elements= list(frame_element_01.iter("element"))
            processed=[]
            for i in range(len(frames_list_02)):
                frame_element_02= frames_list_02[i]
                for element_index, element in enumerate(src_elements):
                    if element_index in processed:
                        continue
                    name_value= element.attrib["name"]
                    if frame_element_02.attrib["name"]== name_value:
                        layername_value= element.attrib["layername"]
                        frame_element_02.set("layername", layername_value)
                        processed.append(element_index)
                        break

    # 将修改后的第二个XML保存到新文件中（如果需要覆盖原始文件，可以直接使用file2）
    modified_file_name = "modified_" + file2
    tree2.write(modified_file_name)

if __name__ == "__main__":
   if len(sys.argv) < 3:
       print("python copylayer.py fromxml1 toxml2\nCopy the layername from xml1 to xml2.")
   else:
       file_path_01 = sys.argv[1]
       file_path_02= sys.argv[2]
       copy_layername(file_path_01, file_path_02)