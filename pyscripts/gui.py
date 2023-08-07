'''
这是GUI脚本
'''
import os
import sys
import PySimpleGUI as gui
def main():
    require()
    filename = gui.popup_get_file("打开你要处理的文件")
    print(filename)
    pass
def require():
    try:
        import rich
    except:
        pass
    try:
        import cv2
    except:
        pass
    try:
        import PIL
    except:
        pass
if __name__ == '__main__':
    main()