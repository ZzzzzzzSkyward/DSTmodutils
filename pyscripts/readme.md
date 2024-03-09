# DS Anim Convert Tools Command Line Usage

The DS Anim Convert Tools script provides a simple command line interface to convert animation file formats.

[中文说明在这里](./readme_zh.md)

## Bug Fix

- Remove the interpolation function, which may cause unwanted results. You need to manually key each frame. Or you can use the experimental interpolation service provided.
- Fix krane wrongly interpreting the size of an image if it is too empty.
- Fix krane losing `layername` when converting an `anim.bin`.
- Fix autocompiler messing up with fps (somehow it is fixed to 40fps, but all animations in DS run in 30fps).

## Usage

```shell
python cli.py filename [parameters]
```

parameters are recognized in the form of `-key=value`.

`-build` tells that the input is a build, `-anim` an anim.

## Dependencies

python3, tested in python3.10. Versions lower than 3.10 will result in some grammar error, you may want to fix them yourself.

lxml

pillow

ktech.exe(for Windows only, see `compiler/ktech.py`)

stex.exe(for Windows only, see `compiler/stex.py`)

ztools.exe(for Windows only, see `compiler/ztools.py`)

`stex` is preferred. Use `-ktech`, `-ztools` to tell which program to use. Platform other than Windows may want to compile their own executables. 

## Example commands

Rename the `build.bin` from `ds_pig.zip` from `pigman` to `newbuild`

```shell
python cli.py build.bin -rename=newbuild
```

Convert `build.xml` to `build.bin`

```shell
python cli.py build.xml
```

Convert `anim.bin` to `anim.xml`, or `anim.json` with `-json`

```shell
python cli.py anim.bin
```

Interpolate keyframes in `test.scon`. This is only for continuous animation with a keyframe at the beginning. If an animation is not valid, it will be skipped.

```shell
python cli.py test.scon -interpolate
```

Crop `test.scml`

```shell
python cropscml.py test.scml
```

Convert `images/*.png` to `xml` atlas and `tex`

```shell
python cli.py images/ -xml
```

Extract `test.zip` containing (`anim.bin`,) `build.bin` and `atlas-0.tex` to `test.scml`. Add `-json` to generate `anim.json` and `build.json` by the way.

```shell
python cli.py test.zip
```

Compile `test.scml` after cropping

```shell
python cli.py test.scml -crop
```

Extract (`anim.bin`,) `build.bin` and `atlas-0.tex` in a folder `test/`

```shell
python cli.py test/
```

Extract `test.xml` and `test.tex` to a folder of images

```shell
python cli.py test.xml
```

Compile `build.bin` and `atlas-0.tex` given a `build.bin` and some image folders in `test/`. This is only used for reskinning if you don't need your own `anim.bin` and just want to change the images extracted from an official build. You are not allow to resize images here.

```shell
python cli.py build.bin test/
```

## Extra Parameters

### Compiling Scml

- The script will try to get attribute `duration` from scml. For example: `<file id="0" name="arm_lower/arm_lower-0.png" duration="2" width="22" height="48" pivot_x="0.568182" pivot_y="0.854167"/>` specifies the duration of `arm_lower-0.png`. This is used especially if you have many images that are identical.

### Handling build.json

1. handle build.json

   - run `python cli.py build.json -crop`
   - input: a `build.json`
   - An extra attribute `Path` is added to json. If there is a `Path` in `build.json`, it implies that the images are located there, otherwise the images are assumed to be located exactly the same as `build.json`.
   - By default, it will only try to fix the width and height mismatch, according to images.
   - parameters after `-crop`:
     - `-check` displays the mismatch without actually modifying the json file.
     - `-remove_vert`removes the `Verts` attribute, which is useless. The `Verts` will be calculated again according to images in that folder.
     - `-compensate` try to adjust the `x` and `y` attribute, given `width` and `height` being wrong. If you use the Animation Viewer(`html/index.html`), you are supposed to do this. If you don't add this parameter, and you have an image that has wrong recorded shape, the `x` and `y` will remain the same, which results in a shift of pivot.
     - `-clip` try to clip images (please do a backup yourself!), removing the blank space around an image to shrink the size.
   - Please be careful when you use these things as they may cause unwanted results.

2. compile build.json and images

   -  run `python cli.py build.json path_to_image_folder/`.

   - output: a zip including `build.bin` and `atlas-0.tex`.

### Handling anim.json

- It is often the case when you don't want to change an item's anim, but just want to change its texture. Since you can compile the build, you can also compile its animation. If your texture is not too different from the original texture in shape, you can just leave the animation alone, and use the original animation file. And you use it by calling `inst.AnimState:SetBank("the original bank")`
- But if the shape is different enough, you need to compile a new animation file.
  1. rename the bank name in `anim.json`.
  2. run `python cli.py anim.json -crop=build.json`, the images are read from either `Path` attribute or the same directory as build.json.
  3. run `python cli.py anim.json` to get an `anim.bin`.
  4. insert it into the zip.
