# -*- coding: utf-8 -*-
'''
检查照片是否有原始日期时间, 如果没有通过解析照片文件名的时间, 然后设置为照片的EXIF中的原始日期时间
用法: python set_photo_orignal_datetime.py F:/photo/store/directory
'''

import os, sys
from datetime import datetime
import config, utils


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python set_photo_orignal_datetime.py <directory>")
        sys.exit(1)
    dir_path = sys.argv[1]

    ## 需要修改EXIF中的拍摄时间的文件
    will_update_original_datetime_files = {}
    ## 没有拍摄时间，且无法从文件名中解析出时间的文件
    will_not_update_original_datetime_files = []

    supported_extensions = [".jpg", ".jpeg", ".tiff"]
    for filename in os.listdir(dir_path):
        if not filename.lower().endswith(tuple(supported_extensions)):
            continue

        if filename not in config.force_update_original_datetime_files:
            ## 不是强制更新原始时间的照片，判断是否存在原始时间
            original_datetime = utils.get_image_exif_datetime(dir_path, filename)
            if original_datetime is not None:
                ## 如果存在原始时间，则跳过
                continue

        ## 如果是需要强制更新原始时间，或者照片中没有原始时间的照片，则尝试从文件名中解析时间
        datetime_from_filename = utils.parse_datetime_from_filename(filename)
        if datetime_from_filename is not None:
            ## 如果没有拍摄时间，并且文件名中解析出来的时间不为空
            will_update_original_datetime_files[filename] = datetime_from_filename
        else:
            ## 如果没有拍摄时间，并且文件名中解析出来的时间为空
            will_not_update_original_datetime_files.append(filename)
        
    print("需要修改并且可以修改的图片(%d张):" % len(will_update_original_datetime_files))    
    for filename, datetime_from_filename in will_update_original_datetime_files.items():
        print(filename + "\t\t" + datetime_from_filename.strftime('%Y-%m-%d %H:%M:%S'))

    print("\n")
    print("需要修改但是无法修改的图片(%d张):" % len(will_not_update_original_datetime_files))
    for filename in will_not_update_original_datetime_files:
        print(filename)

    ## 接收用户输入，确认是否修改
    print("\n")
    if len(will_update_original_datetime_files) == 0:
        print("没有需要修改的图片")
        sys.exit(0)
    print("是否修改以上图片的原始时间？(y/n)")
    user_input = input()
    if user_input.lower() != 'y':
        print("取消修改")
        sys.exit(0)
    print("开始修改图片原始时间...")
    for filename, datetime_from_filename in will_update_original_datetime_files.items():
        file_path = os.path.join(dir_path, filename)
        utils.set_image_exif_datetime_orginal(file_path, datetime_from_filename)
        print("修改成功: " + filename + "\t\t" + datetime_from_filename.strftime('%Y-%m-%d %H:%M:%S'))


