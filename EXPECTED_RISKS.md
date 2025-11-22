# 预期风险问题清单（用于验证）

本文档列出了PR #001中应该被风险评估系统检测到的风险问题，用于验证系统的准确性。

## P0级别 - 致命风险（7个）

### 1. 硬编码密码和密钥
- **文件**: `pr_branch/src/auth.py:5-7`
- **问题**: 密码、密钥和API密钥硬编码在代码中
- **对比**: `main_branch/src/auth.py` 使用环境变量

### 2. SQL注入漏洞
- **文件**: `pr_branch/src/auth.py:18`
- **问题**: 直接拼接用户输入到SQL语句
- **对比**: `main_branch/src/auth.py:18` 使用参数化查询

### 3. 弱加密算法
- **文件**: `pr_branch/src/auth.py:25`
- **问题**: 使用MD5进行加密（已被破解）
- **对比**: `main_branch/src/auth.py:30` 使用SHA-256

### 4. 缺少输入验证
- **文件**: `pr_branch/src/auth.py:31`
- **问题**: 没有检查session_id是否为None或空
- **对比**: `main_branch/src/auth.py:35-36` 有输入验证

### 5. 全局变量存储敏感信息
- **文件**: `pr_branch/src/auth.py:36-40`
- **问题**: 密码以明文形式存储在全局变量中
- **对比**: `main_branch/src/auth.py` 没有此问题

### 6. 危险操作缺少权限检查
- **文件**: `pr_branch/src/database.py:28`
- **问题**: 删除用户操作没有检查权限
- **对比**: `main_branch/src/database.py:38` 有权限检查

### 7. SQL命令注入
- **文件**: `pr_branch/src/database.py:40`
- **问题**: 允许执行任意SQL查询字符串
- **对比**: `main_branch/src/database.py:50` 使用预定义查询

## P1级别 - 高风险（7个）

### 1. 数据库连接资源泄漏
- **文件**: `pr_branch/src/database.py:12`
- **问题**: 异常情况下数据库连接可能未正确关闭
- **对比**: `main_branch/src/database.py` 使用上下文管理器

### 2. 缺少事务处理
- **文件**: `pr_branch/src/database.py:23`
- **问题**: 多个数据库操作没有使用事务
- **对比**: `main_branch/src/database.py:28` 使用事务

### 3. 缺少请求大小限制
- **文件**: `pr_branch/src/api.py:9`
- **问题**: Flask应用没有设置MAX_CONTENT_LENGTH
- **对比**: `main_branch/src/api.py:11` 设置了16MB限制

### 4. 缺少文件验证
- **文件**: `pr_branch/src/api.py:15`
- **问题**: 文件上传没有检查类型、大小和文件名
- **对比**: `main_branch/src/api.py:25-45` 有完整的文件验证

### 5. 缺少访问控制
- **文件**: `pr_branch/src/api.py:22`
- **问题**: 任何用户都可以查看其他用户的敏感信息
- **对比**: `main_branch/src/api.py:48` 有权限检查

### 6. 缺少超时设置
- **文件**: `pr_branch/src/api.py:35`
- **问题**: 外部API调用没有超时设置
- **对比**: `main_branch/src/api.py:75` 设置了10秒超时

### 7. 硬编码URL
- **文件**: `pr_branch/src/api.py:36`
- **问题**: API URL硬编码在代码中
- **对比**: `main_branch/src/api.py:12` 使用环境变量

## P2级别 - 常规风险（9个）

### 1. 缺少分页
- **文件**: `pr_branch/src/api.py:44`
- **问题**: 数据查询接口没有分页功能
- **对比**: `main_branch/src/api.py:88` 有分页功能

### 2. 日志包含敏感信息
- **文件**: `pr_branch/src/api.py:52`
- **问题**: 日志可能记录密码、token等敏感信息
- **对比**: `main_branch/src/api.py:100` 有敏感信息过滤

### 3. 文件操作缺少异常处理
- **文件**: `pr_branch/src/utils.py:11`
- **问题**: 文件不存在时会抛出异常
- **对比**: `main_branch/src/utils.py:12-17` 有异常处理

### 4. 低效算法
- **文件**: `pr_branch/src/utils.py:19`
- **问题**: 使用O(n²)复杂度的嵌套循环
- **对比**: `main_branch/src/utils.py:20` 使用O(n)算法

### 5. 代码重复
- **文件**: `pr_branch/src/utils.py:28`
- **问题**: 格式化逻辑重复，应该使用json模块
- **对比**: `main_branch/src/utils.py:33` 使用json.dumps

### 6. 简单正则表达式
- **文件**: `pr_branch/src/utils.py:40`
- **问题**: 邮箱验证正则过于简单
- **对比**: `main_branch/src/utils.py:45` 使用更严格的正则

### 7. 缓存无过期机制
- **文件**: `pr_branch/src/utils.py:48`
- **问题**: 缓存数据永远不会过期
- **对比**: `main_branch/src/utils.py:47` 使用LRU缓存

### 8. 缺少类型提示
- **问题**: 多个函数缺少类型注解
- **对比**: `main_branch/src/utils.py` 有类型提示

### 9. 缺少装饰器保护
- **文件**: `pr_branch/src/api.py`
- **问题**: API接口缺少认证装饰器
- **对比**: `main_branch/src/api.py` 使用@require_auth装饰器

## 统计摘要

- **P0级别**: 7个问题（需要立即修复，阻塞合并）
- **P1级别**: 7个问题（需要QA审查）
- **P2级别**: 9个问题（代码质量改进）
- **总计**: 23个风险问题

