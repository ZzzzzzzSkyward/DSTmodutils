import argparse, shutil
import re
import struct
import traceback
import xml.dom.minidom
import math
import os
import sys
#import Image
#from clint.textui import progress
import tempfile
import re
import gc
#from StringIO import StringIO
from io import BytesIO
from collections import namedtuple

ZIP_ZERO_TIME = ( 1980, 0, 0, 0, 0, 0 )
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

ANIMVERSION = 4
#ANIM format 4
# 'ANIM'
# Version (int)
# total num element refs (int)
# total num frames (int)
# total num events (int)
# Numanims (int)
#   animname (int, string)
#   validfacings (byte bit mask) (xxxx dlur)
#   rootsymbolhash int
#   frame rate (float)
#   num frames (int)
#       x, y, w, h : (all floats)
#       num events(int)
#           event hash
#       num elements(int)
#           symbol hash (int)
#           symbol frame (int)
#           folder hash (int)
#           mat a, b, c, d, tx, ty, tz: (all floats)
#
# num hashed strings (int)
#   hash (int)
#   original string (int, string)
FACING_RIGHT = 1<<0
FACING_UP = 1<<1
FACING_LEFT = 1<<2
FACING_DOWN = 1<<3
FACING_UPRIGHT = 1<<4
FACING_UPLEFT = 1<<5
FACING_DOWNRIGHT = 1<<6
FACING_DOWNLEFT = 1<<7


def strhash(str, hashcollection):
    hash = 0
    for c in str:
        v = ord(c.lower())
        hash = (v + (hash << 6) + (hash << 16) - hash) & 0xFFFFFFFF
    hashcollection[hash] = str
    return hash

def ExportAnim(endianstring, anim, outfile, ignore_exceptions):
    hashcollection = {}
    infile = BytesIO(anim)
    
    buffer = infile.read(8)
    print(struct.unpack(endianstring + 'cccci',buffer))
    elements = struct.unpack(endianstring + 'I',infile.read(4))[0]
    frames = struct.unpack(endianstring + 'I',infile.read(4))[0]
    events = struct.unpack(endianstring + 'I',infile.read(4))[0]
    anims = struct.unpack(endianstring + 'I',infile.read(4))[0]
    print( elements ,frames ,events,anims)
    dir = ("_up","_down", "_side","_left","_right","_upside","_downside","_upleft","_upright","_downleft","_downright","_45s","_90s")
    #xml组装
    dom=xml.dom.minidom.Document()
    #创建根节点
    root_node=dom.createElement('Anims')
    dom.appendChild(root_node)
    #循环读取 node 
    #anims[0] = 1
    if anims > 0:
        for i in range(0,anims):
            anim_node = dom.createElement('anim')
            root_node.appendChild(anim_node)
            #名称长度
            namelen = struct.unpack(endianstring+"i",infile.read(4))[0]
            #print( str(namelen[0]),  namelen[0] )
            name = struct.unpack(endianstring+str(namelen)+"s",infile.read(namelen))[0]
            #print(name)
            #表情类型？？？
            facingtype = struct.unpack(endianstring+"B",infile.read(1))[0]
            if facingtype == FACING_UP:
                name = name+dir[0]
            elif facingtype == FACING_DOWN:
                name = name+dir[1]
            elif facingtype == FACING_LEFT | FACING_RIGHT:
                name = name+dir[2]
            elif facingtype == FACING_LEFT:
                name = name+dir[3]
            elif facingtype == FACING_RIGHT:
                name = name+dir[4]
            elif facingtype == FACING_UPLEFT | FACING_UPRIGHT:
                name = name+dir[5]
            elif facingtype == FACING_DOWNLEFT | FACING_DOWNRIGHT:
                name = name+dir[6]
            elif facingtype == FACING_UPLEFT:
                name = name+dir[7]
            elif facingtype == FACING_UPRIGHT:
                name = name+dir[8]
            elif facingtype == FACING_DOWNLEFT:
                name = name+dir[9]
            elif facingtype == FACING_DOWNRIGHT:
                name = name+dir[10]
            elif facingtype == FACING_UPLEFT | FACING_UPRIGHT | FACING_DOWNLEFT | FACING_DOWNRIGHT:
                name = name+dir[11]
            elif facingtype == FACING_UP | FACING_DOWN | FACING_LEFT | FACING_RIGHT:
                name = name+dir[12]
            anim_node.setAttribute('name',name)
            #hash？暂时不管
            hash = struct.unpack(endianstring+"I",infile.read(4))[0]
            frame_rate = struct.unpack(endianstring+"f",infile.read(4))[0]
            frames_num = struct.unpack(endianstring+"I",infile.read(4))[0]
            anim_node.setAttribute("root",str(hash))
            anim_node.setAttribute("framerate",str(int(frame_rate)))
            anim_node.setAttribute("numframes",str(int(frames_num)))
            #解析frame
            if frames_num > 0:
                for iframe in range(0,frames_num):
                    frame_node = dom.createElement('frame')
                    anim_node.appendChild(frame_node)
                    x,y,w,h=struct.unpack(endianstring+"ffff",infile.read(16))
                    frame_node.setAttribute("w",str(w))
                    frame_node.setAttribute("h",str(h))
                    frame_node.setAttribute("x",str(x))
                    frame_node.setAttribute("y",str(y))
                    #解析events
                    #print(i,iframe,x,y,w,h)
                    num_events = struct.unpack(endianstring+"I",infile.read(4))[0]
                    #num_events = 0
                    if num_events >0 :
                        #print(i,iframe,num_events)
                        for ievent in range(0,num_events):
                            #print(i,iframe,ievent)
                            event_node = dom.createElement('event')
                            frame_node.appendChild(event_node)
                            namehash = struct.unpack(endianstring+"I",infile.read(4))[0]
                            event_node.setAttribute("name",str(namehash))
                        #解析elements
                    num_elements = struct.unpack(endianstring+"I",infile.read(4))[0]
                    if num_elements >0 :
                        for ielements in range(0,num_elements):
                            elements_node = dom.createElement('element')
                            frame_node.appendChild(elements_node)
                            namehash = struct.unpack(endianstring+"I",infile.read(4))[0]
                            frameint = struct.unpack(endianstring+"I",infile.read(4))[0]
                            layernamehash = struct.unpack(endianstring+"I",infile.read(4))[0]
                            m_a,m_b,m_c,m_d,m_tx,m_ty,z = struct.unpack(endianstring+"fffffff",infile.read(28))
                            #print(namehash)
                            elements_node.setAttribute("name",str(namehash))
                            elements_node.setAttribute("layername",str(layernamehash))
                            elements_node.setAttribute("frame",str(frameint))
                            elements_node.setAttribute("z_index",str(15+ielements))
                            elements_node.setAttribute("m_a",str(m_a))
                            elements_node.setAttribute("m_b",str(m_b))
                            elements_node.setAttribute("m_c",str(m_c))
                            elements_node.setAttribute("m_d",str(m_d))
                            elements_node.setAttribute("m_tx",str(m_tx))
                            elements_node.setAttribute("m_ty",str(m_ty))
    
    #读取hash
    hashs = struct.unpack(endianstring + 'I',infile.read(4))[0]
    for ihash in range(0,hashs):
        hashid,hashlen = struct.unpack(endianstring + 'Ii', infile.read(8))
        hashstr = struct.unpack(endianstring + str(hashlen)+'s', infile.read(hashlen))[0]
        hashcollection[hashid] = hashstr
    #print(hashcollection)
    nodes = root_node.getElementsByTagName("anim")
    
    #检索hash并替换
    for inode in nodes:
        hashid = int(str(inode.getAttribute("root")))
        inode.setAttribute("root",hashcollection[hashid])
        frames = inode.getElementsByTagName("frame")
        for iframe in frames:
            events = iframe.getElementsByTagName("event")
            for ievent in events:
                ievent.setAttribute("name",str(hashcollection[int(ievent.getAttribute("name"))]))
            elements = iframe.getElementsByTagName("element")
            for ielement in elements:
                hashid = int(str(ielement.getAttribute("name")))
                ielement.setAttribute("name",hashcollection[hashid])
                hashid = int(str(ielement.getAttribute("layername")))
                ielement.setAttribute("layername",hashcollection[hashid])
    #写出文件
    #print(dom.toxml())
    root_node.writexml(outfile,indent='',addindent='\t',newl='\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='decode .xml file from anim.bin.')
    parser.add_argument('infile', action="store")

    results = parser.parse_args()
    results.ignoreexceptions  = 0
    try:
        endianstring = "<"
        path, base_name = os.path.split(results.infile)
        f = open(results.infile,'rb')
        anim = f.read()
        f.close()
        outfilename = results.infile+ ".xml"
        fout = open(outfilename, "wb")
        ExportAnim(endianstring, anim, fout,0)
        fout.close()

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


