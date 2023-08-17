# DS Anim Convert Tools Command Line Usage

The DS Anim Convert Tools script provides a simple command line interface to convert animation file formats.

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

opencv

ktech.exe

stex.exe

## Example commands

Rename the `build.bin` from `ds_pig.zip` from `pigman` to `newbuild`

```shell
python cli.py build.bin -rename=newbuild
```

Convert `build.xml` to `build.bin`

```shell
python cli.py build.xml
```

Convert `anim.bin` to `anim.xml`

```shell
python cli.py anim.bin
```

Interpolate keyframes in `test.scon`. This is only for continuous animation with a keyframe at the beginning. If an animation is not valid, it will be skipped.

```shell
python cli.py test.scon -interpolate
```

Crop `test.scml`

```shell
python cli.py test.scml -crop
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

