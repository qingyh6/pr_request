# 测试仓库 - PR风险评估系统

这是一个用于测试PR风险评估功能的测试仓库。

## 项目结构

```
.
├── main_branch/        # 参考代码：原始仓库代码（main分支）
│   └── src/
│       ├── auth.py
│       ├── database.py
│       ├── api.py
│       └── utils.py
├── pr_branch/          # 参考代码：PR变更代码（feature分支）
│   └── src/
│       ├── auth.py
│       ├── database.py
│       ├── api.py
│       └── utils.py
├── src/                # 实际提交的代码（由脚本生成）
├── setup_main.ps1      # Windows: 初始化主分支脚本
├── setup_pr.ps1        # Windows: 创建PR分支脚本
├── setup_main.sh       # Linux/Mac: 初始化主分支脚本
├── setup_pr.sh         # Linux/Mac: 创建PR分支脚本
├── PR_CHANGES.md       # PR变更说明
├── GIT_WORKFLOW.md     # Git工作流详细说明
└── README.md
```

## 快速开始

### 方式一：使用脚本（推荐）

#### Windows PowerShell

```powershell
# 第一步：初始化主分支
.\setup_main.ps1

# 添加远程仓库并推送
git remote add origin <your-repo-url>
git push -u origin main

# 第二步：创建PR分支
.\setup_pr.ps1

# 推送PR分支
git push -u origin feature/pr-risk-test
```

#### Linux/Mac

```bash
# 第一步：初始化主分支
chmod +x setup_main.sh setup_pr.sh
./setup_main.sh

# 添加远程仓库并推送
git remote add origin <your-repo-url>
git push -u origin main

# 第二步：创建PR分支
./setup_pr.sh

# 推送PR分支
git push -u origin feature/pr-risk-test
```

### 方式二：手动操作

详细步骤请参考 [GIT_WORKFLOW.md](GIT_WORKFLOW.md)

## 工作流程说明

1. **首次提交**：将 `main_branch/src/` 的代码作为 `src/` 提交到 `main` 分支
2. **创建PR**：创建 `feature/pr-risk-test` 分支，将 `pr_branch/src/` 的代码替换 `src/` 后提交
3. **风险评估**：系统自动对比PR变更，识别风险问题（P0/P1/P2）

## 风险评估

风险评估系统会对比PR中的代码变更，自动识别：
- **P0级别**：致命风险（需要立即修复，阻塞合并）
- **P1级别**：高风险（需要QA审查）
- **P2级别**：常规风险（代码质量改进）

## 注意事项

- `main_branch/` 和 `pr_branch/` 只是**参考代码目录**，不会直接提交到Git
- 实际提交的是项目根目录下的 `src/` 目录
- PR代码中的问题没有在注释中标注，需要风险评估系统自动发现
- 所有问题都是通过代码对比和AST分析来识别
- 本仓库仅用于测试风险评估功能
