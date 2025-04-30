import os
import pyzjr.Z as Z
from pathlib import Path
from pyzjr.data.utils.listfun import natsorted

def getPhotoPath(path, debug=False):
    """
    :param path: 文件夹路径
    :param debug: 开启打印文件名错误的名字
    :return: 包含图片路径的列表
    """
    imgfile = []
    allfile = []
    file_list = os.listdir(path)
    for i in file_list:
        if debug:
            if i[0] in ['n', 't', 'r', 'b', 'f'] or i[0].isdigit():
                print(f"File name error occurred at the beginning of {i}!")
        newph = os.path.join(path, i).replace("\\", "/")
        allfile.append(newph)
        _, file_ext = os.path.splitext(newph)
        if file_ext[1:] in Z.IMG_FORMATS:
            imgfile.append(newph)

    return natsorted(imgfile), natsorted(allfile)

def SearchFilePath(filedir, file_ext='.png'):
    """What is returned is a list that includes all paths under the target path that match the suffix."""
    search_file_path = []
    for root, dirs, files in os.walk(filedir):
        for filespath in files:
            if str(filespath).endswith(file_ext):
                search_file_path.append(os.path.join(root, filespath))
    return natsorted(search_file_path)

def SearchFileName(target_path, file_ext='.png'):
    """Only search for file names in the appropriate format in the target folder"""
    all_files = os.listdir(target_path)
    png_files = [file for file in all_files if file.lower().endswith(file_ext)]
    sorted_png_files = natsorted(png_files)
    return sorted_png_files

def split_path2list(path_str):
    """
    path_list = split_path2list('D:\PythonProject\MB_TaylorFormer\DehazeFormer\data\rshazy\test\GT\220.png')
    Return:
        ['D:\\', 'PythonProject', 'MB_TaylorFormer', 'DehazeFormer', 'data', 'rshazy', 'test', 'GT', '220.png']
    """
    path = Path(path_str)
    path_parts = path.parts
    return list(path_parts)

def getSpecificImages(basePath, contains=None):
    # return the set of files that are valid
    return list(SearchSpecificFilePath(basePath, validExts=Z.IMG_FORMATS, contains=contains))

def SearchSpecificFilePath(basePath, validExts=None, contains=None):
    # loop over the directory structure
    for (rootDir, dirNames, filenames) in os.walk(basePath):
        for filename in filenames:
            if contains is not None and filename.find(contains) == -1:
                continue
            ext = filename[filename.rfind("."):].lower()

            if validExts is None or ext.endswith(validExts):
                imagePath = os.path.join(rootDir, filename)
                yield imagePath



if __name__ == "__main__":
    path = r"E:\PythonProject\pyzjrPyPi"
    print(SearchFilePath(path))
    print(getSpecificImages(path))