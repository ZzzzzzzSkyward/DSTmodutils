'''
这个是命令行程序
'''
import os
import sys
sys.path.append("compiler")


def main():
    require()
    args = parse()
    if len(args) == 0:
        help()
        return
    filename = args[0]
    if filename == "":
        help()
        return
    work(args)


def work(args):
    fn = None
    filepath, filename, file_ext = split_all(args[0])
    if len(args) == 1:
        if file_ext == "bin" and filename == "build":
            # build.bin->build.xml
            fn = convert_build_bin
        if file_ext == "xml" and filename == "build":
            # build.xml->build.bin
            fn = convert_build_xml
        if file_ext == "xml" and filename == "anim":
            # anim.xml->anim.bin
            fn = convert_anim_xml
        if file_ext == "bin" and filename == "anim":
            # anim.bin->anim.xml
            fn = convert_anim_bin
        if file_ext == "scml":
            # *.scml->*.zip
            fn = convert_scml_scml
        if file_ext == "zip":
            # *.zip->*.scml
            fn = convert_scml_zip
        if file_ext == "tex":
            # *.tex->*.png
            fn = convert_image_tex
        if file_ext in image_exts:
            # image->tex
            fn = convert_image_png
        if not file_ext:
            filedir = os.path.join(filepath, filename)
            if os.path.isdir(filedir):
                # check if it is a scml project
                filelist = os.listdir(filedir)
                scmllist = [i for i in filelist if i.endswith(".scml")]
                imagelist = [i for i in filelist if i.endswith('.png')]
                if len(scmllist) > 0:
                    filedir, filename, file_ext = split_all(
                        os.path.join(filedir, scmllist[0]))
                    fn = convert_scml_scml
                # check if it is a bunch of images
                elif len(imagelist) > 0:
                    pass

    if len(args) == 2:
        filepath1, filename1, file_ext1 = split_all(args[1])
        if file_ext == "png" and args[1].find("xml") >= 0:
            # png->xml&tex
            print("这条命令忽略输入的xml路径")
            fn = convert_image_png_atlas
    if fn:
        fn(filepath, filename, file_ext)
    else:
        print(unrecognized_file)


def help():
    print(helptext)


def parse():
    args = sys.argv[1:]
    return args


def split_all(filename):
    path, file = os.path.split(filename)
    file, ext = os.path.splitext(file)
    ext = ext.strip('.')
    return path, file, ext


def join_all(dir, name, ext):
    file = name + "." + ext
    return os.path.join(dir, file)


def convert_build_bin(filepath, filename, file_ext):
    from buildtoxml import BuildToXml
    output_ext = "xml"
    BuildToXml(
        join_all(filepath, filename, file_ext),
        join_all(filepath, filename, output_ext),
    )


def convert_build_xml(filepath, filename, file_ext):
    from xmltobuild import XmlToBuild
    output_ext = "bin"
    XmlToBuild(
        join_all(filepath, filename, file_ext),
        join_all(filepath, filename, output_ext),
    )


def convert_anim_xml(filepath, filename, file_ext):
    from xmltoanim import XmlToAnim
    output_ext = "bin"
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, output_ext)
    input_string = None
    with open(input_path, 'r') as input_file:
        input_string = input_file.read()
    with open(output_path, 'wb') as output_file:
        XmlToAnim(
            input_string, output_file
        )


def convert_anim_bin(filepath, filename, file_ext):
    from animtoxml import AnimToXml
    output_ext = "xml"
    output_path = join_all(filepath, filename, output_ext)
    input_path = join_all(filepath, filename, file_ext)
    input_bytes = None
    with open(input_path, 'rb') as f:
        input_bytes = f.read()
    output_string = AnimToXml(input_bytes)
    with open(output_path, 'wb') as output_file:
        output_file.write(output_string)


def convert_to_png(filepath, filename, file_ext):
    from PIL import Image
    image_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "png")
    image = Image.open(image_path)
    image.save(output_path, "png")


def convert_image_png(filepath, filename, file_ext):
    if file_ext != "png":
        convert_to_png(filepath, filename, file_ext)
        file_ext = "png"
    from compiler.ktech import png_to_tex
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "tex")
    errmsg = png_to_tex(input_path, output_path)
    if errmsg:
        print(errmsg)


def convert_image_png_atlas(filepath, filename, file_ext):
    if file_ext != "png":
        convert_to_png(filepath, filename, file_ext)
        file_ext = "png"
    from compiler.ktech import png_to_tex
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "tex")
    atlas_path = join_all(filepath, filename, "xml")
    errmsg = png_to_tex(input_path, output_path, atlas_path)
    if errmsg:
        print(errmsg)


def convert_image_tex(filepath, filename, file_ext):
    from compiler.ktech import tex_to_png
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "png")
    errmsg = tex_to_png(input_path, output_path)
    if errmsg:
        print(errmsg)


def convert_scml_scml(filepath, filename, file_ext):
    from compiler.scml import Scml
    input_path = join_all(filepath, filename, file_ext)
    scml_class = Scml(input_path)
    scml_class.build_scml(filepath, 1)


def convert_scml_zip(filepath, filename, file_ext):
    from zipfile import ZipFile
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "scml")
    # check anim.bin
    hasanim = False
    hasbuild = False
    with ZipFile(input_path) as input_zip:
        namelist = input_zip.namelist()
        if 'anim.bin' in namelist:
            hasanim = True
        if 'build.bin' in namelist:
            hasbuild = True
    if hasanim:
        from compiler.anim import DSAnim
        anim_class = DSAnim(input_path)
        # for anim in anims[1:]:
        #    anim_class += anim
        # for anim in anims:
        #    anim.close()
        anim_class.to_scml(output_path)
    elif hasbuild:
        unzip_file(filepath, filename, file_ext)
        from compiler.anim_build import AnimBuild
        build_file = join_all(filepath, "build", "bin")
        build_file = read_file(build_file)
        build_class = None
        with ZipFile(input_path) as build:
            build_class = AnimBuild(build_file, build)
        build_class.bin_to_json()
        build_class.save_symbol_images(filepath)


def unzip_file(filepath, filename, file_ext):
    from zipfile import ZipFile
    input_path = join_all(filepath, filename, file_ext)
    """
    解压给定的 ZIP 文件到当前文件夹
    :param zip_file_path: 要解压的 ZIP 文件的路径
    """
    with ZipFile(input_path, 'r') as zip_ref:
        zip_ref.extractall(filepath)


def read_file(file):
    data = None
    with open(file, 'rb') as f:
        data = f.read()
    return data


image_exts = {"png", "jpg", "jpeg", "gif", "tiff", "bmp"}

helptext = '''饥荒动画转换工具DS Anim Convert Tools
[1]build.bin<->build.xml
[2]anim.bin<->anim.xml
[3]zip<->scml
[4]tex<->png
[5]zip->scml images [without anim.bin]
'''
unrecognized_file = '''无法识别文件
Cannot Identity File
'''


def require():
    try:
        import rich
    except BaseException:
        pass


if __name__ == '__main__':
    main()
