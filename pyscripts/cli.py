"""
这个是命令行程序
"""
import os
import sys
import shutil

sys.path.append("compiler")
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将当前目录添加到sys.path
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "compiler"))
pretty_error = False


def main():
    require()
    args, params = parse()
    if len(args) == 0:
        help()
        loop()
        return
    filename = args[0]
    if filename == "":
        help()
        return
    work(args, params)


def loop():
    while True:
        args, params = parse(input(">").strip('"').strip("\n").split(" "))
        if len(args) == 0:
            return
        filename = args[0]
        if filename == "":
            help()
            return
        try:
            work(args, params)
        except Exception as e:
            print(e)


def work(args, params):
    fn = None
    filepath, filename, file_ext = split_all(args[0])
    # print(filepath, filename, file_ext)
    if len(args) == 1:
        if file_ext == "xml":
            fn = convert_image_xml
        if file_ext == "bin" and (filename == "build" or params.build):
            # build.bin->build.xml
            fn = convert_build_bin
        if file_ext == "xml" and (filename == "build" or params.build):
            # build.xml->build.bin
            fn = convert_build_xml
        if (file_ext == "json" or file_ext == "js") and (
            filename == "build" or params.build
        ):
            # build.json->build.bin
            fn = convert_build_json
        if file_ext == "xml" and (filename == "anim" or params.anim):
            # anim.xml->anim.bin
            fn = convert_anim_xml
        if file_ext == "json" and (filename == "anim" or params.anim):
            # anim.json->anim.bin
            fn = convert_anim_json
            # anim.json rebuild
            if params.crop:
                fn = rebuild_anim_json
        if file_ext == "bin" and (filename == "anim" or params.anim):
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
        if file_ext == "dyn":
            # dyn->zip
            fn = convert_dyn_zip
        if not file_ext:
            filedir = join_all(filepath, filename)
            if os.path.isdir(filedir):
                # check if it is a scml project
                filelist = os.listdir(filedir)
                scmllist = [i for i in filelist if i.endswith(".scml")]
                imagelist = [i for i in filelist if i.endswith(".png")]
                binlist = [i for i in filelist if i.endswith(".bin")]
                if len(scmllist) > 0:
                    filedir, filename, file_ext = split_all(
                        join_all(filedir, scmllist[0])
                    )
                    fn = convert_scml_scml
                # check if it is a decompressed zip dir
                elif len(binlist) > 0 and "build.bin" in binlist:
                    fn = convert_scml_dir
                    file_ext = filelist
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
        if not file_ext1:
            filedir1 = join_all(filepath1, filename1)
            if os.path.isdir(filedir1):
                if file_ext == "xml" and (filename == "build" or params.build):
                    # build.xml + */*.png -> build.zip
                    params.set("filedir1", filedir1)
                    fn = convert_scml_build
                if file_ext == "bin" and (filename == "build" or params.build):
                    # build.bin + */*.png -> build.zip
                    params.set("filedir1", filedir1)
                    fn = convert_scml_build
                if file_ext == "json" and (filename == "build" or params.build):
                    # build.json + */*.png -> build.zip
                    params.set("filedir1", filedir1)
                    fn = convert_scml_build

    if fn:
        fn(filepath, filename, file_ext, params)
    else:
        print(unrecognized_file)
        print(args)


def help():
    print(helptext)


class ParsedArgs:
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        return None  # 返回默认值 None

    def set(self, name, value):
        setattr(self, name, value)


def parse(args=None):
    args = args or sys.argv[1:]
    params_ = {arg.lstrip("-"): True for arg in args if arg.startswith("-")}
    params = {arg.lstrip("-"): True for arg in args if arg.startswith("-")}
    for i in params_:
        keys = i.split("=")
        if len(keys) == 1:
            pass
        else:
            params[keys[0]] = "=".join(keys[1:])

    args = [arg for arg in args if not arg.startswith("-")]
    return args, ParsedArgs(params)


def split_all(filename):
    filename = os.path.abspath(filename)
    path, file = os.path.split(filename)
    file, ext = os.path.splitext(file)
    ext = ext.strip(".")
    return path, file, ext


def join_all(dir, name, ext=None):
    # print(f'd={dir}, n={name}, e={ext}')
    file = name + (("." + ext) if ext is not None else "")
    return os.path.join(dir, file)


def convert_build_bin(filepath, filename, file_ext, params):
    if params.rename or params.json:
        from compiler.anim_build import AnimBuild

        build_path = join_all(filepath, filename, file_ext)
        build_file = read_file(build_path)
        build_class = AnimBuild(build_file)
        build_class.bin_to_json()
        if params.rename:
            print(f"原build名：{build_class.data['name']}")
            build_class.set_build_name(params.rename)
            build_class.json_to_bin()
            build_class.save_bin(filepath)
            print(f"rename指令仅仅重命名原文件为{params.rename}")
            return
        if params.json:
            build_class.save_json(filepath)
    else:
        from buildtoxml import BuildToXml

        output_ext = "xml"
        build_path = join_all(filepath, filename, file_ext)
        build_file = read_file(build_path)
        BuildToXml(
            build_file,
            join_all(filepath, filename, output_ext),
        )


def convert_build_xml(filepath, filename, file_ext, params):
    from xmltobuild import XmlToBuild

    output_ext = "bin"
    XmlToBuild(
        join_all(filepath, filename, file_ext),
        join_all(filepath, filename, output_ext),
    )


def convert_build_json(filepath, filename, file_ext, params):
    from compiler.anim_build import AnimBuild

    build_path = join_all(filepath, filename, file_ext)
    build_file = read_file(build_path, "json")
    if params.crop:
        import clip_build

        print(
            "-crop参数仅仅裁剪",
            filename,
            ", 覆盖原文件",
            not params.check,
            "补偿",
            not not params.compensate,
            "裁剪图片",
            not not params.clip,
        )
        if params.remove_vert:
            if "Vert" in build_file:
                del build_file["Vert"]
        if params.check:
            if 'Path' not in build_file:
                build_file['Path']=filepath
            clip_build.check(build_file)
        else:
            #add a safeguard not to wrongly remove all images
            if clip_build.clip(
                build_file, compensate_pivot=params.compensate, clip_image=params.clip
            ) and len(list(build_file.get('Symbol',{}).keys()))>0:
                save_file(build_path, build_file)
        return
    build_class = AnimBuild(build_file)
    build_class.json_to_bin()
    build_class.save_bin(filepath)


def convert_anim_xml(filepath, filename, file_ext, params):
    from xmltoanim import XmlToAnim

    output_ext = "bin"
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, output_ext)
    input_string = None
    with open(input_path, "r") as input_file:
        input_string = input_file.read()
    with open(output_path, "wb") as output_file:
        XmlToAnim(input_string, output_file)


def convert_anim_json(filepath, filename, file_ext, params):
    from compiler.anim_bank import AnimBank

    input_path = join_all(filepath, filename, file_ext)
    input_data = read_file(input_path, "json")
    bank_class = AnimBank(input_data)
    bank_class.save_bin("")


def convert_anim_bin(filepath, filename, file_ext, params):
    from animtoxml import AnimToXml

    input_path = join_all(filepath, filename, file_ext)
    if params.json:
        from compiler.anim_bank import AnimBank

        input_data = read_file(input_path)
        bank_class = AnimBank(input_data)
        bank_class.save_json(filepath)
    else:
        output_ext = "xml"
        output_path = join_all(filepath, filename, output_ext)
        input_bytes = None
        with open(input_path, "rb") as f:
            input_bytes = f.read()
        output_string = AnimToXml(input_bytes)
        with open(output_path, "wb") as output_file:
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
    if params.ktech:
        from compiler.ktech import png_to_tex
    elif params.ztools:
        from compiler.ztools import png_to_tex
    else:
        from compiler.stex import png_to_tex
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename, "tex")
    atlas_path = join_all(filepath, filename, "xml") if params.xml else None
    errmsg = png_to_tex(input_path, output_path, atlas_path)
    if errmsg:
        print(errmsg)
        return
    if params.dyn:
        zip_path = join_all(filepath, filename, "tex")
        from zipfile import ZipFile

        zip_file = ZipFile(zip_path, mode="w")
        zip_file.write(output_path)
        zip_file.close()
        from compiler.dynamic import zip_to_dyn

        zip_to_dyn(zip_path)
        os.remove(zip_path)


def convert_image_tex(filepath, filename, file_ext, params):
    input_path = join_all(filepath, filename, file_ext)
    if params.dyn:
        zip_path = join_all(filepath, filename, "tex")
        from zipfile import ZipFile

        zip_file = ZipFile(zip_path, mode="w")
        zip_file.write(input_path)
        zip_file.close()
        from compiler.dynamic import zip_to_dyn

        zip_to_dyn(zip_path)
        os.remove(zip_path)
    else:
        output_path = join_all(filepath, filename, "png")
        if params.ktech:
            from compiler.ktech import tex_to_png
        else:
            from compiler.stex import tex_to_png
        errmsg = tex_to_png(input_path, output_path)
        if errmsg:
            print(errmsg)


def convert_dyn_zip(filepath, filename, file_ext, params):
    input_path = join_all(filepath, filename, file_ext)
    zip_path = join_all(filepath, filename, "zip")
    subdir = join_all(filepath, filename)
    from compiler.dynamic import dyn_to_zip

    dyn_to_zip(input_path)
    if params.png:
        from zipfile import ZipFile

        zip_file = ZipFile(zip_path, mode="r")
        zip_file.extractall(subdir)
        zip_file.close()
        convert_image_tex(subdir, "atlas-0", "tex", params)


def convert_image_dir(filepath, filename, filelist, params):
    import editxml

    detect_special_images(filepath, filename, filelist, params)
    output_path = join_all(filepath, filename, "xml")
    editxml.main(["p", output_path])


def convert_image_xml(filepath, filename, file_ext, params):
    if params.ztools:
        from compiler.ztools import xml_to_png
    else:
        from compiler.stex import xml_to_png
    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename)
    errmsg = xml_to_png(input_path, output_path)
    if errmsg:
        print(errmsg)


def detect_special_images(filepath, filename, filelist, params):
    # inventoryimages,64x64,crop
    fn = None
    if filename.find("inventoryimages") >= 0:
        fn = convert_inventoryimages
    # minimap icon,crop,atlas to power 2,rename to png
    if filename.find("minimap") >= 0 or filename.find("mapicon") >= 0:
        fn = convert_map
    # cookbook icon,crop,max to 128x128,crop
    if filename.find("cookbook") >= 0:
        fn = convert_cookbook
    if fn is None:
        fn = convert_xml_common
    fn(filepath, filename, filelist, params)


def crop_images(input_dir, filelist, maxwidth, maxheight, targetwidth, targetheight):
    from crop import crop_image

    for i in filelist:
        crop_image(
            join_all(input_dir, i), maxwidth, maxheight, targetwidth, targetheight
        )


def mkdir(d):
    if os.path.exists(d):
        return
    return os.mkdir(d)


def convert_inventoryimages(filepath, filename, filelist, params):
    if params.ztools:
        from compiler.ztools import png_to_xml
    else:
        from compiler.stex import png_to_xml
    input_dir = join_all(filepath, filename)
    temp_dir = make_temp_dir(filepath, filename)
    pngs = [
        os.path.join(input_dir, item)
        for item in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, item))
        and item.lower().endswith(".png")
    ]
    pngs = [shutil.copy2(png, temp_dir) for png in pngs]
    crop_images(temp_dir, filelist, None, None, 64, 64)
    errmsg = png_to_xml(temp_dir, filepath or input_dir)
    if not params.preserve_temp:
        shutil.rmtree(temp_dir)
    if errmsg:
        print(errmsg)


def convert_map(filepath, filename, filelist, params):
    if params.ztools:
        from compiler.ztools import png_to_xml
    else:
        from compiler.stex import png_to_xml
    input_dir = join_all(filepath, filename)
    temp_dir = make_temp_dir(filepath, filename)
    pngs = [
        os.path.join(input_dir, item)
        for item in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, item))
        and item.lower().endswith(".png")
    ]
    pngs = [shutil.copy2(png, temp_dir) for png in pngs]
    crop_images(
        temp_dir,
        filelist,
        params.maxwidth,
        params.maxheight,
        params.targetwidth,
        params.targetheight,
    )  # 根据需求设置参数
    errmsg = png_to_xml(temp_dir, filepath or input_dir)
    if not params.preserve_temp:
        shutil.rmtree(temp_dir)
    if errmsg:
        print(errmsg)


def convert_cookbook(filepath, filename, filelist, params):
    if params.ztools:
        from compiler.ztools import png_to_xml
    else:
        from compiler.stex import png_to_xml
    input_dir = join_all(filepath, filename)
    temp_dir = make_temp_dir(filepath, filename)
    pngs = [
        os.path.join(input_dir, item)
        for item in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, item))
        and item.lower().endswith(".png")
    ]
    pngs = [shutil.copy2(png, temp_dir) for png in pngs]
    crop_images(temp_dir, filelist, None, None, 128, 128)  # 根据需求设置参数
    errmsg = png_to_xml(temp_dir, filepath or input_dir)
    if not params.preserve_temp:
        shutil.rmtree(temp_dir)
    if errmsg:
        print(errmsg)


def convert_xml_common(filepath, filename, filelist, params):
    if params.ztools:
        from compiler.ztools import png_to_xml
    else:
        from compiler.stex import png_to_xml
    input_dir = join_all(filepath, filename)
    temp_dir = make_temp_dir(filepath, filename)
    pngs = [
        os.path.join(input_dir, item)
        for item in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, item))
        and item.lower().endswith(".png")
    ]
    pngs = [shutil.copy2(png, temp_dir) for png in pngs]
    # crop_images(temp_dir, filelist, None, None, None, None)  # 根据需求设置参数
    errmsg = png_to_xml(input_dir, filepath or input_dir)
    if not params.preserve_temp:
        shutil.rmtree(temp_dir)
    if errmsg:
        print(errmsg)


def make_temp_dir(root, dir):
    dir = dir.strip("/").strip("\\")
    ret = join_all(root, dir + "/" + dir)
    mkdir(ret)
    return ret


def convert_scml_scml(filepath, filename, file_ext, params):
    from compiler.scml import Scml

    input_path = join_all(filepath, filename, file_ext)
    output_path = join_all(filepath, filename + "_interp", file_ext)
    if params.interpolate or params.interp:
        # do interpolate
        if file_ext == "scml":
            print("目前无法对scml插值，请转换为scon后再执行此操作")
            return
        from interpolate import processroot

        input_data = read_file(input_path, ftype="json")
        try:
            processroot(input_data, params.fps or 30)
            save_file(output_path, input_data)
        except Exception as e:
            if pretty_error:
                raise e
            else:
                print(e)
                print("目前插值仅适用于规范的30fps动画")
            return
        return
    if file_ext == "scon":
        print("目前无法编译scon，请转换为scml后再执行此操作")
        return
    if params.crop:
        if file_ext == "scon":
            print("目前无法裁剪scon，请转换为scml后再执行此操作")
        else:
            from cropscml import crop_pivot_values

            temp_dir = join_all(filepath, "tempdir")
            shutil.copytree(filepath, temp_dir)
            temp_path = join_all(temp_dir, filename, file_ext)
            crop_pivot_values(temp_path)
            scml_class = Scml(temp_path)
            scml_class.build_scml(filepath, 1)
            # shutil.rmtree(temp_dir)
            return

    scml_class = Scml(input_path)
    scml_class.build_scml(filepath, 1)


def convert_scml_dir(filepath, filename, filelist, params):
    input_path = join_all(filepath, filename)
    output_path = join_all(input_path, filename, "scml")
    from compiler.anim import DSAnim
    from compiler.anim_build import AnimBuild

    anims = [i for i in filelist if i.endswith("bin") and i.find("anim") >= 0]
    builds = [i for i in filelist if i.endswith("bin") and i.find("build") >= 0]
    atlases = [i for i in filelist if i.endswith("tex") and i.find("atlas") >= 0]
    if len(anims) > 0:
        # this is a full scml project
        anim_file = join_all(input_path, anims[0])
        anim_class = DSAnim(anim_file)
        for anim in anims[1:]:
            anim_class2 = DSAnim(join_all(input_path, anim))
            anim_class += anim_class2
            anim_class2.close()
        for i, build in enumerate(builds):
            build_data = read_file(join_all(input_path, build))
            build_class = AnimBuild(build_data, input_path)
            anim_class.parse_file(build_class)
        anim_class.to_scml(output_path)
    elif len(builds) > 0:
        for i, build in enumerate(builds):
            build_data = read_file(join_all(input_path, build))
            build_class = AnimBuild(build_data, input_path)
            build_class.bin_to_json()
            build_class.save_symbol_images(input_path)
    else:
        for i, atlas in enumerate(atlases):
            convert_image_tex(filepath, atlas[:-4], "tex", params)


def convert_scml_build(filepath, filename, file_ext, params):
    if file_ext == "xml":
        print("xml格式暂时不可用，请改用bin或json格式")
        return
    build_path = join_all(filepath, filename, file_ext)
    build_file = read_file(build_path, ftype=file_ext)
    from compiler.anim_build import AnimBuild

    build_class = None
    image_path = params.filedir1
    build_class = AnimBuild(build_file, None, image_path)
    build_class.bin_to_json()
    if params.rename:
        build_class.set_build_name(params.rename)
    elif not "name" in build_class.data:
        build_class.set_build_name(filename)
    build_class.save_bin(filepath)


def convert_scml_zip(filepath, filename, file_ext, params):
    from zipfile import ZipFile

    input_path = join_all(filepath, filename, file_ext)
    output_dir = join_all(filepath, filename)
    mkdir(output_dir)
    output_path = join_all(filepath, filename, "scml")
    # check anim.bin
    hasanim = False
    hasbuild = False
    has_output = False
    with ZipFile(input_path) as input_zip:
        namelist = input_zip.namelist()
        if "anim.bin" in namelist:
            hasanim = True
        if "build.bin" in namelist:
            hasbuild = True
    if hasanim:
        from compiler.anim import DSAnim

        anim_class = DSAnim(input_path)
        if params.json:
            anim_class.save_json(output_dir)
            has_output = True
        if params.scml:
            anim_class.to_scml(output_path)
            has_output = True
        if not has_output:
            anim_class.to_scml(output_path)
            has_output = True
    elif hasbuild:
        unzip_file(filepath, filename, file_ext)
        from compiler.anim_build import AnimBuild

        build_file = join_all(filepath, "build", "bin")
        build_file = read_file(build_file)
        build_class = None
        with ZipFile(input_path) as build:
            build_class = AnimBuild(build_file, build)
        build_class.bin_to_json()
        if params.json:
            build_class.save_json(output_dir)
            has_output = True
        build_class.save_symbol_images(output_dir)
    else:
        print("不存在anim.bin或build.bin，直接解压")
        unzip_file(filepath, filename, file_ext)


def rebuild_anim_json(filepath, filename, file_ext, params):
    # 该指令用于修复错误的anim边框
    input_path = join_all(filepath, filename, file_ext)
    build_path = params.crop
    anim_data = read_file(input_path, "json")
    build_data = read_file(build_path, "json")
    if not anim_data or not build_data:
        print("缺失文件Missing File")
        return
    from compiler.scml import Scml

    Scml.rebuild_anim(anim_data, build_data)
    save_file(input_path, anim_data)


def unzip_file(filepath, filename, file_ext):
    """
    解压给定的 ZIP 文件到当前文件夹
    """
    from zipfile import ZipFile

    input_path = join_all(filepath, filename, file_ext)
    with ZipFile(input_path, "r") as zip_ref:
        zip_ref.extractall(filepath)


def read_file(file, ftype=None):
    data = None
    with open(file, "rb") as f:
        if ftype == "json":
            import json

            data = json.load(f)
        else:
            data = f.read()
    if not data:
        print("无法打开文件", file)
        raise FileNotFoundError()
    return data


def save_file(file, data):
    import json

    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
    except OSError:
        print("保存文件", file, "出错")


image_exts = {"png", "jpg", "jpeg", "gif", "tiff", "bmp"}

helptext = """饥荒动画转换工具DS Anim Convert Tools
可通过 -anim -build 识别文件类型
[1]build.bin<->build.xml -json
   build.json -crop 
                    -check -compensate -clip -remove_vert
[2]build.bin -rename="build name"
[3]anim.bin<->anim.xml
[4]zip<->scml -crop
[5]tex<->png -xml
[6]zip->scml images [without anim.bin]
[7]xml<->images [auto resize cookbook, inventoryimages, minimap]
[8]scon -interpolate -fps=30
[9]build.bin/json */*.png ->zip -rename="build name"
[10]anim.json -crop=build.json
"""
unrecognized_file = """无法识别文件
Cannot Identify File
"""


def require():
    try:
        import rich
        from rich.traceback import install
        
        install()
        global pretty_error
        pretty_error = True
        pass
    except BaseException as e:
        pass


if __name__ == "__main__":
    main()
