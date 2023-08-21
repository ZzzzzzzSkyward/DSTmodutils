# DS Anim Convert Tools Command Line Usage

The DS Anim Convert Tools script provides a simple command line interface to convert animation file formats.

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

## Dependencies

python3, tested in python3.10

lxml

pillow

matplot

ktech.exe(for Windows only, see `compiler/ktech.py`)

stex.exe(for Windows only, see`compiler/stex.py`)

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

Crop `test.scml` and then generate a `zip`

```shell
python cropscml.py test.scml -crop
```

Convert `images/*.png` to `xml` atlas and `tex`

```shell
python cli.py images/ -xml
```

Extract `test.zip` containing (`anim.bin`,) `build.bin` and `atlas-0.tex` to `test.scml`

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

- the script will try to get attribute `duration` from scml. For example: `<file id="0" name="arm_lower/arm_lower-0.png" duration="2" width="22" height="48" pivot_x="0.568182" pivot_y="0.854167"/>` specifies the duration of `arm_lower-0.png`. This is used especially if you have many images that are identical.

