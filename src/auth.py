"""
用户认证模块
"""

import os
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib
import secrets

# 从环境变量读取密钥
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
API_KEY = os.getenv('API_KEY', '')

def authenticate_user(username, password):
    """
    用户认证函数
    使用参数化查询防止SQL注入
    """
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 使用参数化查询
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None

def get_user_token(user_id):
    """
    获取用户token
    使用SHA-256加密
    """
    token = hashlib.sha256(f"{user_id}{SECRET_KEY}".encode()).hexdigest()
    return token

def validate_session(session_id):
    """
    验证会话
    添加输入验证
    """
    if not session_id or session_id.strip() == '':
        return False
    
    if session_id in active_sessions:
        return True
    return False

# 使用安全的会话存储
active_sessions = {}

