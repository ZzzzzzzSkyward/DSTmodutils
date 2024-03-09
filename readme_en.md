# DST Modding Tools and Utilities

This repository contains various programs and tools for viewing Don't Starve Together source files and modding assets. 

## ktools

### BuildRenamer.exe

Renames a build.bin's "build" name and removes the symbol table from the end of the build.bin file. 

Removing the symbol table does not affect gameplay.

### krane.exe and ktech.exe 

Origins: https://github.com/nsimplex/ktools 

Fork used: https://github.com/dstmodders/ktools

Usage:

1. Convert tex to png:

```bash
ktech atlas-0.tex
ktech atlas-0.tex d:/
```

2. Convert png to tex:  

```bash 
ktech aaa.png
ktech d:/b/c.png e:/f/g/h.tex
```

3. Print information:

```bash
ktech -i atlas-0.tex
```

4. Convert anim.bin, build.bin, atlas-0.tex to scml file:

```bash
krane anim.bin build.bin output_dir
krane dirin dirout  
krane ./ ./
```

Recommended usage: Specify both parameters as the animation file folder name

5. Special usage: Used to generate edge marked png files from a build.bin: 

```bash
krane --mark-atlases build.bin output_dir
```

6. Simultaneously generate xml files:

```bash 
ktech icon.png --atlas modicon.xml
```

Generates modicon.xml and modicon.tex

Potential errors: Issues with non-English characters in folders.

## sample_build example

Contains an official Wilson scml project file. Try packing it into a build.zip

## Unpacking and conversion example

Find a favorite packed animation folder from DontStarveTogether\data\anim, unpack it, view images with ktech, and convert to scml with krane.  

**Tip: You may find things missing - search other files**

## Spriter-4.2

A newer version of Spriter. The Spriter Pro version can also be downloaded (requires VPN) from their website. Personal opinion is it's not very user friendly.  

Functions: Play animations, export frames, export gif, rename build and bank.

## Spriter r11 

The newest version of Spriter Pro.  

Activation codes: 

spriter@spk.stw           SPLK-BUIJ-0ZYY-NQ74
TheBlade@Pirates.gov      BLAD-C0P6-0T8D-K8XU

## textool v1.4.2.0

Origins: https://github.com/zxcvbnm3057/dont-starve-tools 

Fork used: https://github.com/oblivioncth/dont-starve-tools

Used to view tex files.

## (DontStarveLUAJIT)

A 32-bit engine patch created by a skilled modder, with a corresponding mod on the Klei Creative Forum. 

Origins: https://github.com/paintdream/DontStarveLuaJIT

There is also a 64-bit patch.

## Steam Don't Starve Mod Tools

This tool package has Workshop uploading functionality as well as an autocompiler.exe. 

When Don't Starve Together is opened after installing, it will automatically call autocompiler.exe on files located in dont_starve\mods\xxx\.

**Note: In some cases this tool does not generate gameplay compatible animation files, unknown why.**

Known bugs:

1. Source: https://forums.kleientertainment.com/forums/topic/72067-autocompiler-symbol-issues/?tab=comments#comment-842755 

Don't Starve Mod Tools/mod_tools/tools/scripts/buildanimation.py:163 (line number may have changed)

```python
layername = element_node.attributes["layername"].value.encode('ascii').split('/')[-1]
Should be:
layername = element_node.attributes["name"].value.encode('ascii').split('/')[-1]
```

2. Disappearing symbols incorrectly reappear on non-looping animations (need to manually set looping=false or disable looping in Spriter)

3. Image interactable area does not match actual non-transparent pixel area, causing selection issues in-game 

## DS Tool

https://github.com/Jerry457/ds_tool

Fixes some bugs in autocompiler.exe

## AnimBuilder 

This folder contains two sets of programs.  

The first: enanim.py compiles anim.xml, deanim.py decompiles anim.bin. debuild.py decompiles build.bin. Uses mod tools included tools/scripts/buildanimation.py to compile build.xml.

The second: animc.exe compiles anim.xml and build.xml, animd.exe decompiles anim.bin and build.bin.

The first set of programs comes from @勿言 (Five Years of Don't Starve Mod Making). 

The second set comes from @Fa鸽 https://github.com/Akarinnnnn/KleiAnim

```bash
animc /anim anim.xml /build build.xml /out outdir  
animd /in inputdir /out outputdir
```

```bash
py2 enanim.py 
@py2 refers to Don't Starve Mod Tools
```

## Resources used

Klei forums modding tools section: https://forums.kleientertainment.com/files/category/5-modding-tools-tutorials-examples/

Github, Gitlab repositories