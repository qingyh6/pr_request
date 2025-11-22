"""
工具函数模块
"""

import os
import json
from typing import List, Dict, Any

def read_config():
    """
    读取配置文件
    添加异常处理
    """
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def process_data(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    处理数据列表
    使用字典优化为O(n)复杂度
    """
    result = []
    # 使用字典建立索引，优化性能
    parent_map = {item['id']: item for item in data_list}
    
    for item in data_list:
        parent_id = item.get('parent_id')
        if parent_id and parent_id in parent_map:
            result.append(item)
    return result

def format_output(data: Any) -> str:
    """
    格式化输出
    使用json模块避免重复代码
    """
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False)
    return str(data)

def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    使用更严格的正则表达式
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

class LRUCache:
    """LRU缓存实现"""
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    
    def set(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)

# 使用LRU缓存
_cache = LRUCache()

def cache_data(key: str, value: Any) -> Any:
    """
    缓存数据
    使用LRU缓存机制
    """
    _cache.set(key, value)
    return _cache.get(key)

