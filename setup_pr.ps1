# PowerShell脚本：创建PR分支
# 使用方法：在项目根目录运行 .\setup_pr.ps1

Write-Host "正在创建PR分支..." -ForegroundColor Green

# 检查是否在Git仓库中
if (-not (Test-Path ".git")) {
    Write-Host "✗ 错误：当前目录不是Git仓库，请先运行setup_main.ps1" -ForegroundColor Red
    exit 1
}

# 检查是否在main分支
$currentBranch = git branch --show-current
if ($currentBranch -ne "main" -and $currentBranch -ne "master") {
    Write-Host "⚠ 警告：当前不在main分支，正在切换到main分支..." -ForegroundColor Yellow
    git checkout main 2>$null
    if ($LASTEXITCODE -ne 0) {
        git checkout master 2>$null
    }
}

# 创建feature分支
$branchName = "feature/pr-risk-test"
git checkout -b $branchName 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 已创建并切换到 $branchName 分支" -ForegroundColor Green
} else {
    Write-Host "⚠ 分支已存在，正在切换..." -ForegroundColor Yellow
    git checkout $branchName
}

# 复制pr_branch代码到src目录
if (Test-Path "pr_branch\src") {
    if (Test-Path "src") {
        Remove-Item -Path "src" -Recurse -Force
    }
    Copy-Item -Path "pr_branch\src" -Destination "src" -Recurse -Force
    Write-Host "✓ 已复制pr_branch代码到src目录" -ForegroundColor Green
} else {
    Write-Host "✗ 错误：找不到pr_branch\src目录" -ForegroundColor Red
    exit 1
}

# 添加文件
git add .
Write-Host "✓ 已添加文件到暂存区" -ForegroundColor Green

# 提交变更
git commit -m "feat: 功能更新和代码优化"
Write-Host "✓ 已提交变更" -ForegroundColor Green

Write-Host ""
Write-Host "下一步操作：" -ForegroundColor Cyan
Write-Host "1. 推送到远程: git push -u origin $branchName" -ForegroundColor Yellow
Write-Host "2. 在Git平台上创建Pull Request" -ForegroundColor Yellow

