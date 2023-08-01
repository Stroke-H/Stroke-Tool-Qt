# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.11.3
@Time    :   2023/5/29 5:34 PM
@Desc    :   读取yml文件方法
"""
import yaml


def read_yaml(path):
    with open(path, 'r+', encoding='utf-8') as file:
        dict_data = yaml.load(stream=file, Loader=yaml.FullLoader)
        return dict_data
