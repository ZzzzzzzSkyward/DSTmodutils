import sys
import xml.etree.ElementTree as ET
helptext='''Usage: python edit.py [.scml/build.xml] merge | Merge | add | delete | list | import | rename | purge
'''
nodenames={
    "xml":["Build","Symbol","Frame"],
    "anim":["Anims","anim","frame"],
    "scml":["spriter_data","folder","file"]
}
attrnames={
    "xml":["name","image"],
    "anim":["name","idx"],
    "scml":["name","name"],
}
#merge操作
def mergenode(symbol,target_symbol):
    print("merged node")
    if filetype=="xml":
        for frame in symbol.findall(Frame):
            framenum = frame.get('framenum')
            duration = frame.get('duration')
            image = frame.get('image')
            target_frame = target_symbol.find('./Frame[@framenum="{}"][@duration="{}"]'.format(framenum, duration))
            if target_frame is None or target_frame.get('image') != image:
                target_symbol.append(frame)
                print(frame)
    else:
        pass

def main(args):
    #符号
    filetype="scml" if args[1].find("scml")>=0 else "xml"
    if args[1].find("anim")>=0 and filetype=="xml":
        filetype="anim"
    symbolname=nodenames[filetype][1]
    Symbol="./"+symbolname
    framename=nodenames[filetype][2]
    Frame='./'+framename
    symbolattr=attrnames[filetype][0]
    frameattr=attrnames[filetype][1]

    # 解析xxx.xml/scml文件
    # args: cmd src params
    tree = ET.parse(args[1])
    root = tree.getroot()
    # 处理命令行参数
    #merge
    if args[0].find('m')>=0:
        # 合并a.xml文件
        merge_file = args[2]
        merge_tree = ET.parse(merge_file)
        merge_root = merge_tree.getroot()
        for symbol in merge_root.findall(Symbol):
            name = symbol.get('name')
            target_symbol = root.find((Symbol+'[@name="{}"]').format(name))
            if target_symbol is not None:
                mergenode(symbol, target_symbol)
            else:
                # 如果目标文件中不存在相同名称的Symbol节点，直接将整个Symbol节点添加到目标文件中
                root.append(symbol)
        tree.write(args[2])
    #merge scml操作，用于将一个scml的图片复制到另一个scml
    if args[0].find('M')>=0:
        merge_file = args[2]
        print(merge_file)
        merge_tree = ET.parse(merge_file)
        merge_root = merge_tree.getroot()
        print(Symbol)
        for symbol in merge_root.findall(Symbol):
            name = symbol.get('name')
            id=symbol.get('id')
            target_symbol = root.find('./folder[@name="{}"]'.format(name))
            if target_symbol is not None:
                print("overwrite", name)
                id=target_symbol.get('id')
                symbol.set('id',id)
                root.insert(int(id),symbol)
                root.remove(target_symbol)
            else:
                # 如果目标文件中不存在相同名称的Symbol节点，直接将整个Symbol节点添加到目标文件中
                root.append(symbol)
        tree.write(args[1])
    #delete
    elif args[0].find('d')>=0:
        # 删除指定的Symbol节点
        symbol_name = args[2]
        for symbol in root.findall(Symbol):
            if symbol.get(symbolattr) == symbol_name:
                root.remove(symbol)
        tree.write(args[1])
    #copy,add
    elif args[0].find('a')>=0 or args[1].find('c')>=0:
        # 从b.xml文件复制节点到xxx.xml
        symbol_name = args[2]
        add_file = args[3]
        add_tree = ET.parse(add_file)
        add_root = add_tree.getroot()
        name = symbol_name
        target_symbol = root.find((Symbol+'[@name="{}"]').format(name))
        for symbol in add_root.findall(Symbol):
            if symbol.get(symbolattr) == symbol_name:
                if target_symbol is not None:
                    if filetype=="xml":
                        mergenode(symbol, target_symbol)
                    else:
                        id=target_symbol.get('id')
                        root.remove(target_symbol)
                        symbol.set('id',id)
                        root.insert(int(id),symbol)
                else:
                    # 如果目标文件中不存在相同名称的Symbol节点，直接将整个Symbol节点添加到目标文件中
                    root.append(symbol)
        tree.write(args[1])
    #list
    elif args[0].find('l')>=0:
        syms=[i.get(symbolattr) for i in root.findall(Symbol)]
        print("\n".join(syms))
    #import
    elif args[0].find('i')>=0:
        # 从source.xml文件复制节点到xxx.xml，并对Symbol节点和Image属性进行重命名
        symbol_name = args[2]
        source_file = args[3]
        source_symbol_name = args[4]
        symbol_name = args[2]
        source_file = args[3]
        source_symbol_name = args[4]
        source_tree = ET.parse(source_file)
        source_root = source_tree.getroot()
        target_symbol = root.find((Symbol+'[@name="{}"]').format(symbol_name))
        if target_symbol is not None:
            print("Symbol already exists")
            sys.exit(1)
        # 复制Symbol节点
        for symbol in source_root.findall(Symbol):
            if symbol.get(symbolattr) == source_symbol_name:
                symbol.set(symbolattr, symbol_name)
                for frame in symbol.findall(Frame):
                    frame.set(frameattr, symbol_name + '-' + frame.get(frameattr).split('-')[-1])
                root.append(symbol)
        tree.write(args[1])
    #rename
    elif args[0].find('r')>=0:
        source_symbol_name = args[2]
        symbol_name = args[3]
        for symbol in root.findall(Symbol):
            if symbol.get(symbolattr) == source_symbol_name:
                symbol.set(symbolattr, symbol_name)
                for frame in symbol.findall(Frame):
                    frame.set(frameattr, symbol_name + '-' + frame.get(frameattr).split('-')[-1])
                root.append(symbol)
        tree.write(args[1])
    #purge
    elif args[0].find('p')>=0:
        # 遍历节点删除空属性 
        for elem in root.iter():
            for attr in list(elem.attrib):
                if not elem.attrib[attr]:
                    del elem.attrib[attr]
        tree.write(args[1], encoding='utf-8',xml_declaration=False)
    else:
        print(helptext)

if '__main__'==__name__:
    # 解析命令行参数
    args = sys.argv[1:]
    if len(args) < 2:
        print(helptext)
        sys.exit(1)
    main(args)