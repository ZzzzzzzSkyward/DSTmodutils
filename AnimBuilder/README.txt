1.反编译bin为xml
1.1Fa鸽的animd.exe
animd /in indir /out outdir
indir存放anim.bin与build.bin
(缺少image属性）
1.2勿言的脚本
py2 deanim.py anim.bin
py2 debuild.py build.bin
py2是Don't Starve Mod Tools自带的python.exe
（反编译出的build.bin.xml缺少atlas，build名多了一个.scml后缀，格式与官方一致）
2.编译xml为bin
2.1Fa鸽的animc.exe
animc /anim anim.xml /build build.xml /out outdir
2.2勿言的enanim.py
py2 enanim.py anim.xml
2.3自带的buildanimation.py
py2 /tools/scripts/buildanimation.py ...