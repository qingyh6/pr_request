"""
主应用入口
用于演示和测试
"""

from flask import Flask
from src.api import app

if __name__ == '__main__':
    print("启动应用服务器...")
    print("注意：本仓库包含多个风险问题，仅用于测试风险评估系统")
    app.run(debug=True, port=5000)

