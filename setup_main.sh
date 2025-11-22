#!/bin/bash
# Linux/Mac脚本：初始化主分支
# 使用方法：chmod +x setup_main.sh && ./setup_main.sh

echo "正在设置主分支..."

# 复制main_branch代码到src目录
if [ -d "main_branch/src" ]; then
    if [ -d "src" ]; then
        rm -rf src
    fi
    cp -r main_branch/src ./src
    echo "✓ 已复制main_branch代码到src目录"
else
    echo "✗ 错误：找不到main_branch/src目录"
    exit 1
fi

# 初始化Git（如果还没有）
if [ ! -d ".git" ]; then
    git init
    echo "✓ 已初始化Git仓库"
fi

# 添加文件
git add .
echo "✓ 已添加文件到暂存区"

# 检查是否有未提交的变更
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "Initial commit: 主分支代码"
    echo "✓ 已提交到本地仓库"
else
    echo "ℹ 没有新的变更需要提交"
fi

echo ""
echo "下一步操作："
echo "1. 添加远程仓库: git remote add origin <your-repo-url>"
echo "2. 推送到远程: git push -u origin main"

