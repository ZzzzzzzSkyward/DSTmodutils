# 饥荒联机版mod制作工具等

本仓库主要包括查看饥荒源文件的一些程序。

## ktools

### BuildRenamer.exe

将一个build.bin的`build`替换成新名字，并删去build.bin尾部的哈希表。

删去尾部不影响游戏，但无法重建成scml工程。

### krane.exe与ktech.exe

原仓库：https://github.com/nsimplex/ktools

用法：

1. tex到png

```bash
ktech atlas-0.tex
ktech atlas-0.tex d:/
```

2. png到tex

```bash
ktech aaa.png
ktech d:/b/c.png e:/f/g/h.tex
```

3. 打印信息

```bash
ktech -i atlas-0.tex
```

4. anim.bin+build.bin+atlas-0.tex到scml文件

```bash
krane anim.bin build.bin output_dir
krane dirin dirout
krane ./ ./
```

推荐用法：两个参数都填动画文件所在文件夹名称

5. 特殊用法：用于修改原图，build.bin到边缘标记的png文件

```bash
krane --mark-atlases build.bin output_dir
```

可能的错误：文件夹里有非英文字符报错。

## 作业：sample_build

里面是官方给的威尔逊scml工程文件。尝试将它打包成build.zip

## 作业：解压缩与转换

在Don't Starve Together\data\anim文件夹里找一个你喜欢的压缩包，先解压，然后用ktech查看图片，再用krane转换成scml文件。

**提示：你有可能发现缺少了什么东西，你可以在别的文件里找找**

## Spriter-4.2

较新版本的Spriter，你还可以在官网（需翻墙）下载未激活的Spriter Pro。个人评价不是很好用。

功能：播放动画、导出帧、导出gif动图、修改build名与bank名

## textool v1.4.2.0

原仓库：https://github.com/zxcvbnm3057/dont-starve-tools

上述ktech的图形化界面。

## DontStarveLUAJIT

由大佬制作的32位引擎补丁，在创意工坊有对应mod

原仓库：https://github.com/paintdream/DontStarveLuaJIT

## steam的Don't Starve Mod Tools

这个工具包拥有上传到创意工坊的功能，还有一个autocompiler.exe

安装后，每次打开饥荒联机版，都会自动调用autocompiler.exe，把位于dont_starve\mods\xxx\的文件打包成另一种格式。

**注意：有些情况下这个工具生成的不是游戏里可用的动画文件，不知道为啥**
