# -*- coding: utf-8 -*-
import os, re
from datetime import datetime
import piexif

def get_image_exif_datetime(dir, file_name):
    file_path = os.path.join(dir, file_name)

    exif_dict = piexif.load(file_path).get('Exif')
    if exif_dict.get(piexif.ExifIFD.DateTimeOriginal) is not None:
        ## 返回拍摄时间
        return exif_dict.get(piexif.ExifIFD.DateTimeOriginal).decode("utf-8")
    return None

def parse_datetime_from_filename(file_name):
    ''' 从文件名中解析出时间 '''
    date_time = None
    if file_name.startswith('mmexport'):
        '''文件名格式：mmexport1531666049849.jpg，一般是微信之前发送保存下来的图片'''
        mmexport_pattern = r'^mmexport(\d{13})\.jpg$'
        match = re.match(mmexport_pattern, file_name)
        if match:
            timestamp = int(match.group(1))
            date_time = datetime.fromtimestamp(timestamp / 1000.0)
    else:
        pattern = r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}'
        match = re.search(pattern, file_name)
        if match:
            date_time_str = match.group()
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d_%H-%M-%S')
    
    return date_time

def set_image_exif_datetime_orginal(file_path, date_time):
    if date_time is None:
        return False

    exif_dict = piexif.load(file_path).get('Exif')
    date_time_str = date_time.strftime('%Y:%m:%d %H:%M:%S')
    exif_dict[piexif.ExifIFD.DateTimeOriginal] = date_time_str.encode('utf-8')
    data = {}
    data["Exif"] = exif_dict
    exif_dict_bytes = piexif.dump(data)
    piexif.insert(exif_dict_bytes, file_path)