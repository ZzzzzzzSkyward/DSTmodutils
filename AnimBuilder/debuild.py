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

hashlookup={"81162281":"spider_repellent","2333899264":"dark_nightmare_fuel01","489261827":"snow","4100606808":"smol_tail","758731695":"ripple_shadow","220614720":"fish_mouth","118065854":"headbase_transform","3527666988":"swap_frozen","3356016232":"smol_head","1425581713":"fx_leap_phase","598995423":"superjump_rubble1","2251700669":"splash_pull","3969697825":"brick","3415725241":"fish01","731400221":"FX_fishing","777565744":"card","2639019695":"dark_tendril_white","2776605667":"smol_fin_back","51649127":"snap_fx","1121341095":"hairfront","385272047":"hand","2503680453":"pig_ear","1329092223":"pan_flute01","1725007553":"watchprop_idle","3715622524":"shoal_body","63299517":"page_flip","740660083":"torso","2153311881":"meter","4003765724":"drip_fx","2875087029":"fx_splat","2204993127":"fish_head","2898791583":"fx_droplet","3863927633":"ww_limb","1267459279":"swap_object_bernie","902761014":"swap_boat_hook","3914925069":"boat_wheel_stick","262319454":"book_cook","2887055349":"swap_book_fx_under","344763966":"arm_lower","4126561954":"book_closed","2024622209":"balloon_red","1022376185":"scale_loop","3479742338":"pig_torso","2769822675":"swap_item2","1403170395":"merm_hand","464666431":"back_water","1047036768":"book_open","719922799":"smol_bod","1934262124":"whipline","606217510":"fx_hit","1899249097":"fish_body","2829784663":"hairpigtails","598995425":"superjump_rubble3","1746013835":"SWAP_OBJECT","347554504":"water_shadow","2471749611":"pig_arm","3650222914":"water_ripple_front","3267251723":"boat_wheel_round","598995424":"superjump_rubble2","4240373615":"stab_fx","6691218":"FX","1550269982":"eel_eye","1972479441":"shoal_fin","640136165":"shadow_hands","2591147848":"sprk_1","1162055856":"tail","699295155":"skirt","3885869108":"fan01","2121288935":"splash","898868142":"leg","2179895191":"swap_book_fx_over","111721250":"body","2838898737":"STRING","3083483767":"wrap_paper","3278855924":"FX_wipe","558723846":"wrap_string","3632444306":"swap_bedroll","1341564572":"prop_poop","1019583295":"wood_splinter","3839468699":"flower","881434974":"hair_hat","1758329841":"pig_head","3126759360":"torso_transform","2561773373":"pig_leg","3281870581":"torso_pelvis","2883727546":"scale_wrist","2978046506":"scale","3344386951":"fx_lunge_streak","3279052732":"fx_wisp","568008419":"spiralfx","752575235":"smol_fin","1557481912":"eel_fin","2293956612":"machine_rope_comp","1177345894":"cbell","3292370103":"lantern_overlay","2101183731":"eel_head","3721226251":"face_monkeyparts","1111815181":"headbase_hat","3369598559":"ww_shadow","2473642807":"swap_pocket_scale_arrow","1315521930":"FX halo","1113909454":"superjump_spear_fx","2487757449":"superjump_smokering","2949583703":"fish_tail","2151100926":"dark_center","1864876520":"superjump_groundlift","2536163490":"eyes","3238147685":"dark_tendril_black","1562828166":"board","4278182943":"swap_item","2331007291":"swap_shock_fx","3872412870":"hit_2","2845774307":"eel_tail","2656306483":"fx_star_part","1871061916":"Smear new","271157747":"arm_lower_cuff","1442575526":"woodenarm","3578374980":"fish_fin","2235966017":"splode","827288350":"shadow_ball","2912836022":"rope_joints","1068524485":"superjump_speedline","948174794":"ray","1857896239":"tear_fx","1683025819":"swap_goo","3251382164":"ww_torso","2304494351":"razor01","2839857689":"ww_meathand","1027103032":"hound_whistle01","2242699715":"prop_mug","1993330418":"boat_part","2794168603":"hand_idle_wormwood","707745631":"ww_head","3067666734":"swap_body","2881891899":"wheel","4211082272":"glow_2","381158205":"sprks","3095906253":"cheeks","2904107377":"headbase","880408248":"dark_burst01","4164613600":"fx_bubb","3074764298":"swap_boat_net","2346890768":"beard","3427202812":"wendy_idle_flower","2892157090":"slackrope","2861269034":"emotefx","3234791630":"foot","4021366554":"shoal_head","2574210267":"giftbox","1795439701":"eel_body","2838770366":"FX_webber_wipe","2851071397":"meter_color2","11524681":"FX_liquid","2770205278":"prop_carolbook","3118343357":"face","2230047924":"FX_splash","2733664639":"ARM_upper","3571163050":"fish_eye","419160814":"fx_large","1503094397":"superjump_groundcrack","528309380":"bell01","213878485":"fx_spit","1318562590":"swap_body_tall","1779321545":"swap_face","557606594":"hand_wickerbottom","384944066":"HAIR","2599363604":"swap_pocket_scale_body","1836671383":"water","1676172676":"horn01","445246256":"warly_inhale_fx","2371334557":"arm_upper_skin","3540207685":"legs","953935066":"wooden_circles","150504261":"dark_squigle","4286819824":"wheelshine","910185848":"dark_spew","4010956263":"swap_goosplat","1690368943":"swap_hat","2694334675":"platform","2902804558":"prop_rope","956463774":"fishingline"}
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
    len_hashcollection=0
    try:
        len_hashcollection = struct.unpack(endianstring + 'I', infile.read(4))[0]
    except Exception as e:
        print("cannot read byte",infile.tell())
        print(e)

    hashcollection = {}

    for index in range(len_hashcollection):
        hash_idx = struct.unpack(endianstring + 'I', infile.read(4))[0]
        len_name = struct.unpack(endianstring + 'i', infile.read(4))[0]
        name = struct.unpack(endianstring + str(len_name) + 's', infile.read(len_name))[0]
        hashcollection[hash_idx]=name

    symbols = root_node.getElementsByTagName("Symbol")

    #检索hash并替换
    for isymbol in symbols:
        symbol_name=str(isymbol.getAttribute("name"))
        hashid = int(symbol_name)
        try:
            symbol_name = hashcollection[hashid] if (hashid in hashcollection) else hashlookup[symbol_name]
        except:
            print(symbol_name,"missing")
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