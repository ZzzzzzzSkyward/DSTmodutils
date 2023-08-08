'''
这个是命令行程序
'''
import os
import sys
import shutil
sys.path.append("compiler")


def main():
    require()
    args, params = parse()
    if len(args) == 0:
        help()
        return
    filename = args[0]
    if filename == "":
        help()
        return
    work(args, params)


def work(args, params):
    fn = None
    filepath, filename, file_ext = split_all(args[0])
    if len(args) == 1:
        if file_ext == "xml":
            fn = convert_image_xml
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
        if file_ext == "scml" or file_ext == "scon":
            # *.scml/*.scon->*.zip
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
            filedir = join_all(filepath, filename)
            if os.path.isdir(filedir):
                # check if it is a scml project
                filelist = os.listdir(filedir)
                scmllist = [i for i in filelist if i.endswith(".scml")]
                imagelist = [i for i in filelist if i.endswith('.png')]
                if len(scmllist) > 0:
                    filedir, filename, file_ext = split_all(
                        join_all(filedir, scmllist[0]))
                    fn = convert_scml_scml
                # check if it is a bunch of images
                elif len(imagelist) > 0:
                    fn = convert_image_dir
                    file_ext = imagelist

    if len(args) == 2:
        filepath1, filename1, file_ext1 = split_all(args[1])
        if file_ext == "png" and args[1].find("xml") >= 0:
            # png->xml&tex
            print("这条命令忽略输入的xml路径")
            params.set("xml", True)
            fn = convert_image_png
    if fn:
        fn(filepath, filename, file_ext, params)
    else:
        print(unrecognized_file)


def help():
    print(helptext)


class ParsedArgs:
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        return None  # 返回默认值 None

    def set(self, name, value):
        setattr(self, name, value)


def parse():
    args = sys.argv[1:]
    params = {arg.lstrip('-'): True
              for arg in args if arg.startswith('-')}
    args = [arg for arg in args if not arg.startswith('-')]
    return args, ParsedArgs(params)


def split_all(filename):
    filename = os.path.abspath(filename)
    path, file = os.path.split(filename)
    file, ext = os.path.splitext(file)
    ext = ext.strip('.')
    return path, file, ext


def join_all(dir, name, ext=None):
    #print(f'd={dir}, n={name}, e={ext}')
    file = name + (("." + ext)if ext is not None else "")
    return os.path.join(dir, file)


def convert_build_bin(filepath, filename, file_ext, params):
    from buildtoxml import BuildToXml
    output_ext = "xml"
    BuildToXml(
        join_all(filepath, filename, file_ext),
        join_all(filepath, filename, output_ext),
    )


def convert_build_xml(filepath, filename, file_ext, params):
    from xmltobuild import XmlToBuild
    output_ext = "bin"
    XmlToBuild(
        join_all(filepath, filename, file_ext),
        join_all(filepath, filename, output_ext),
    )


def convert_anim_xml(filepath, filename, file_ext, params):
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


def convert_anim_bin(filepath, filename, file_ext, params):
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


def convert_to_png(filepath, filename, file_ext, params):
    from PIL import Image
    image_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "png")
    image = Image.open(image_path)
    image.save(output_path, "png")


def convert_image_png(filepath, filename, file_ext, params):
    if file_ext != "png":
        convert_to_png(filepath, filename, file_ext, params)
        file_ext = "png"
    from compiler.ktech import png_to_tex
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "tex")
    atlas_path = join_all(filepath, filename, "xml") if params.xml else None
    errmsg = png_to_tex(input_path, output_path, atlas_path)
    if errmsg:
        print(errmsg)


def convert_image_tex(filepath, filename, file_ext, params):
    from compiler.ktech import tex_to_png
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "png")
    errmsg = tex_to_png(input_path, output_path)
    if errmsg:
        print(errmsg)


def convert_image_dir(filepath, filename, filelist, params):
    import editxml
    detect_special_images(filepath, filename, filelist, params)
    output_path = join_all(filepath, filename, "xml")
    editxml.main(["p", output_path])


def convert_image_xml(filepath, filename, file_ext, params):
    from compiler.stex import xml_to_png
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, "")
    xml_to_png(input_path, output_path)


def detect_special_images(filepath, filename, filelist, params):
    # inventoryimages,64x64,crop
    fn = None
    if filename.find("inventoryimages") >= 0:
        fn = convert_inventoryimages
    # minimap icon,crop,atlas to power 2
    if filename.find("minimap") >= 0 or filename.find("mapicon"):
        fn = convert_map
    # cookbook icon,crop,max to 128x128,crop
    if filename.find("cookbook") >= 0:
        fn = convert_cookbook
    if fn is None:
        fn = convert_xml_common
    fn(filepath, filename, filelist, params)


def crop_images(input_dir, filelist, maxwidth,
                maxheight, targetwidth, targetheight):
    from crop import crop_image
    for i in filelist:
        crop_image(
            join_all(
                input_dir,
                i),
            maxwidth,
            maxheight,
            targetwidth,
            targetheight)


def mkdir(d):
    if os.path.exists(d):
        return
    return os.mkdir(d)


def convert_inventoryimages(filepath, filename, filelist, params):
    from compiler.stex import png_to_xml
    input_dir = join_all(filepath, filename)
    temp_dir = make_temp_dir(filepath, filename)
    shutil.copytree(input_dir, temp_dir)
    crop_images(temp_dir, filelist, None, None, 64, 64)
    errmsg = png_to_xml(temp_dir, filepath or input_dir)
    # shutil.rmtree(temp_dir)
    if errmsg:
        print(errmsg)


def convert_map(filepath, filename, filelist, params):
    from compiler.stex import png_to_xml
    input_dir = join_all(filepath, filename)
    temp_dir = make_temp_dir(filepath, filename)
    shutil.copytree(input_dir, temp_dir)
    crop_images(temp_dir, filelist, None, None, None, None)  # 根据需求设置参数
    print("请手动使用Texture And Atlas Packer输出2的幂宽高")
    return
    errmsg = png_to_xml(temp_dir, filepath or input_dir)
    # shutil.rmtree(temp_dir)
    if errmsg:
        print(errmsg)


def convert_cookbook(filepath, filename, filelist, params):
    from compiler.stex import png_to_xml
    input_dir = join_all(filepath, filename)
    temp_dir = make_temp_dir(filepath, filename)
    shutil.copytree(input_dir, temp_dir)
    crop_images(temp_dir, filelist, None, None, 128, 128)  # 根据需求设置参数
    errmsg = png_to_xml(temp_dir, filepath or input_dir)
    # shutil.rmtree(temp_dir)
    if errmsg:
        print(errmsg)


def convert_xml_common(filepath, filename, filelist, params):
    from compiler.stex import png_to_xml
    input_dir = join_all(filepath, filename)
    temp_dir = make_temp_dir(filepath, filename)
    shutil.copytree(input_dir, temp_dir)
    crop_images(temp_dir, filelist, None, None, None, None)  # 根据需求设置参数
    errmsg = png_to_xml(temp_dir, filepath or input_dir)
    # shutil.rmtree(temp_dir)
    if errmsg:
        print(errmsg)


def make_temp_dir(root, dir):
    dir = dir.strip('/').strip('\\')
    return join_all(root, dir + '/' + dir)


def convert_scml_scml(filepath, filename, file_ext, params):
    from compiler.scml import Scml
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename + "_interp", file_ext)
    if params.interpolate or params.interp:
        # do interpolate
        if file_ext == 'scml':
            print("目前无法对scml插值，请转换为scon后再执行此操作")
            return
        from interpolate import processroot
        input_data = read_file(input_path, ftype="json")
        try:
            output_data = processroot(input_data, params.fps)
            save_file(output_path, output_data)
        except Exception as e:
            print(e)
            print("目前插值仅适用于规范的30fps动画")
    if file_ext == "scon":
        print("目前无法编译scon，请转换为scml后再执行此操作")
        return
    if params.crop:
        if file_ext == "scon":
            print("目前无法裁剪scon，请转换为scml后再执行此操作")
        else:
            from cropscml import crop_pivot_values
            temp_dir = join_all(os.path.dirname(filepath), "tempdir")
            shutil.copytree(filepath, temp_dir)
            temp_path = join_all(temp_dir, filename, file_ext)
            crop_pivot_values(temp_path)
            scml_class = Scml(temp_path)
            scml_class.build_scml(filepath, 1)
            shutil.rmtree(temp_dir)
            return

    scml_class = Scml(input_path)
    scml_class.build_scml(filepath, 1)


def convert_scml_zip(filepath, filename, file_ext, params):
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


def read_file(file, ftype=None):
    data = None
    with open(file, 'rb') as f:
        if ftype == "json":
            import json
            data = json.load(f)
        else:
            data = f.read()
    return data


def save_file(file, data):
    import json
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)


image_exts = {"png", "jpg", "jpeg", "gif", "tiff", "bmp"}

helptext = '''饥荒动画转换工具DS Anim Convert Tools
[1]build.bin<->build.xml
[2]anim.bin<->anim.xml
[3]zip<->scml -crop
[4]tex<->png -xml
[5]zip->scml images [without anim.bin]
[6]xml<->images [auto resize cookbook, inventoryimages, minimap]
[7]scon -interpolate -fps=30
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
