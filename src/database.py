"""
数据库操作模块
"""

import sqlite3
import os

def get_user_by_id(user_id):
    """
    根据ID获取用户
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_user_balance(user_id, amount):
    """
    更新用户余额
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user_id))
    cursor.execute("INSERT INTO transactions (user_id, amount) VALUES (?, ?)", (user_id, amount))
    
    conn.commit()
    conn.close()

def delete_user(user_id):
    """
    删除用户
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def query_user_data(query_string):
    """
    查询用户数据
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(query_string)
    result = cursor.fetchall()
    conn.close()
    return result

