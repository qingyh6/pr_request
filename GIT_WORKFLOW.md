# Git 工作流说明

## 标准工作流程

### 第一步：初始化仓库并上传主分支（main/master）

```bash
# 1. 初始化Git仓库
git init

# 2. 添加main_branch目录下的文件到仓库
# 将main_branch/src下的文件复制到项目根目录的src目录
cp -r main_branch/src ./src

# 3. 提交到main分支
git add .
git commit -m "Initial commit: 主分支代码"

# 4. 创建远程仓库并推送
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

### 第二步：创建feature分支并提交PR代码

```bash
# 1. 创建并切换到feature分支
git checkout -b feature/pr-risk-test

# 2. 用pr_branch的代码替换当前代码
# 删除旧的src目录，复制pr_branch/src
rm -rf src
cp -r pr_branch/src ./src

# 3. 提交变更
git add .
git commit -m "feat: 功能更新和代码优化"

# 4. 推送feature分支
git push -u origin feature/pr-risk-test
```

### 第三步：创建Pull Request

在Git平台（GitHub/GitLab等）上：
1. 创建从 `feature/pr-risk-test` 到 `main` 的Pull Request
2. 风险评估系统会自动分析PR中的代码变更
3. 系统会对比main分支和feature分支的差异，识别风险问题

## 目录结构说明

- `main_branch/` - 这是**参考代码**，代表主分支应该有的安全代码
- `pr_branch/` - 这是**参考代码**，代表PR分支中包含问题的代码

**实际使用时**：
- 首次提交：将 `main_branch/src/` 的内容作为 `src/` 提交到main分支
- PR提交：将 `pr_branch/src/` 的内容替换 `src/` 后提交到feature分支

## 快速脚本

### Windows PowerShell 脚本

```powershell
# 初始化主分支
# 1. 复制main_branch代码到src
Copy-Item -Path "main_branch\src" -Destination "src" -Recurse -Force

# 2. Git操作
git init
git add .
git commit -m "Initial commit: 主分支代码"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main

# 创建PR分支
# 1. 创建feature分支
git checkout -b feature/pr-risk-test

# 2. 替换为pr_branch代码
Remove-Item -Path "src" -Recurse -Force
Copy-Item -Path "pr_branch\src" -Destination "src" -Recurse -Force

# 3. 提交并推送
git add .
git commit -m "feat: 功能更新和代码优化"
git push -u origin feature/pr-risk-test
```

### Linux/Mac 脚本

```bash
#!/bin/bash
# 初始化主分支
cp -r main_branch/src ./src
git init
git add .
git commit -m "Initial commit: 主分支代码"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main

# 创建PR分支
git checkout -b feature/pr-risk-test
rm -rf src
cp -r pr_branch/src ./src
git add .
git commit -m "feat: 功能更新和代码优化"
git push -u origin feature/pr-risk-test
```

## 注意事项

1. `main_branch/` 和 `pr_branch/` 目录只是**参考代码**，不会直接提交到Git
2. 实际提交的是项目根目录下的 `src/` 目录
3. 在创建PR之前，确保feature分支是基于最新的main分支创建的
4. 风险评估系统会对比PR中的变更，自动识别风险问题

