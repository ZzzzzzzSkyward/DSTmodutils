'''
判断图片是否全透明
'''
import sys
from PIL import Image

def istransparent(filename):
    try:
        with Image.open(filename) as image:
            return image.mode == 'RGBA' and not any(image.getchannel('A').getdata())
    except (IOError, OSError):
        return False

if __name__ == '__main__':
    # 获取命令行参数
    if len(sys.argv) < 2:
        print('Usage: python istransparent.py filename')
        sys.exit(1)
    filename = sys.argv[1]

    # 判断图片是否全透明
    if is_transparent(filename):
        print(f'The image file {filename} is fully transparent.')
    else:
        print(f'The image file {filename} is not fully transparent.')