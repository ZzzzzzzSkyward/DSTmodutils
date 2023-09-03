import subprocess
import os
possible_paths = ["./", "../", "./ztools/", "../ztools/", "../../", "../../ztools/"]
ztools_exe = "ztools.exe"
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)


def locate_exe(exe_name, directories):
    for directory in directories:
        exe_path = os.path.join(script_dir,directory, exe_name)
        if os.path.exists(exe_path):
            return os.path.abspath(exe_path)
        exe_path = os.path.join(directory, exe_name)
        if os.path.exists(exe_path):
            return os.path.abspath(exe_path)
    return None


ztoolspath = locate_exe(ztools_exe, possible_paths)
if not ztoolspath:
    print("ztools.exe，请手动修改possible_paths里的搜索路径。Cannot find ztools.exe ,please manually modify possible_paths.")
    ztoolspath = ztools_exe


def run(command):
    """
    运行命令并阻止打印输出
    :param command: 要执行的命令
    """
    #print(command)
    # 执行命令并捕获子进程的输出
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        stderr = stderr.decode("utf-8")
    if stdout:
        stdout = stdout.decode('utf-8')
    return stderr or stdout


def png_to_xml(dir, dest=None):
    if dest is None:
        dest = os.path.dirname(dir) or dir
    cmd = f'{ztoolspath} "{dir}" "{dest}"'
    return run(cmd)

def tex_to_png(dir,dest=None):
    if dest is None:
        dest = os.path.dirname(dir) or dir
    cmd = f'{ztoolspath} "{dir}" "{dest}"'
    return run(cmd)