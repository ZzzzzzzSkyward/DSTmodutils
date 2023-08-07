import sys 
import os
from scml import Scml
from anim import DSAnim
from ktech import *
def build(mod_path, dest=None):
    a = Scml(mod_path)
    anim_path = os.path.join(os.path.dirname(mod_path), '../anim/') 
    if dest:
        pass
    elif os.path.exists(anim_path):      
        dest = anim_path
    else:               
        dest = './'              
    a.build_scml(dest, 1)
def unzipanim(path,dest=None,mapping=False):
    anims = []
    root=os.path.abspath(path)
    anims.append(DSAnim(root))
    root=os.path.dirname(root)
    for anim in anims[1:]:
        anims[0] += anim
    anims[0].to_scml(root, mapping=mapping)

    for anim in anims:
        anim.close()

if __name__ == '__main__':
    args=sys.argv[1:]
    ext=os.path.splitext(args[0])[-1]
    print(ext)
    if ext.find("scml")>=0:
        build(*args)
    elif ext.find("zip")>=0:
        unzipanim(*args)
    elif ext.find("tex")>=0:
        tex_to_png(*args)
    elif ext.find("png")>=0:
        png_to_tex(*args)