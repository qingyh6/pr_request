# PowerShell脚本：初始化主分支
# 使用方法：在项目根目录运行 .\setup_main.ps1

Write-Host "正在设置主分支..." -ForegroundColor Green

# 复制main_branch代码到src目录
if (Test-Path "main_branch\src") {
    if (Test-Path "src") {
        Remove-Item -Path "src" -Recurse -Force
    }
    Copy-Item -Path "main_branch\src" -Destination "src" -Recurse -Force
    Write-Host "✓ 已复制main_branch代码到src目录" -ForegroundColor Green
} else {
    Write-Host "✗ 错误：找不到main_branch\src目录" -ForegroundColor Red
    exit 1
}

# 初始化Git（如果还没有）
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✓ 已初始化Git仓库" -ForegroundColor Green
}

# 添加文件
git add .
Write-Host "✓ 已添加文件到暂存区" -ForegroundColor Green

# 检查是否有未提交的变更
$status = git status --porcelain
if ($status) {
    git commit -m "Initial commit: 主分支代码"
    Write-Host "✓ 已提交到本地仓库" -ForegroundColor Green
} else {
    Write-Host "ℹ 没有新的变更需要提交" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "下一步操作：" -ForegroundColor Cyan
Write-Host "1. 添加远程仓库: git remote add origin <your-repo-url>" -ForegroundColor Yellow
Write-Host "2. 推送到远程: git push -u origin main" -ForegroundColor Yellow

