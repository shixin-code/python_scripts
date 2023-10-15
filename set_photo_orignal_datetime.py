# -*- coding: utf-8 -*-
'''
检查照片是否有原始日期时间, 如果没有通过解析照片文件名的时间, 然后设置为照片的EXIF中的原始日期时间
用法: python set_photo_orignal_datetime.py F:/photo/store/directory
'''

import os, sys
import re
from datetime import datetime
import piexif

def parse_datetime_from_filename(file_name):
    ''' 从文件名中解析出时间 '''
    pattern = r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}'
    match = re.search(pattern, file_name)
    if match:
        date_time_str = match.group()
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d_%H-%M-%S')
        return date_time
    else:
        return None

def check_set_image_exif_datetime_orginal(dir, file_name):
    ''' 检查并设置图片的EXIF中的拍摄时间 '''
    file_path = os.path.join(dir, file_name)

    exif_dict = piexif.load(file_path).get('Exif')
    if exif_dict.get(piexif.ExifIFD.DateTimeOriginal) is not None:
        print(file_name + " DateTimeOriginal: " + exif_dict.get(piexif.ExifIFD.DateTimeOriginal).decode("utf-8"))
        return

    ## 没有拍摄时间，从文件名中解析出来
    date_time = parse_datetime_from_filename(file_name)
    if date_time is not None:
        date_time_str = date_time.strftime('%Y:%m:%d %H:%M:%S')
        exif_dict[piexif.ExifIFD.DateTimeOriginal] = date_time_str.encode('utf-8')
        print("set " + file_name + " DateTimeOriginal...")
        data = {}
        data["Exif"] = exif_dict
        exif_dict_bytes = piexif.dump(data)
        piexif.insert(exif_dict_bytes, file_path)
    else:
        print(file_name + " parse datetime from filename failed!")


dir_path = sys.argv[1]
for filename in os.listdir(dir_path):
    check_set_image_exif_datetime_orginal(dir_path, filename)

