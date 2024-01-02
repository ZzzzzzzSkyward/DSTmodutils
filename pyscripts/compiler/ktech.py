possible_paths=["./","../","./ktools/","../ktools","../../","../../ktools/"]
ktech_exe="ktech.exe"
import os
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

ktechpath=locate_exe(ktech_exe,possible_paths)
if not ktechpath:
    print("找不到ktech.exe，请手动修改possible_paths里的搜索路径。Cannot find ktech.exe, please manually modify possible_paths.")
    ktechpath=ktech_exe
import subprocess

def run(command):
    """
    运行命令并阻止打印输出
    :param command: 要执行的命令
    """
    # 执行命令并捕获子进程的输出
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        stderr=stderr.decode("utf-8")
    return stderr #or stdout

def png_to_tex(path,dest=None,atlas=None):
    if dest==None:
        dest=os.path.dirname(path)
    if atlas and atlas!="":
        if atlas=="." or atlas=="-":
            atlas=path.replace(".png",".xml")
        if not atlas.find("xml"):
            atlas=atlas+'.xml'
    doatlas=f'--atlas "{atlas}"' if atlas else ""
    cmd=f'{ktechpath} {doatlas} "{path}" "{dest}"'
    return run(cmd)
def tex_to_png(path,dest=None):
    if dest==None:
        dest=os.path.dirname(path)
    if isinstance(path,list):
        for i in path:
            tex_to_png(i,dest)
        return
    cmd=f'{ktechpath} "{path}" "{dest}"'
    #print(cmd)
    return run(cmd)