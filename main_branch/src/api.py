"""
API接口模块
"""

from flask import Flask, request, jsonify
import requests
from functools import wraps
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB限制

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
EXTERNAL_API_URL = os.getenv('EXTERNAL_API_URL', 'https://api.example.com/endpoint')

def require_auth(f):
    """权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not validate_token(token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def validate_token(token):
    """验证token"""
    # 实现token验证逻辑
    return True

@app.route('/api/upload', methods=['POST'])
@require_auth
def upload_file():
    """
    文件上传接口
    添加文件类型和大小验证
    """
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected"}), 400
    
    # 验证文件类型
    if not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "File type not allowed"}), 400
    
    # 验证文件大小
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    if file_length > 10 * 1024 * 1024:  # 10MB
        return jsonify({"status": "error", "message": "File too large"}), 400
    
    file.seek(0)
    safe_filename = secure_filename(file.filename)
    file.save(f'/uploads/{safe_filename}')
    return jsonify({"status": "success"})

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    """生成安全的文件名"""
    import re
    filename = re.sub(r'[^\w\.-]', '', filename)
    return filename

@app.route('/api/user/<user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """
    获取用户信息
    添加访问控制
    """
    current_user_id = get_current_user_id(request)
    
    # 检查权限：只能查看自己的信息或管理员可以查看所有
    if current_user_id != user_id and not is_admin(current_user_id):
        return jsonify({"error": "Forbidden"}), 403
    
    from src.database import get_user_by_id
    user = get_user_by_id(user_id)
    if user:
        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2]
            # 不返回余额等敏感信息
        })
    return jsonify({"error": "User not found"}), 404

def get_current_user_id(request):
    """获取当前用户ID"""
    # 从token中解析用户ID
    return request.headers.get('User-Id', '')

def is_admin(user_id):
    """检查用户是否为管理员"""
    # 实现管理员检查逻辑
    return False

@app.route('/api/external', methods=['POST'])
@require_auth
def call_external_api():
    """
    调用外部API
    添加超时设置和重试机制
    """
    data = request.json
    try:
        response = requests.post(
            EXTERNAL_API_URL, 
            json=data,
            timeout=10,  # 10秒超时
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timeout"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['GET'])
@require_auth
def get_data():
    """
    获取数据
    添加分页功能
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    from src.database import query_user_data
    offset = (page - 1) * per_page
    # 使用分页查询
    all_data = query_user_data(f"SELECT * FROM users LIMIT {per_page} OFFSET {offset}")
    return jsonify({
        "data": all_data,
        "page": page,
        "per_page": per_page
    })

@app.route('/api/log', methods=['POST'])
@require_auth
def log_event():
    """
    记录日志
    过滤敏感信息
    """
    event = request.json
    
    # 过滤敏感字段
    filtered_event = filter_sensitive_data(event)
    print(f"Event logged: {filtered_event}")
    return jsonify({"status": "logged"})

def filter_sensitive_data(data):
    """过滤敏感信息"""
    sensitive_keys = ['password', 'token', 'secret', 'key', 'credit_card']
    if isinstance(data, dict):
        return {k: '***' if any(sk in k.lower() for sk in sensitive_keys) else v 
                for k, v in data.items()}
    return data

