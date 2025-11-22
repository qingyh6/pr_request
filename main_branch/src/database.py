"""
数据库操作模块
"""

import sqlite3
import os
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """数据库连接上下文管理器"""
    conn = sqlite3.connect('app.db')
    try:
        yield conn
    finally:
        conn.close()

def get_user_by_id(user_id):
    """
    根据ID获取用户
    使用上下文管理器确保连接关闭
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
    return result

def update_user_balance(user_id, amount):
    """
    更新用户余额
    使用事务确保数据一致性
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN")
            cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user_id))
            cursor.execute("INSERT INTO transactions (user_id, amount) VALUES (?, ?)", (user_id, amount))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

def delete_user(user_id, current_user_role):
    """
    删除用户
    添加权限检查
    """
    if current_user_role != 'admin':
        raise PermissionError("Only admin can delete users")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

def query_user_data(user_id):
    """
    查询用户数据
    使用预定义查询，防止SQL注入
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchall()
    return result

