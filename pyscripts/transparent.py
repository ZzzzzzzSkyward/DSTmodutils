'''
图片透明
'''
import os
import shutil
import subprocess
import sys


def make_transparent(dir_path):
    if not os.path.exists(dir_path):
        print('Directory does not exist: ' + dir_path)
        return
    # create backup directory
    backup_dir = dir_path + '-old'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # find all png files recursively
    png_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.png'):
                png_files.append(os.path.join(root, file))

    # make each png file transparent and backup the original
    for png_file in png_files:
        basename = os.path.basename(png_file)
        backup_path = os.path.join(backup_dir, basename)
        shutil.copy2(png_file, backup_path)
        png_file=os.path.abspath(png_file)
        print(png_file)
        subprocess.call(['magick', 'convert', '-alpha', 'set', '-channel', 'A', '-evaluate', 'set', '0%', png_file, png_file])


def revert_dir(path):
    # get directory paths from command line arguments
    # find all backup files
    backup_dir = path + '-old'
    if not os.path.exists(backup_dir):
        print('Backup directory does not exist: ' + backup_dir)
        return
    backup_files = []
    for root, dirs, files in os.walk(backup_dir):
        for file in files:
            backup_files.append(os.path.join(root, file))

    # restore each backup file
    for backup_file in backup_files:
        basename = os.path.basename(backup_file)
        original_path = os.path.join(dir_path, basename)
        shutil.copy2(backup_file, original_path)

    # delete backup directory
    shutil.rmtree(backup_dir)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: transparent.py [--revert] dir1 dir2 ...')
        sys.exit(1)
    revert = sys.argv[1].find('-r')>=0
    if revert:
        dir_paths = sys.argv[2:]
        for dir_path in dir_paths:
            revert_dir(dir_path)
    else:
        # get directory paths from command line arguments
        dir_paths = sys.argv[1:]
        for dir_path in dir_paths:
            make_transparent(dir_path)
