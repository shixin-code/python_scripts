# -*- coding: utf-8 -*-

'''
需要强制更新图片原始时间戳的文件列表，该集合中的文件不检查原始时间，直接尝试从文件外解析时间更新原始时间
有些文件存在原始时间，但原始时间不正确，则添加到该列表中
'''
force_update_original_datetime_files = set([
    "exmaple.jpg"

])
