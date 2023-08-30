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
    except BaseException:
        pass
    try:
        import cv2
    except BaseException:
        pass
    try:
        import PIL
    except BaseException:
        pass


if __name__ == '__main__':
    main()
