import argparse, shutil
import re
import struct
import traceback
import xml.dom.minidom
import math
import os
import sys
import Image
from clint.textui import progress
import tempfile
import re
import gc
from StringIO import StringIO
from io import BytesIO
from collections import namedtuple

BUILDVERSION = 6

#BUILD format 6
# 'BILD'
# Version (int)
# total symbols;
# total frames;
# build name (int, string)
# num materials
#   material texture name (int, string)
#for each symbol:
#   symbol hash (int)
#   num frames (int)
#       frame num (int)
#       frame duration (int)
#       bbox x,y,w,h (floats)
#       vb start index (int)
#       num verts (int)

# num vertices (int)
#   x,y,z,u,v,w (all floats)
#
# num hashed strings (int)
#   hash (int)
#   original string (int, string)


def ExportBuild(endianstring,build,font):
    infile = BytesIO(build)
    
    buffer = infile.read(8)
    
    print(struct.unpack(endianstring + 'cccci',buffer))
    
    symbol_num = struct.unpack(endianstring + 'I',infile.read(4))[0]
    frame_num = struct.unpack(endianstring + 'I',infile.read(4))[0]
    buildnamelen =  struct.unpack(endianstring + 'i',infile.read(4))[0]
    buildname = struct.unpack(endianstring + str(buildnamelen) + 's',infile.read(buildnamelen))[0]
    atlaseslen = struct.unpack(endianstring + 'I', infile.read(4))[0]
    
    print("symbol num:",symbol_num)
    print("frame num:",frame_num)
    print("build name:",buildname)
    
    lists=[] #  atlasdata = atlases[ atlas_idx ] mip = atlasdata.mips[0]  name = mip.name + ".tex"
    
    for atlas_idx in range( atlaseslen ):
        namelen = struct.unpack(endianstring + 'i' ,infile.read(4))[0]
        name = struct.unpack(endianstring + str(namelen) + 's' ,infile.read(namelen))[0]
        lists.append(name)
    
    print("atlas:",lists)
    
    dom=xml.dom.minidom.Document()
    #创建根节点
    root_node=dom.createElement('Build')
    
    root_node.attributes['name']=buildname+'.scml'
    dom.appendChild(root_node)
    
    for symbol_id in range(symbol_num):
        symbol = dom.createElement('Symbol')
        hash = struct.unpack(endianstring + 'I', infile.read(4))[0]
        symbol.attributes['name']=str(hash) #hash后续进行替换
        framecount = struct.unpack(endianstring + 'I', infile.read(4))[0]
        
        root_node.appendChild(symbol)
        for idx in range( framecount ):
            framenum = struct.unpack(endianstring + 'I', infile.read(4))[0]
            duration = struct.unpack(endianstring + 'I', infile.read(4))[0]
            xywh = struct.unpack(endianstring + 'ffff', infile.read(16))
            alphaidx = struct.unpack(endianstring + 'I', infile.read(4))[0]
            alphacount = struct.unpack(endianstring + 'I', infile.read(4))[0]
            
            frame = dom.createElement('Frame')
            frame.attributes["image"] = '???' #先占个位，后续补全
            frame.attributes["framenum"] = str(framenum)
            frame.attributes["duration"] = str(duration)
            frame.attributes["x"] = str(xywh[0])
            frame.attributes["y"] = str(xywh[1])
            frame.attributes["w"] = str(xywh[2])
            frame.attributes["h"] = str(xywh[3])
            # frame.attributes["alphaidx"] = str(alphaidx)
            # frame.attributes["alphacount"] = str(alphacount)
            symbol.appendChild(frame)
            
    len_alphaverts = struct.unpack(endianstring + 'I', infile.read(4))[0]
    
    for i in range(len_alphaverts):
        xyzuvw = struct.unpack(endianstring + 'ffffff', infile.read(24))

    len_hashcollection = struct.unpack(endianstring + 'I', infile.read(4))[0]

    hashcollection = {}

    for index in range(len_hashcollection):
        hash_idx = struct.unpack(endianstring + 'I', infile.read(4))[0]
        len_name = struct.unpack(endianstring + 'i', infile.read(4))[0]
        name = struct.unpack(endianstring + str(len_name) + 's', infile.read(len_name))[0]
        hashcollection[hash_idx]=name

    symbols = root_node.getElementsByTagName("Symbol")
    
    #检索hash并替换
    for isymbol in symbols:
        hashid = int(str(isymbol.getAttribute("name")))
        symbol_name = hashcollection[hashid]
        isymbol.setAttribute("name",symbol_name)

        frames = isymbol.getElementsByTagName("Frame")
        idx = 0
        for iframe in frames:
            iframe.setAttribute("image",symbol_name+'-'+str(idx))
            idx = idx+1

    
    root_node.writexml(fout,indent='',addindent='\t',newl='\n')
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='decode .xml file from build.bin.')
    parser.add_argument('infile', action="store")

    results = parser.parse_args()
    results.ignoreexceptions  = 0
    try:
        endianstring = "<"
        path, base_name = os.path.split(results.infile)
        f = open(results.infile,'rb')
        build = f.read()
        f.close()
        outfilename = results.infile+ ".xml"
        fout = open(outfilename, "wb")
        ExportBuild(endianstring, build, fout)
        fout.close()
        
        #下面这一溜照抄官方的，不知道干啥的，也不必知道
        if not results.ignoreexceptions:
            try:
                import pysvn
                client = pysvn.Client()            
                client.add( outfilename )
            except:
                pass

            try:
                client = pysvn.Client()
                client.add_to_changelist( outfilename, 'Export ' + base_name)
            except:
                pass
    except: # catch *all* exceptions
        e = sys.exc_info()[1]
        sys.stderr.write( "Error Exporting {}\n".format(results.infile) + str(e) )
        traceback.print_exc(file=sys.stderr)
        if not results.ignoreexceptions:
            #raw_input("There was an export error!\n") # uncomment this to stop the execution when this breaks
            exit(-1)