# DS动画转换工具命令行用法

DS Anim Convert Tools脚本提供简单的命令行接口来转换动画文件格式。

##  Bug 修复

- 移除插值函数,该函数可能会导致不想要的结果。您需要手动为每一帧设置关键帧。或者您可以使用实验性插值服务。
- 修复krane错误地解释空图像的大小。  
- 修复krane在转换`anim.bin`时丢失`layername`。
- 修复自动编译出错,fps被设置成40fps,但DS中的所有动画都是30fps。

## 使用方法

```shell
python cli.py 文件名 [参数]
```

参数采用`-键=值`的形式识别。

`-build`表示输入是一个构建文件,`-anim`表示一个动画文件。

## 依赖项

Python3,已在Python3.10中测试。低于3.10的版本可能会出现一些语法错误,您可以自行修复。

lxml

pillow

ktech.exe(仅适用于Windows,参考`compiler/ktech.py`)

stex.exe(仅适用于Windows,参考`compiler/stex.py`)  

ztools.exe(仅适用于Windows,参考`compiler/ztools.py`)

推荐使用`stex`。使用`-ktech`,-`ztools`指定使用哪个程序。非Windows平台可能需要自己编译可执行文件。

## 示例命令

将`ds_pig.zip`中的`build.bin`从`pigman`重命名为`newbuild`

```shell
python cli.py build.bin -rename=newbuild
```

将`build.xml`转换为`build.bin`

```shell 
python cli.py build.xml
```

将`anim.bin`转换为`anim.xml`,或使用`-json`参数生成`anim.json`

```shell
python cli.py anim.bin
```

对`test.scon`中的关键帧进行插值。这只适用于从开始就含有关键帧的连续动画。如果动画无效就会跳过。

```shell
python cli.py test.scon -interpolate
```

裁剪`test.scml`

```shell
python cropscml.py test.scml
```

将`images/*.png`转换为`xml`图集和`tex`贴图

```shell
python cli.py images/ -xml
```

从`test.zip`提取(`anim.bin`,)`build.bin`和`atlas-0.tex`到`test.scml`。使用`-json`参数同时生成`anim.json`和`build.json`。

```shell
python cli.py test.zip
```

裁剪后的`test.scml`编译

```shell 
python cli.py test.scml -crop
```

从文件夹`test/`提取(`anim.bin`,)`build.bin`和`atlas-0.tex`

```shell
python cli.py test/
```

将`test.xml`和`test.tex`提取到图片文件夹

```shell
python cli.py test.xml
```

给定`build.bin`和一些图片文件夹`test/`,编译`build.bin`和`atlas-0.tex`。仅用于更换皮肤,不需要自己的`anim.bin`,只想改变官方构建中的图片。这里不允许调整图片大小。

```shell
python cli.py build.bin test/  
```

## 额外参数

### 编译Scml

- 脚本将从scml尝试获取属性`duration`。例如:`<file id="0" name="arm_lower/arm_lower-0.png" duration="2" width="22" height="48" pivot_x="0.568182" pivot_y="0.854167"/>` 指定`arm_lower-0.png`的持续时间。这对于有许多相同图像的时候特别有用。

### 处理build.json

1. 处理build.json

   - 运行`python cli.py build.json -crop`

   - 输入:一个`build.json`

   - 如果`build.json`中含有`Path`属性,它表示图像位于该路径下,否则假设图像与`build.json`完全相同。

   - 默认只根据图片修正宽高不匹配。

   - `-crop`后的参数:
     - `-check`显示不匹配而不实际修改json文件
     
     - `-remove_vert`删除无用的`Verts`属性
     
     - `-compensate`给定宽高错误,尝试调整`x`和`y`属性。需要这一参数如果使用动画查看器(`html/index.html`)
     
     - `-clip`尝试剪裁图片(请自行备份),去除周围空白缩小尺寸。
     
   - 请小心使用这些操作,可能导致不良结果。
   
2. 编译build.json和图片

   - 运行 `python cli.py build.json 图片文件夹路径/`

   - 输出:包含`build.bin`和`atlas-0.tex`的zip包。

### 处理anim.json 

- 很常见的是不想改变物体的动画,只想改变其纹理。由于可以编译build,也可以编译其动画。如果新纹理形状与原始纹理相近,可以直接使用原始动画文件。使用`inst.AnimState:SetBank("原始动画名")`

- 如果形状不同足以影响,需要编译新的动画文件:

  1. 在`anim.json`中改动动画库名称

  2. 运行`python cli.py anim.json -crop=build.json`,图片从`Path`属性或`build.json`同目录读取

  3. 运行`python cli.py anim.json`获取`anim.bin`

  4. 插入zip中