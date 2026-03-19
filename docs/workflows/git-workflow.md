# Git 工作流

本文档描述项目的 Git 使用规范。

## 分支策略

**主要分支：**
- `main` - 稳定版本

**功能分支：**
- `feature/topic-name` - 新增学习主题
- `docs/update-name` - 文档更新
- `fix/issue-name` - 修复问题

## 工作流程

### 开始新工作

```bash
# 从 main 创建功能分支
git checkout main
git pull
git checkout -b feature/your-work

# 进行工作
# ... 编辑文件 ...

# 提交更改
git add .
git commit -m "feat: description"

# 推送
git push -u origin feature/your-work
```

### 提交信息规范

使用 Conventional Commits 格式：

```
<type>: <description>
```

类型（type）：
- `feat` - 新功能
- `docs` - 文档更新
- `fix` - 修复 bug
- `refactor` - 重构
- `style` - 格式调整
- `test` - 测试
- `chore` - 构建/工具配置

示例：
```bash
git commit -m "feat: add basics topic notes"
git commit -m "docs: update workflow guide"
git commit -m "fix: broken link in readme"
```

### 合并到 main

```bash
git checkout main
git pull
git merge feature/your-work
git push
```

## 最佳实践

- ✅ 所有改动使用功能分支（除了纯 typo 修正）
- ✅ 频繁提交，小步前进
- ✅ 写清晰的提交信息
- ✅ 合并前保持 main 分支稳定

相关文档：
- [开发工作流](development-workflow.md)
- [Claude Code 最佳实践](claude-code-best-practices.md)
