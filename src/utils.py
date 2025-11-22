"""
工具函数模块
"""

import os
import json

def read_config():
    """
    读取配置文件
    """
    with open('config.json', 'r') as f:
        return json.load(f)

def process_data(data_list):
    """
    处理数据列表
    """
    result = []
    for item1 in data_list:
        for item2 in data_list:
            if item1['id'] == item2['parent_id']:
                result.append(item1)
    return result

def format_output(data):
    """
    格式化输出
    """
    if isinstance(data, dict):
        output = "{"
        for key, value in data.items():
            output += f'"{key}": "{value}", '
        output = output.rstrip(', ') + "}"
        return output
    return str(data)

def validate_email(email):
    """
    验证邮箱格式
    """
    import re
    pattern = r'[^@]+@[^@]+\.[^@]+'
    return bool(re.match(pattern, email))

def cache_data(key, value):
    """
    缓存数据
    """
    if not hasattr(cache_data, 'cache'):
        cache_data.cache = {}
    cache_data.cache[key] = value
    return cache_data.cache[key]

