# 开发工作流基础结构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立完整的 Claude Code 学习项目基础结构，包括目录组织、配置文件、文档模板和自动化工具

**Architecture:** 基于主题驱动的文档型项目结构，使用 Python 进行代码示例开发，通过 pre-commit 实现代码和文档质量自动化检查

**Tech Stack:** Python 3.11+, Markdown, Git, Pre-commit, Black, Flake8, MyPy, PyYAML

---

## 文件结构概览

本计划将创建以下文件：

**配置文件：**
- `.gitignore` - Git 忽略规则
- `pyproject.toml` - Python 项目配置
- `.pre-commit-config.yaml` - Pre-commit 钩子配置

**目录结构：**
- `docs/` - 文档根目录
  - `topics/` - 学习主题目录
  - `workflows/` - 工作流程文档
  - `assets/` - 图片资源
  - `README.md` - 文档导航
- `examples/` - 独立示例
- `tools/` - 工具脚本
- `tests/` - 测试代码

**文档模板：**
- `docs/topics/.templates/README.md` - 主题模板
- `docs/topics/.templates/notes.md` - 笔记模板

**工具脚本：**
- `tools/check-links.py` - 链接检查脚本

---

## Task 1: 创建基础目录结构

**Files:**
- Create: `docs/getting-started/`
- Create: `docs/topics/`
- Create: `docs/workflows/`
- Create: `docs/assets/`
- Create: `examples/`
- Create: `tools/`
- Create: `tests/`

- [ ] **Step 1: 创建文档子目录**

```bash
mkdir -p docs/getting-started
mkdir -p docs/topics
mkdir -p docs/workflows
mkdir -p docs/assets
```

- [ ] **Step 2: 创建其他目录**

```bash
mkdir -p examples
mkdir -p tools
mkdir -p tests
```

- [ ] **Step 3: 验证目录创建**

```bash
ls -la docs/
ls -la examples/
ls -la tools/
ls -la tests/
```
Expected: 所有目录都已创建

- [ ] **Step 4: 提交目录结构**

```bash
git add docs/ examples/ tools/ tests/
git commit -m "feat: create base directory structure"
```

---

## Task 2: 安装 Python 开发依赖

**Files:**
- Create: `requirements.txt` (可选，用于 pip 安装)
- Modify: Python environment

- [ ] **Step 1: 创建虚拟环境（推荐）**

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

- [ ] **Step 2: 安装开发依赖**

```bash
# 使用 pip install -e 安装项目为可编辑模式
pip install -e ".[dev]"

# 验证安装
black --version
flake8 --version
mypy --version
pre-commit --version
```
Expected: 显示各工具的版本号

- [ ] **Step 3: 安装额外依赖**

```bash
# 安装 PyYAML（用于 YAML 验证）
pip install pyyaml

# 验证
python3 -c "import yaml; print('✅ PyYAML installed')"
```
Expected: 显示 "✅ PyYAML installed"

- [ ] **Step 4: 提交依赖配置**

```bash
git add pyproject.toml
git commit -m "chore: add project dependencies configuration"
```

---

## Task 3: 创建 .gitignore 配置

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: 创建 .gitignore 文件**

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Claude Code
.claude/

# Logs
*.log

# Temporary files
*.tmp
temp/
EOF
```

- [ ] **Step 2: 验证 .gitignore 内容**

```bash
cat .gitignore
```
Expected: 显示所有忽略规则

- [ ] **Step 3: 提交 .gitignore**

```bash
git add .gitignore
git commit -m "chore: add gitignore configuration"
```

---

## Task 4: 创建 pyproject.toml 配置

**Files:**
- Create: `pyproject.toml`

- [ ] **Step 1: 创建 pyproject.toml**

```bash
cat > pyproject.toml << 'EOF'
[project]
name = "claude-code-study"
version = "0.1.0"
description = "Claude Code 学习项目"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "black>=24.1.0",
    "flake8>=7.0.0",
    "mypy>=1.8.0",
    "pre-commit>=3.6.0",
    "pyyaml>=6.0.0",
]

[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
EOF
```

- [ ] **Step 2: 验证 pyproject.toml 语法**

```bash
python3 -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
```
Expected: 无错误输出

- [ ] **Step 3: 提交 pyproject.toml**

```bash
git add pyproject.toml
git commit -m "chore: add pyproject.toml configuration"
```

---

## Task 5: 创建 pre-commit 配置

**Files:**
- Create: `.pre-commit-config.yaml`

- [ ] **Step 1: 创建 pre-commit 配置文件**

```bash
cat > .pre-commit-config.yaml << 'EOF'
repos:
  # 通用检查
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-toml

  # Python 代码格式化
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.11

  # Python 代码检查
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203']

  # Python 类型检查
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: []
        exclude: ^tests/
EOF
```

- [ ] **Step 2: 验证 YAML 语法**

```bash
python3 -c "import yaml; yaml.safe_load(open('.pre-commit-config.yaml'))"
```
Expected: 无错误输出

- [ ] **Step 3: 安装 pre-commit hooks**

```bash
pre-commit install
```
Expected: 显示 "pre-commit installed"

- [ ] **Step 4: 测试 pre-commit**

```bash
pre-commit run --all-files
```
Expected: 所有检查通过（可能没有文件可检查）

- [ ] **Step 5: 提交 pre-commit 配置**

```bash
git add .pre-commit-config.yaml
git commit -m "chore: add pre-commit configuration"
```

---

## Task 6: 创建文档模板目录和模板文件

**Files:**
- Create: `docs/topics/.templates/`
- Create: `docs/topics/.templates/README.md`
- Create: `docs/topics/.templates/notes.md`
- Create: `docs/topics/.templates/example.py`

- [ ] **Step 1: 创建模板目录**

```bash
mkdir -p docs/topics/.templates
```

- [ ] **Step 2: 创建主题 README 模板**

```bash
cat > docs/topics/.templates/README.md << 'EOF'
# 主题名称：[中文标题]

## 概述
[简要介绍这个主题的学习目标和内容]

## 前置知识
- [知识点 1](链接到其他主题)
- [知识点 2]

## 学习内容
1. [子主题 1](notes.md#子主题)
2. [子主题 2](notes.md#子主题)

## 实践项目
- [项目 1](practice/project1/) - 难度：⭐⭐☆☆☆
- [项目 2](practice/project2/) - 难度：⭐⭐⭐☆☆

## 代码示例
参见 [examples/](./examples/) 目录

## 参考资料
- [官方文档](链接)
- [相关资源](链接)

## 学习进度
- [ ] 阅读笔记
- [ ] 运行示例
- [ ] 完成实践项目
- [ ] 整理心得

---
最后更新：YYYY-MM-DD
EOF
```

- [ ] **Step 3: 创建学习笔记模板**

```bash
cat > docs/topics/.templates/notes.md << 'EOF'
# 学习笔记：[主题名称]

> 学习时间：YYYY-MM-DD
> 状态：进行中/已完成

## 核心概念

### 概念 1
**定义**：...
**理解**：...
**使用场景**：...

## 关键要点

1. **要点 1**
   - 详细说明
   - 代码示例（如果有）

2. **要点 2**
   - 详细说明

## 常见问题

### Q: 问题？
A: 解答...

## 实践笔记

记录实践过程中遇到的问题和解决方案...

## 相关链接
- [官方文档](链接)
- [相关主题](../其他主题/README.md)
EOF
```

- [ ] **Step 4: 创建代码示例模板**

```bash
cat > docs/topics/.templates/example.py << 'EOF'
#!/usr/bin/env python3
"""
示例名称：简短描述

这个示例演示了...
"""

from typing import List


def example_function(param: str) -> List[str]:
    """
    函数功能描述

    Args:
        param: 参数说明

    Returns:
        返回值说明

    Example:
        >>> example_function("test")
        ['result']
    """
    return [param]


if __name__ == "__main__":
    # 示例用法
    result = example_function("test")
    print(f"结果: {result}")
EOF
```

- [ ] **Step 5: 验证模板文件创建**

```bash
ls -la docs/topics/.templates/
```
Expected: 显示 README.md, notes.md, example.py

- [ ] **Step 6: 提交模板文件**

```bash
git add docs/topics/.templates/
git commit -m "feat: add document templates for topics"
```

---

## Task 7: 创建链接检查工具脚本

**Files:**
- Create: `tools/check-links.py`

- [ ] **Step 1: 创建链接检查脚本**

```bash
cat > tools/check-links.py << 'EOF'
#!/usr/bin/env python3
# Requires: Python 3.9+
"""
检查 Markdown 文档中的内部链接是否有效
"""
from __future__ import annotations

import re
import argparse
from pathlib import Path


def extract_links(markdown_file: Path) -> list[tuple[str, str]]:
    """提取 Markdown 文件中的所有链接"""
    content = markdown_file.read_text(encoding='utf-8')
    # 匹配 [text](path) 格式的链接
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, content)


def check_link(link: str, base_dir: Path) -> bool:
    """检查链接是否有效"""
    # 移除锚点
    path = link.split('#')[0]
    if not path or path.startswith('http'):
        return True

    target = base_dir / path
    return target.exists()


def main() -> None:
    parser = argparse.ArgumentParser(
        description='检查 Markdown 文档中的内部链接'
    )
    parser.add_argument('docs_dir', type=Path, help='文档目录')
    args = parser.parse_args()

    docs_dir = args.docs_dir
    if not docs_dir.exists():
        print(f"❌ 目录不存在: {docs_dir}")
        exit(1)

    all_links_ok = True

    for md_file in docs_dir.rglob('*.md'):
        links = extract_links(md_file)
        for text, link in links:
            if not check_link(link, md_file.parent):
                print(f"❌ {md_file.relative_to(docs_dir)}: [{text}]({link})")
                all_links_ok = False

    if all_links_ok:
        print("✅ 所有链接检查通过")
    else:
        exit(1)


if __name__ == '__main__':
    main()
EOF
```

- [ ] **Step 2: 设置脚本可执行权限**

```bash
chmod +x tools/check-links.py
```

- [ ] **Step 3: 验证脚本语法**

```bash
python3 -m py_compile tools/check-links.py
```
Expected: 无语法错误

- [ ] **Step 4: 测试脚本**

```bash
python3 tools/check-links.py docs/
```
Expected: 显示"✅ 所有链接检查通过"或列出无效链接

- [ ] **Step 5: 提交脚本**

```bash
git add tools/check-links.py
git commit -m "feat: add markdown link checker tool"
```

---

## Task 8: 创建文档导航和工作流程文档

**Files:**
- Create: `docs/README.md`
- Create: `docs/workflows/development-workflow.md`
- Create: `docs/workflows/git-workflow.md`
- Create: `docs/workflows/claude-code-best-practices.md`

- [ ] **Step 1: 创建文档导航**

```bash
cat > docs/README.md << 'EOF'
# Claude Code 学习文档

欢迎来到 Claude Code 学习项目文档中心！

## 快速导航

### 入门指南
- [安装指南](getting-started/installation.md)
- [基础使用](getting-started/basic-usage.md)
- [第一个项目](getting-started/first-project.md)

### 学习主题
参见 [topics/](./topics/) 目录，按编号顺序学习：

1. [基础主题](topics/01-basics/) - Claude Code 基础知识
2. [Agents](topics/02-agents/) - Agent 开发
3. [MCP 服务器](topics/03-mcp-servers/) - MCP 服务器开发
4. [高级主题](topics/04-advanced/) - 高级技巧和最佳实践

### 工作流程
- [开发工作流](workflows/development-workflow.md) - 项目开发流程
- [Git 工作流](workflows/git-workflow.md) - 版本控制最佳实践
- [Claude Code 最佳实践](workflows/claude-code-best-practices.md) - 使用技巧

## 文档规范

所有文档遵循统一的规范，参见 [开发工作流设计文档](../development-workflow-design.md)。

## 贡献指南

欢迎贡献内容！请遵循以下步骤：
1. 阅读工作流程文档
2. 创建功能分支
3. 使用提供的文档模板
4. 遵循代码和文档规范
5. 提交 Pull Request
EOF
```

- [ ] **Step 2: 创建开发工作流文档**

```bash
cat > docs/workflows/development-workflow.md << 'EOF'
# 开发工作流

本文档描述项目的开发工作流程。

## 项目结构

项目采用主题驱动的文档型结构：

```
claude-code-study/
├── docs/           # 主要文档
│   ├── topics/     # 学习主题（核心）
│   └── workflows/  # 工作流程文档
├── examples/       # 独立示例
├── tools/          # 工具脚本
└── tests/          # 测试代码
```

## 开始新主题

1. 在 `docs/topics/` 下创建新目录（使用编号前缀）
2. 复制模板文件从 `.templates/` 目录
3. 填充内容
4. 创建代码示例和实践项目
5. 提交代码

## 自动化检查

项目使用 pre-commit 进行自动化检查：

```bash
# 安装
pip install -e ".[dev]"
pre-commit install

# 手动运行
pre-commit run --all-files

# 检查文档链接
python tools/check-links.py docs/
```

## 相关文档

- [Git 工作流](git-workflow.md)
- [Claude Code 最佳实践](claude-code-best-practices.md)
- [完整设计文档](../development-workflow-design.md)
EOF
```

- [ ] **Step 3: 创建 Git 工作流文档**

```bash
cat > docs/workflows/git-workflow.md << 'EOF'
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
EOF
```

- [ ] **Step 4: 创建 Claude Code 最佳实践文档**

```bash
cat > docs/workflows/claude-code-best-practices.md << 'EOF'
# Claude Code 最佳实践

本文档总结使用 Claude Code 的最佳实践。

## 有效的提示词编写

### 1. 清晰的任务描述

✅ **好的做法：**
```
"创建一个 Python 函数，读取 CSV 文件并计算特定列的平均值"
```

❌ **不好的做法：**
```
"帮我处理数据"
```

### 2. 提供上下文

✅ **好的做法：**
```
"我正在学习 MCP 服务器的开发。请帮我创建一个简单的 MCP 服务器示例，
该服务器提供获取天气信息的功能。使用 Python 和官方 MCP SDK。"
```

### 3. 明确输出格式

✅ **好的做法：**
```
"请分析这段代码的性能问题，并以以下格式输出：
1. 问题列表
2. 每个问题的影响
3. 建议的优化方案"
```

### 4. 分步处理复杂任务

✅ **好的做法：**
```
"首先，帮我设计项目结构。然后我们再一步步实现各个功能。"
```

## 技能（Skills）使用指南

### 何时使用技能

1. **开发新功能** → `brainstorming` 技能
2. **修复 Bug** → `systematic-debugging` 技能
3. **执行计划** → `executing-plans` 技能
4. **代码审查** → `requesting-code-review` 技能

### 典型工作流程

```
新任务
  ↓
brainstorming (探索需求)
  ↓
writing-plans (制定计划)
  ↓
executing-plans (执行实现)
  ↓
requesting-code-review (代码审查)
  ↓
完成
```

## 协作最佳实践

### 增量开发
- 不要一次要求完成所有功能
- 分成小的、可验证的步骤
- 每步完成后测试和反馈

### 利用 CLAUDE.md
- 在 `CLAUDE.md` 中记录项目约定
- 包括代码风格、架构决策、工作流程
- Claude Code 会自动遵循

### 版本控制集成
- 让 Claude Code 帮助写提交信息
- 合并前请求代码审查

### 学习记录
- 让 Claude Code 帮助生成学习总结
- 记录遇到的问题和解决方案
- 定期整理学习笔记

## 提问技巧

### 探索性提问
```
"这个功能的实现有哪几种方式？各自的优缺点是什么？"
```

### 验证性提问
```
"我这样理解对吗：...？"
```

### 代码解释
```
"请解释这段代码的工作原理，特别是第 X 行的逻辑"
```

相关文档：
- [开发工作流](development-workflow.md)
- [Git 工作流](git-workflow.md)
- [完整设计文档](../../development-workflow-design.md)
EOF
```

- [ ] **Step 5: 验证文档创建**

```bash
ls -la docs/workflows/
```
Expected: 显示三个工作流文档

- [ ] **Step 6: 提交文档**

```bash
git add docs/
git commit -m "docs: add navigation and workflow documentation"
```

---

## Task 9: 更新项目 README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 读取当前 README**

```bash
cat README.md
```

- [ ] **Step 2: 备份原 README（如果有内容）**

```bash
if [ -s README.md ]; then
  cp README.md README.md.bak
fi
```

- [ ] **Step 3: 创建新的 README**

```bash
cat > README.md << 'EOF'
# Claude Code 学习项目

这是一个用于学习 Claude Code 的项目，记录学习过程、笔记和最佳实践。

## 项目概述

本项目采用结构化的主题驱动学习方式，每个学习主题包含：
- 📝 学习笔记
- 💻 代码示例
- 🚀 实践项目
- 📚 参考资源

## 快速开始

### 环境要求

- Python 3.11+
- Git
- Claude Code CLI

### 安装开发依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -e ".[dev]"

# 安装 pre-commit hooks
pre-commit install
```

## 项目结构

```
claude-code-study/
├── docs/           # 文档和笔记
│   ├── topics/     # 学习主题
│   └── workflows/  # 工作流程文档
├── examples/       # 独立示例
├── tools/          # 工具脚本
└── tests/          # 测试代码
```

## 文档导航

- 📖 [完整文档](docs/)
- 🚀 [快速入门](docs/getting-started/)
- 📋 [学习主题](docs/topics/)
- 🔧 [工作流程](docs/workflows/)
- 📐 [设计文档](docs/development-workflow-design.md)

## 开发工作流

本项目遵循规范的开发流程：

1. 创建功能分支：`git checkout -b feature/your-work`
2. 进行开发和文档编写
3. 运行自动化检查：`pre-commit run --all-files`
4. 提交代码：`git commit -m "feat: description"`
5. 推送并合并

详见 [开发工作流文档](docs/workflows/development-workflow.md)。

## 学习进度

- [ ] 基础主题
- [ ] Agent 开发
- [ ] MCP 服务器
- [ ] 高级技巧

## 贡献

欢迎贡献内容！请查看 [贡献指南](CONTRIBUTING.md)。

## 许可

MIT License

## 联系方式

- 维护者：ray
- 项目链接：[GitHub](https://github.com/yourusername/claude-code-study)

---

**注意**：这是一个学习项目，旨在探索 Claude Code 的最佳实践和学习方法。
EOF
```

- [ ] **Step 4: 验证 README**

```bash
cat README.md
```
Expected: 显示新的项目 README

- [ ] **Step 5: 提交 README 更新**

```bash
git add README.md
git commit -m "docs: update project README with comprehensive guide"
```

---

## Task 10: 创建第一个学习主题（示例）

**Files:**
- Create: `docs/topics/01-basics/`
- Create: `docs/topics/01-basics/README.md`
- Create: `docs/topics/01-basics/notes.md`
- Create: `docs/topics/01-basics/examples/`
- Create: `docs/topics/01-basics/examples/hello_claude.py`
- Create: `docs/topics/01-basics/practice/`
- Create: `docs/topics/01-basics/practice/hello-world/`
- Create: `docs/topics/01-basics/practice/hello-world/README.md`

- [ ] **Step 1: 创建主题目录**

```bash
mkdir -p docs/topics/01-basics/examples
mkdir -p docs/topics/01-basics/practice/hello-world
```

- [ ] **Step 2: 创建主题 README**

```bash
cat > docs/topics/01-basics/README.md << 'EOF'
# 主题名称：Claude Code 基础

## 概述

本主题介绍 Claude Code 的基础知识，包括安装、配置、基本使用方法和核心概念。

## 前置知识

- 基础的命令行操作
- Python 基础知识
- Git 基础操作

## 学习内容

1. [Claude Code 简介](notes.md#claude-code-简介)
2. [安装和配置](notes.md#安装和配置)
3. [基本使用](notes.md#基本使用)
4. [核心概念](notes.md#核心概念)

## 实践项目

- [Hello World](practice/hello-world/) - 难度：⭐☆☆☆☆
  - 第一次使用 Claude Code 完成简单任务

## 代码示例

参见 [examples/](./examples/) 目录

## 参考资料

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)

## 学习进度

- [ ] 阅读笔记
- [ ] 运行示例
- [ ] 完成实践项目
- [ ] 整理心得

---
最后更新：2026-03-19
EOF
```

- [ ] **Step 3: 创建学习笔记**

```bash
cat > docs/topics/01-basics/notes.md << 'EOF'
# 学习笔记：Claude Code 基础

> 学习时间：2026-03-19
> 状态：进行中

## 核心概念

### Claude Code 是什么？

**定义**：Claude Code 是 Anthropic 开发的官方 CLI 工具，让开发者能够在命令行中直接与 Claude AI 交互，用于辅助编程任务。

**理解**：它就像一个强大的编程助手，可以在终端中帮你：
- 编写和解释代码
- 调试和修复错误
- 重构和优化代码
- 编写文档和测试

**使用场景**：
- 日常开发工作
- 学习新技术
- 代码审查
- 问题诊断

## 关键要点

### 1. 安装方法

Claude Code 通过 npm 安装：

```bash
npm install -g @anthropic-ai/claude-code
```

### 2. 基本使用流程

1. **启动**：在项目目录运行 `claude`
2. **交互**：通过自然语言描述任务
3. **执行**：Claude 会分析代码并执行操作
4. **确认**：重要操作需要确认

### 3. 核心特性

- **上下文感知**：理解整个项目结构
- **工具使用**：可以读写文件、运行命令
- **技能系统**：提供专业化的工作流程
- **安全优先**：重要操作需要确认

### 4. 配置文件

项目中的 `CLAUDE.md` 文件可以：
- 定义项目特定的约定
- 说明代码风格和架构
- 描述工作流程

Claude Code 会自动读取并遵循这些指导。

## 常见问题

### Q: Claude Code 可以访问我的所有文件吗？

A: 是的，但它会谨慎操作。涉及写入、删除等重要操作时会请求确认。

### Q: 如何让 Claude Code 更好地理解我的项目？

A: 在 `CLAUDE.md` 中详细描述：
- 项目的目标和架构
- 代码风格约定
- 特殊的命令或工具

### Q: Claude Code 会自动提交代码吗？

A: 不会。它只会建议提交信息，实际提交需要你的确认。

## 实践笔记

待补充...

## 相关链接

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [开发工作流](../../workflows/development-workflow.md)
- [Git 工作流](../../workflows/git-workflow.md)
EOF
```

- [ ] **Step 4: 创建示例代码**

```bash
cat > docs/topics/01-basics/examples/hello_claude.py << 'EOF'
#!/usr/bin/env python3
"""
Hello Claude - 第一个示例

这是一个简单的示例，演示如何使用 Claude Code
来理解和改进代码。
"""


def greet(name: str) -> str:
    """
    生成问候语

    Args:
        name: 要问候的名字

    Returns:
        问候语字符串

    Example:
        >>> greet("Claude")
        'Hello, Claude!'
    """
    return f"Hello, {name}!"


def main() -> None:
    """主函数"""
    # 问候 Claude
    message = greet("Claude")
    print(message)

    # 可以尝试其他名字
    other_names = ["World", "Developer", "Learner"]
    for name in other_names:
        print(greet(name))


if __name__ == "__main__":
    main()
EOF
```

- [ ] **Step 5: 创建实践项目 README**

```bash
cat > docs/topics/01-basics/practice/hello-world/README.md << 'EOF'
# Hello World - 第一次使用 Claude Code

## 项目目标

通过这个简单的实践项目，熟悉 Claude Code 的基本使用流程。

## 任务说明

使用 Claude Code 完成以下任务：

1. **代码解释**
   - 让 Claude Code 解释 `examples/hello_claude.py` 的功能
   - 提示词："请解释 examples/hello_claude.py 这个文件"

2. **代码改进**
   - 让 Claude Code 添加错误处理
   - 提示词："请为 hello_claude.py 添加输入验证"

3. **测试编写**
   - 让 Claude Code 编写单元测试
   - 提示词："请为 hello_claude.py 编写单元测试"

4. **文档生成**
   - 让 Claude Code 生成使用文档
   - 提示词："请为 hello_claude.py 生成使用文档"

## 预期成果

完成这个项目后，你应该能够：
- ✅ 使用 Claude Code 解释代码
- ✅ 通过 Claude Code 改进代码
- ✅ 使用 Claude Code 编写测试
- ✅ 让 Claude Code 帮助写文档

## 提示

- 使用清晰、具体的提示词
- 一步步完成，不要一次要求太多
- 观察 Claude Code 的工作方式
- 记录有用的提示词模式

## 扩展练习

- 尝试让 Claude Code 重构代码
- 添加新的功能（如日志记录）
- 创建 CLI 界面

## 相关资源

- [学习笔记](../../notes.md)
- [代码示例](../../examples/hello_claude.py)
- [Claude Code 最佳实践](../../../workflows/claude-code-best-practices.md)
EOF
```

- [ ] **Step 6: 运行示例代码**

```bash
python3 docs/topics/01-basics/examples/hello_claude.py
```
Expected: 输出问候语

- [ ] **Step 7: 检查文档链接**

```bash
python3 tools/check-links.py docs/topics/01-basics/
```
Expected: 链接检查通过

- [ ] **Step 8: 提交第一个主题**

```bash
git add docs/topics/01-basics/
git commit -m "feat: add first learning topic - Claude Code basics"
```

---

## Task 11: 运行最终检查和验证

**Files:**
- All created files

- [ ] **Step 1: 检查项目结构**

```bash
# 尝试使用 tree 命令（如果可用）
if command -v tree &> /dev/null; then
    tree -L 3 -I '__pycache__|*.pyc|.git'
else
    # 备选方案：使用 find
    find . -type d -not -path '*/\.git/*' -not -path '*/__pycache__/*' -not -path '*/\.venv/*' | head -30
fi
```
Expected: 显示完整的项目结构

- [ ] **Step 2: 运行 pre-commit 检查**

```bash
pre-commit run --all-files
```
Expected: 所有检查通过（或自动修复问题）

- [ ] **Step 3: 检查文档链接**

```bash
python3 tools/check-links.py docs/
```
Expected: 所有链接有效

- [ ] **Step 4: 验证 Python 配置**

```bash
python3 -c "import tomllib; print('✅ pyproject.toml valid')"
```
Expected: 无错误

- [ ] **Step 5: 检查 Git 状态**

```bash
git status
```
Expected: 所有更改已提交

- [ ] **Step 6: 查看提交历史**

```bash
git log --oneline -10
```
Expected: 显示清晰的提交历史

- [ ] **Step 7: 创建最终标签（可选）**

```bash
git tag -a v0.1.0 -m "Initial project structure setup"

# 仅在有远程仓库时推送标签
if git remote get-url origin &> /dev/null; then
    git push origin v0.1.0
fi
```

- [ ] **Step 8: 生成项目摘要**

```bash
echo "# 项目摘要

## 已完成
- ✅ 基础目录结构
- ✅ Git 配置（.gitignore）
- ✅ Python 配置（pyproject.toml）
- ✅ Pre-commit 配置
- ✅ 文档模板
- ✅ 工具脚本（链接检查）
- ✅ 工作流程文档
- ✅ 第一个学习主题

## 下一步
- 开始使用 Claude Code 学习
- 根据实践调整工作流
- 添加更多学习主题

## 统计信息
" > PROJECT_SUMMARY.md

echo "- 目录数: $(find . -type d -not -path '*/\.git/*' | wc -l)"
echo "- 文件数: $(find . -type f -not -path '*/\.git/*' | wc -l)"
echo "- 代码行数: $(find . -name '*.py' -not -path '*/\.git/*' -exec cat {} \; | wc -l)"
echo "- 文档行数: $(find . -name '*.md' -not -path '*/\.git/*' -exec cat {} \; | wc -l)" >> PROJECT_SUMMARY.md
```

- [ ] **Step 9: 提交最终检查结果**

```bash
git add PROJECT_SUMMARY.md
git commit -m "docs: add project setup summary"
```

---

## 验证标准

完成所有任务后，项目应该满足：

- ✅ 完整的目录结构
- ✅ 所有配置文件就位
- ✅ Pre-commit hooks 正常工作
- ✅ 文档模板可用
- ✅ 工具脚本可运行
- ✅ 工作流程文档完整
- ✅ 第一个学习主题创建
- ✅ 所有 Git 提交遵循规范
- ✅ 代码通过自动检查
- ✅ 文档链接全部有效

## 下一步

完成基础结构搭建后，可以：

1. **开始学习**：使用 Claude Code 完成第一个主题的实践项目
2. **优化流程**：根据实际使用体验调整工作流
3. **添加内容**：创建更多学习主题
4. **分享经验**：整理最佳实践并分享

---

**计划版本**：1.1
**创建日期**：2026-03-19
**最后更新**：2026-03-19
**设计文档**：[development-workflow-design.md](../../development-workflow-design.md)

---

## 变更记录

- **v1.1** (2026-03-19)：根据审查反馈修复问题
  - 添加依赖安装步骤
  - 修复 Python 版本要求为 3.9+
  - 修复 pre-commit mypy 配置
  - 添加 pre-commit 安装步骤
  - 改进命令兼容性
  - 修复文件路径引用

- **v1.0** (2026-03-19)：初始版本
