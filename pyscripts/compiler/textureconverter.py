import os
import sys
import subprocess
possible_paths = ["./", "../", "../bin/", "../../", "../../bin/"]
converter_exe = "TextureConverter.exe"
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)


def locate_exe(exe_name, directories):
    for directory in directories:
        exe_path = os.path.join(script_dir, directory, exe_name)
        if os.path.exists(exe_path):
            return os.path.abspath(exe_path)
        exe_path = os.path.join(directory, exe_name)
        if os.path.exists(exe_path):
            return os.path.abspath(exe_path)
    return None


converterpath = locate_exe(converter_exe, possible_paths)
if not converterpath:
    print("找不到TextureConverter.exe，请手动修改possible_paths里的搜索路径。Cannot find TextureConverter.exe ,please manually modify possible_paths.")
    converterpath = converter_exe


texture_format = "bc3"
no_premultiply = False
platform = "opengl"
generate_mips = False
verbose = False
ignore_exceptions = False
def png_to_tex(input_paths: list[str] | str, output: str, atlas=None):
    width = None
    height = None

    if isinstance(input_paths, str):
        input_paths = [input_paths]

    # If a list is passed in, concatenate the filenames with semi-colon
    # separators, otherwise just use the filename
    src_filename_str = ';'.join(input_paths)

    cmd_list = [converterpath,
                '--swizzle',
                '--format ' + texture_format,
                '--platform ' + platform,
                '-i ' + src_filename_str,
                '-o ' + output,
                ]

    if generate_mips:
        cmd_list.append('--mipmap')

    if not no_premultiply:
        cmd_list.append('--premultiply')

    if width:
        cmd_list.append('-w {}'.format(width))
    if height:
        cmd_list.append('-h {}'.format(height))

    cmd = " ".join(cmd_list)
    if verbose:
        print(cmd)
    if subprocess.call(cmd_list) != 0:
        sys.stderr.write(
            "Error attempting to convert {} to {}\n".format(
                input_paths, output))
        sys.stderr.write(cmd + "\n")
        if not ignore_exceptions:
            raise
