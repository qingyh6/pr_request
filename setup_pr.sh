#!/bin/bash
# Linux/Mac脚本：创建PR分支
# 使用方法：chmod +x setup_pr.sh && ./setup_pr.sh

echo "正在创建PR分支..."

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo "✗ 错误：当前目录不是Git仓库，请先运行setup_main.sh"
    exit 1
fi

# 检查是否在main分支
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
    echo "⚠ 警告：当前不在main分支，正在切换到main分支..."
    git checkout main 2>/dev/null || git checkout master 2>/dev/null
fi

# 创建feature分支
branch_name="feature/pr-risk-test"
git checkout -b $branch_name 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ 已创建并切换到 $branch_name 分支"
else
    echo "⚠ 分支已存在，正在切换..."
    git checkout $branch_name
fi

# 复制pr_branch代码到src目录
if [ -d "pr_branch/src" ]; then
    if [ -d "src" ]; then
        rm -rf src
    fi
    cp -r pr_branch/src ./src
    echo "✓ 已复制pr_branch代码到src目录"
else
    echo "✗ 错误：找不到pr_branch/src目录"
    exit 1
fi

# 添加文件
git add .
echo "✓ 已添加文件到暂存区"

# 提交变更
git commit -m "feat: 功能更新和代码优化"
echo "✓ 已提交变更"

echo ""
echo "下一步操作："
echo "1. 推送到远程: git push -u origin $branch_name"
echo "2. 在Git平台上创建Pull Request"

