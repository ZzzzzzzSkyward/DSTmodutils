'''
Make A Character's PO File from Official PO
从官方PO文件制作人物PO文件
'''
chs_po_path="chinese_s.po"
target_path="./target.po"
dest_path="./merged.po"
character="WILSON"
import sys
import os
import polib
import heapq
try:
    import rich
except ImportError:
    pass
class PO:
    head=r"""msgid ""
msgstr ""
"Language: zh\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"POT Version: 2.0"

"""
    def __init__(self, po_path):
        self.po_path = po_path
        self.po = polib.pofile(po_path)
        self.po_dict = {}
        for i in self.po:
            self.po_dict[i.msgctxt] = i.msgstr

    def __sub__(self, other):
        # erase from myself the same msgctxt as other
        for i in other.po:
            if i.msgctxt in self.po_dict:
                self.po_dict.pop(i.msgctxt)
        return self

    def __add__(self, other):
        # add from other msgctxt which I don't have
        for i in other.po:
            if i.msgctxt not in self.po_dict:
                self.add(i)

    def __eq__(self, other) -> bool:
        # compare myself with other by msgctxt and msgstr
        for i in other.po:
            if i.msgctxt not in self.po_dict:
                return False
            if i.msgstr != self.po_dict[i.msgctxt]:
                return False
        for i in self.po:
            if i.msgctxt not in other.po_dict:
                return False
            if i.msgstr != other.po_dict[i.msgctxt]:
                return False
        return True

    def __len__(self):
        # get keys of po_dict
        return len(self.po_dict)
    
    def remove(self,entry):
        if type(entry)!=str:
            entry=entry.msgctxt
        if entry not in self.po_dict:
            return
        del self.po_dict[entry]
    
    def add(self,entry,overwrite=False):
        if not overwrite and entry.msgctxt in self.po_dict:
            return
        self.po_dict[entry.msgctxt]=entry.msgstr
        self.po.append(entry)
    
    def save(self, filepath):
        # save the po_dict to a po file
        po = self.po
        with open(filepath,'w',encoding='utf-8') as f:
            f.write(self.head)
            for i in po:
                if i.msgctxt not in self.po_dict:
                    continue
                f.write("\n")
                f.write(f"#. {i.comment}")
                f.write("\n")
                f.write(f'msgctxt "{i.msgctxt}"')
                f.write("\n")
                f.write(f'msgid "{polib.escape(i.msgid)}"')
                f.write("\n")
                f.write(f'msgstr "{polib.escape(i.msgstr)}"')
                f.write("\n")
    def save_lua(self,filepath):
        # Save in lua format
        # msgctxt="(msgid escaped)"
        sorted_msg=[]
        for i in self.po_dict:
            heapq.heappush((i,self.po_dict[i]))
        sorted_str="\n".join(sorted_msg)
        with open(filepath, "wb") as f:
            f.write(sorted_str.encode('utf-8'))
            
    def keys(self):
        return list(self.po_dict.keys())
    
    def get(self,k):
        return self.po_dict.get(k,None)
    
    def set(self,k,v):
        self.po_dict[k]=v

def has_ref(text):
    words=text.split('.')
    if character in words:
        return True
    return False

def nonsense(id,text):
    if text.find("only_used_by_")>=0:
        return True
    if text.lower()=="n/a":
        return True
    return False
def clean_po():
    if __name__=='__main__':
        parse_args_clean(sys.argv[2:])
    if not os.path.exists(chs_po_path):
        print(f"{chs_po_path} not exist")
        return    
    srcpo=PO(chs_po_path)
    for i in list(srcpo.keys()):
        if nonsense(i,srcpo.get(i)):
            srcpo.remove(i)
    srcpo.save(target_path)
def do_po():
    if __name__=='__main__':
        parse_args_do(sys.argv[2:])
    if not os.path.exists(chs_po_path):
        print(f"{chs_po_path} not exist")
        return
    srcpo=PO(chs_po_path)
    for i in list(srcpo.keys()):
        if has_ref(i):
            continue
        srcpo.remove(i)
    srcpo.save(target_path)
def merge_po():
    if __name__=='__main__':
        parse_args_merge(sys.argv[2:])
    if not os.path.exists(chs_po_path):
        print(f"{chs_po_path} not exist")
        return
    if not os.path.exists(target_path):
        print(f"{target_path} not exist")
        return
    srcpo=PO(chs_po_path)
    mypo=PO(target_path)
    srcpo+mypo
    srcpo.save(dest_path)
def parse_args_do(args):
    global chs_po_path
    global target_path
    global character
    if len(args)>=1:
        character=args[0].upper()
        print(f"set character={character}")
    if len(args)>=2:
        target_path=args[1]
        print(f"set target={target_path}")
    if len(args)>=3:
        chs_po_path=args[2]
        print(f"set source={chs_po_path}")
    if len(args)>3 or len(args)<1:
        print("Usage: python make_po.py extract character [target.po] [source.po]")
def parse_args_merge(args):
    global chs_po_path
    global target_path
    global character
    global dest_path
    if len(args)>=1:
        chs_po_path=args[0]
        print(f"set source={chs_po_path}")
    if len(args)>=2:
        target_path=args[1]
        print(f"set my={target_path}")
    if len(args)>=3:
        dest_path=args[2]
        print(f"set save={dest_path}")
    if len(args)>3 or len(args)<1:
        print("Usage: python make_po.py merge src.po my.po [target.po]")
def parse_args_clean(args):
    global chs_po_path
    global target_path
    if len(args)>=1:
        chs_po_path=args[0]
        print(f"set source={chs_po_path}")
    if len(args)>=2:
        target_path=args[1]
        print(f"set my={target_path}")
    if len(args)>2 or len(args)<1:
        print("Usage: python make_po.py clean src.po [target.po]")
helptext="Error: no command given\nValid Commands:extract, merge, clean"
if __name__=='__main__':
    if len(sys.argv)<2:
        print(helptext)
        exit(0)
    command=sys.argv[1]
    if command=="extract":
        do_po()
    elif command=="merge":
        merge_po()
    elif command=="clean":
        clean_po()
    else:
        print(helptext)
        exit(0)
    