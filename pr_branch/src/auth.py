"""
用户认证模块
"""

import os

ADMIN_PASSWORD = "admin123"
SECRET_KEY = "my_secret_key_12345"
API_KEY = "sk-1234567890abcdef"

def authenticate_user(username, password):
    """
    用户认证函数
    """
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    
    conn.close()
    return result is not None

def get_user_token(user_id):
    """
    获取用户token
    """
    import hashlib
    token = hashlib.md5(f"{user_id}{SECRET_KEY}".encode()).hexdigest()
    return token

def validate_session(session_id):
    """
    验证会话
    """
    if session_id in active_sessions:
        return True
    return False

active_sessions = {}
user_credentials = {
    "admin": "password123",
    "user1": "qwerty"
}

