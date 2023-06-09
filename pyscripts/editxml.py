from re import A
import sys
import xml.etree.ElementTree as ET
helptext='''Usage: python edit.py [.scml/build.xml] merge | add | delete | list | import | rename
'''
nodenames={
    "xml":["Build","Symbol","Frame"],
    "scml":["spriter_data","folder","file"]
}
attrnames={
    "xml":["name","image"],
    "scml":["name","name"],
}
# 解析命令行参数
args = sys.argv[1:]
if len(args) < 2:
    print(helptext)
    sys.exit(1)
#符号
filetype="scml" if args[0].find("scml")>=0 else "xml"
symbolname=nodenames[filetype][1]
Symbol="./"+symbolname
framename=nodenames[filetype][2]
Frame='./'+framename
symbolattr=attrnames[filetype][0]
frameattr=attrnames[filetype][1]

# 解析xxx.xml/scml文件
tree = ET.parse(args[0])
root = tree.getroot()
#merge操作
def mergenode(symbol,target_symbol):
    print("merged node")
    for frame in symbol.findall('./Frame'):
        framenum = frame.get('framenum')
        duration = frame.get('duration')
        image = frame.get('image')
        target_frame = target_symbol.find('./Frame[@framenum="{}"][@duration="{}"]'.format(framenum, duration))
        if target_frame is None or target_frame.get('image') != image:
            target_symbol.append(frame)
            print(frame)
# 处理命令行参数
#merge
if args[1].find('m')>=0:
    # 合并a.xml文件
    merge_file = args[2]
    merge_tree = ET.parse(merge_file)
    merge_root = merge_tree.getroot()
    for symbol in merge_root.findall(Symbol):
        name = symbol.get('name')
        target_symbol = root.find('./Symbol[@name="{}"]'.format(name))
        if target_symbol is not None:
            mergenode(symbol, target_symbol)
        else:
            # 如果目标文件中不存在相同名称的Symbol节点，直接将整个Symbol节点添加到目标文件中
            root.append(symbol)
    tree.write(args[0])
#delete
elif args[1].find('d')>=0:
    # 删除指定的Symbol节点
    symbol_name = args[2]
    for symbol in root.findall(Symbol):
        if symbol.get(symbolattr) == symbol_name:
            root.remove(symbol)
    tree.write(args[0])
#copy,add
elif args[1].find('a')>=0 or args[1].find('c')>=0:
    # 从b.xml文件复制节点到xxx.xml
    symbol_name = args[2]
    add_file = args[3]
    add_tree = ET.parse(add_file)
    add_root = add_tree.getroot()
    name = symbol_name
    target_symbol = root.find('./Symbol[@name="{}"]'.format(name))
    for symbol in add_root.findall(Symbol):
        if symbol.get(symbolattr) == symbol_name:
            if target_symbol is not None:
                mergenode(symbol, target_symbol)
            else:
                # 如果目标文件中不存在相同名称的Symbol节点，直接将整个Symbol节点添加到目标文件中
                root.append(symbol)
    tree.write(args[0])
#list
elif args[1].find('l')>=0:
    syms=[i.get(symbolattr) for i in root.findall(Symbol)]
    print("\n".join(syms))
#import
elif args[1].find('i')>=0:
    # 从source.xml文件复制节点到xxx.xml，并对Symbol节点和Image属性进行重命名
    symbol_name = args[2]
    source_file = args[3]
    source_symbol_name = args[4]
    symbol_name = args[2]
    source_file = args[3]
    source_symbol_name = args[4]
    source_tree = ET.parse(source_file)
    source_root = source_tree.getroot()
    target_symbol = root.find('./Symbol[@name="{}"]'.format(symbol_name))
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
    tree.write(args[0])
#rename
elif args[1].find('r')>=0:
    source_symbol_name = args[2]
    symbol_name = args[3]
    for symbol in root.findall(Symbol):
        if symbol.get(symbolattr) == source_symbol_name:
            symbol.set(symbolattr, symbol_name)
            for frame in symbol.findall(Frame):
                frame.set(frameattr, symbol_name + '-' + frame.get(frameattr).split('-')[-1])
            root.append(symbol)
    tree.write(args[0])

else:
    print(helptext)
    sys.exit(1)
