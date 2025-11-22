"""
API接口模块
"""

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    文件上传接口
    """
    file = request.files.get('file')
    if file:
        file.save(f'/uploads/{file.filename}')
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    获取用户信息
    """
    from src.database import get_user_by_id
    user = get_user_by_id(user_id)
    if user:
        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "balance": user[3]
        })
    return jsonify({"error": "User not found"}), 404

@app.route('/api/external', methods=['POST'])
def call_external_api():
    """
    调用外部API
    """
    data = request.json
    response = requests.post('https://api.example.com/endpoint', json=data)
    return jsonify(response.json())

@app.route('/api/data', methods=['GET'])
def get_data():
    """
    获取数据
    """
    from src.database import query_user_data
    all_data = query_user_data("SELECT * FROM users")
    return jsonify(all_data)

@app.route('/api/log', methods=['POST'])
def log_event():
    """
    记录日志
    """
    event = request.json
    print(f"Event logged: {event}")
    return jsonify({"status": "logged"})

