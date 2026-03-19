# Claude Code 学习项目开发工作流设计文档

**设计日期**：2026-03-19
**设计目标**：创建一个使用 Claude Code 进行学习的参考模板和最佳实践工作流程
**目标用户**：Claude Code 初学者，Git 基础使用者

---

## 1. 概述

本设计文档描述了一个结构化的学习驱动型开发工作流程，旨在：
- 为 Claude Code 的学习提供清晰的框架
- 建立可复用的最佳实践模板
- 规范化文档、代码和项目管理
- 适合初学者逐步掌握工具和流程

---

## 2. 项目结构设计

### 2.1 目录结构

```
claude-code-study/
├── README.md                 # 项目总览和快速开始
├── CLAUDE.md                 # Claude Code 项目配置
├── .gitignore               # Git 忽略规则
├── pyproject.toml           # Python 项目配置
├── requirements.txt         # Python 依赖
├── pre-commit-config.yaml   # Pre-commit 钩子配置
│
├── docs/                    # 主要文档目录
│   ├── README.md           # 文档导航
│   ├── getting-started/    # 入门指南
│   │   ├── installation.md
│   │   ├── basic-usage.md
│   │   └── first-project.md
│   ├── topics/             # 学习主题（核心）
│   │   ├── 01-basics/          # 基础主题
│   │   │   ├── README.md       # 主题概述
│   │   │   ├── notes.md        # 学习笔记
│   │   │   ├── examples/       # 代码示例
│   │   │   ├── practice/       # 实践项目
│   │   │   │   ├── project1/   # 具体项目
│   │   │   │   │   ├── README.md
│   │   │   │   │   └── main.py
│   │   │   │   └── project2/
│   │   │   └── resources.md    # 参考资料
│   │   ├── 02-agents/
│   │   ├── 03-mcp-servers/
│   │   └── 04-advanced/
│   ├── workflows/          # 工作流程文档
│   │   ├── development-workflow.md
│   │   ├── git-workflow.md
│   │   └── claude-code-best-practices.md
│   └── assets/             # 图片、图表等资源
│
├── examples/               # 独立的完整示例
│   ├── hello-world/
│   └── advanced-examples/
│
├── tools/                  # 开发工具和脚本
│   ├── check-links.py     # 文档链接检查
│   └── format-code.py     # 代码格式化
│
└── tests/                  # 测试代码
    └── test_examples.py
```

### 2.2 核心设计原则

1. **主题驱动**：按 `topics/` 目录组织，每个主题是一个独立的学习单元
2. **编号系统**：使用两位数字前缀（01-, 02-, ..., 99-）保持学习顺序，支持至少 99 个主题
3. **完整单元**：每个主题包含笔记、示例、实践、参考四部分
4. **分离关注**：独立示例与主题示例分离
5. **工具支持**：提供自动化检查工具

### 2.3 实践项目难度评级标准

- ⭐☆☆☆☆（入门级）：只需跟随文档操作，无需额外思考
- ⭐⭐☆☆☆（初级）：需要理解概念，少量修改代码
- ⭐⭐⭐☆☆（中级）：需要独立实现功能，综合运用概念
- ⭐⭐⭐⭐☆（高级）：需要深入研究，解决复杂问题
- ⭐⭐⭐⭐⭐（挑战级）：需要创新思维或探索未知领域

---

## 3. 文档规范设计

### 3.1 主题 README.md 模板

```markdown
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
```

### 3.2 学习笔记 notes.md 模板

```markdown
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
```

### 3.3 代码示例规范

每个示例代码文件应包含：
- 清晰的文件名（使用英文，描述性强）
- 文档字符串说明用途
- 使用类型注解（Python）
- 必要的注释

```python
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
    pass
```

### 3.4 文档编写规范

**标题层级**：
- # 用于文档标题
- ## 用于主要章节
- ### 用于子章节
- 最多使用到 ####

**列表使用**：
- 使用 `-` 作为无序列表标记
- 使用 `1. ` `2. ` 作为有序列表标记
- 列表项之间保持一个空行分隔主要部分

**代码块**：
- 使用 ```language 指定语言
- 关键代码添加行号注释
- 复杂代码添加解释性注释

**链接规范**：
- 内部链接使用相对路径
- 外部链接添加描述性文字
- 避免使用"点击这里"等无意义链接文字

**图片和图表**：
- 存放在 `docs/assets/` 或对应主题的 `assets/` 目录
- 使用描述性文件名
- 添加 alt 文本说明

---

## 4. Git 工作流设计

### 4.1 分支策略（简化版）

**主要分支**：
- `main` - 稳定版本，始终可运行
- `develop` - 开展分支（可选，对于简单项目可以只用 main）

**功能分支**：
- `feature/topic-name` - 新增学习主题或功能
- `docs/update-name` - 文档更新
- `fix/issue-name` - 修复问题

**分支命名规范**：
```
feature/01-basics          # 新增基础主题
feature/02-agents          # 新增 Agent 主题
docs/update-readme        # 更新 README
fix/broken-link           # 修复链接问题
```

### 4.2 工作流程

**开始新主题学习**：
```bash
# 从 main 创建功能分支
git checkout main
git pull
git checkout -b feature/01-basics

# 进行学习和开发工作
# ... 编辑文件 ...

# 提交更改
git add .
git commit -m "feat: add basics topic notes and examples"
```

**完成并合并**：
```bash
# 推送到远程
git push -u origin feature/01-basics

# 如果使用 GitHub/GitLab，创建 Pull Request
# 合并到 main 后删除功能分支
git checkout main
git pull
git branch -d feature/01-basics
```

**推荐的日常工作流**：
```bash
# 使用功能分支进行所有改动
git checkout -b feature/new-topic
# ... 工作 ...
git checkout main
git merge feature/new-topic
git push
```

> **注意**：即使是小改动也建议使用功能分支，确保主分支的稳定性。唯一例外是纯文档的 typo 修正。

### 4.3 提交信息规范

使用 **Conventional Commits** 格式（简化版）：

```
<类型>: <简短描述>

[可选的详细描述]

[可选的脚注]
```

**类型（type）**：
- `feat` - 新增功能或新主题
- `docs` - 文档更新
- `fix` - 修复 bug
- `refactor` - 代码重构
- `style` - 代码格式调整（不影响功能）
- `test` - 添加或修改测试
- `chore` - 构建/工具配置更新
- `perf` - 性能优化
- `ci` - CI 配置文件和脚本（可选）

**示例**：
```bash
git commit -m "feat: add MCP server topic with examples"
git commit -m "docs: update getting-started guide"
git commit -m "fix: broken link in basics notes"
git commit -m "style: format python code with black"
```

### 4.4 .gitignore 配置

```gitignore
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
```

---

## 5. Claude Code 使用规范设计

### 5.1 有效的提示词编写原则

**1. 清晰的任务描述**

✅ **好的做法**：
```
"创建一个 Python 函数，读取 CSV 文件并计算特定列的平均值"
```

❌ **不好的做法**：
```
"帮我处理数据"
```

**2. 提供上下文**

✅ **好的做法**：
```
"我正在学习 MCP 服务器的开发。请帮我创建一个简单的 MCP 服务器示例，
该服务器提供获取天气信息的功能。使用 Python 和官方 MCP SDK。"
```

❌ **不好的做法**：
```
"写一个 MCP 服务器"
```

**3. 明确输出格式**

✅ **好的做法**：
```
"请分析这段代码的性能问题，并以以下格式输出：
1. 问题列表
2. 每个问题的影响
3. 建议的优化方案"
```

**4. 分步处理复杂任务**

✅ **好的做法**：
```
"首先，帮我设计项目结构。然后我们再一步步实现各个功能。"
```

### 5.2 技能（Skills）使用指南

**何时使用技能**：

1. **开发新功能** → 先用 `brainstorming` 技能
   ```
   /skill brainstorming
   我想添加一个新功能：...
   ```

2. **修复 Bug** → 先用 `systematic-debugging` 技能
   ```
   /skill systematic-debugging
   遇到错误：...
   ```

3. **执行实现计划** → 使用 `executing-plans` 技能
   ```
   /skill executing-plans
   按照这个计划实现：...
   ```

4. **代码审查** → 使用 `requesting-code-review` 技能
   ```
   /skill requesting-code-review
   请审查我的代码：...
   ```

**工作流程建议**：

```
开始新任务
    ↓
brainstorming (探索需求)
    ↓
是否满意方案? → 否 → 重新 brainstorming
    ↓ 是
writing-plans (制定计划)
    ↓
执行过程中出错? → 是 → systematic-debugging → 返回执行
    ↓ 否
executing-plans (执行实现)
    ↓
requesting-code-review (代码审查)
    ↓
需要修改? → 是 → 修复并重新审查
    ↓ 否
完成或继续迭代
```

### 5.3 与 Claude Code 协作的最佳实践

**1. 增量开发**
- 不要一次要求完成所有功能
- 分成小的、可验证的步骤
- 每步完成后测试和反馈

**2. 利用 CLAUDE.md**
- 在 `CLAUDE.md` 中记录项目特定的约定
- 包括：代码风格、架构决策、工作流程
- Claude Code 会自动读取并遵循

**3. 版本控制集成**
- 让 Claude Code 帮助写有意义的提交信息
- 使用 `/commit` 技能（如果可用）
- 在合并前请求代码审查

**4. 学习记录**
- 让 Claude Code 帮助生成学习总结
- 记录遇到的问题和解决方案
- 定期整理学习笔记

**5. 提问技巧**

**探索性提问**：
```
"这个功能的实现有哪几种方式？各自的优缺点是什么？"
```

**验证性提问**：
```
"我这样理解对吗：...？"
```

**代码解释**：
```
"请解释这段代码的工作原理，特别是第 X 行的逻辑"
```

### 5.4 常用工作模式

**模式 1：学习驱动**
```
你: "我想学习 MCP 服务器开发"
Claude: 使用 brainstorming 探索学习路径
你: "开始第一步"
Claude: 制定计划并执行
你: "解释这部分代码"
Claude: 详细说明
```

**模式 2：问题驱动**
```
你: "遇到错误：..."
Claude: 使用 systematic-debugging
你: "修复它"
Claude: 实施修复
```

**模式 3：审查驱动**
```
你: "完成了一个功能"
Claude: 使用 requesting-code-review
你: "根据建议修改"
Claude: 实施修改
```

---

## 6. 自动化检查设计

### 6.1 Pre-commit Hooks 配置

使用 pre-commit 框架进行代码提交前自动检查。

**.pre-commit-config.yaml**：
> **注意**：版本号基于文档编写时的稳定版本。实际使用时建议检查并使用最新稳定版本。

```yaml
repos:
  # 通用检查
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace        # 删除行尾空格
      - id: end-of-file-fixer          # 确保文件以换行符结尾
      - id: check-yaml                 # 检查 YAML 语法
      - id: check-added-large-files    # 防止提交大文件
      - id: check-merge-conflict       # 检查合并冲突标记
      - id: check-toml                 # 检查 TOML 语法

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
        additional_dependencies: [types-all]
        exclude: ^tests/
```

### 6.2 项目配置文件

**pyproject.toml**：
```toml
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
```

### 6.3 自定义检查脚本

**tools/check-links.py** - 检查文档中的链接：
```python
#!/usr/bin/env python3
# Requires: Python 3.8+
"""
检查 Markdown 文档中的内部链接是否有效
"""
import re
from pathlib import Path
import argparse

def extract_links(markdown_file: Path) -> list[str]:
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('docs_dir', type=Path, help='文档目录')
    args = parser.parse_args()

    docs_dir = args.docs_dir
    all_links_ok = True

    for md_file in docs_dir.rglob('*.md'):
        links = extract_links(md_file)
        for text, link in links:
            if not check_link(link, md_file.parent):
                print(f"❌ {md_file}: [{text}]({link})")
                all_links_ok = False

    if all_links_ok:
        print("✅ 所有链接检查通过")
    else:
        exit(1)

if __name__ == '__main__':
    main()
```

### 6.4 自动化工作流程

**安装和设置**：
```bash
# 安装开发依赖
pip install -e ".[dev]"

# 安装 pre-commit hooks
pre-commit install

# 手动运行所有检查
pre-commit run --all-files

# 运行链接检查
python tools/check-links.py docs/
```

**开发工作流**：
```bash
# 1. 创建功能分支
git checkout -b feature/new-topic

# 2. 进行开发工作
# ... 编辑文件 ...

# 3. 提交时自动运行检查
git add .
git commit -m "feat: add new topic"
# pre-commit hooks 自动运行

# 4. 如果检查失败，修复后重新提交
# pre-commit 会自动修复部分问题
git add .
git commit -m "feat: add new topic"

# 5. 推送到远程
git push
```

### 6.5 CI/CD 配置（可选，GitHub Actions）

**.github/workflows/check.yml**：
```yaml
name: Code Quality Checks

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run Black
        run: black --check .

      - name: Run Flake8
        run: flake8 .

      - name: Run MyPy
        run: mypy .

      - name: Check links
        run: python tools/check-links.py docs/
```

---

## 7. 实施计划

### 阶段一：基础结构搭建（第 1-2 周）

**任务清单**：
- [ ] 创建目录结构
- [ ] 配置 `.gitignore`
- [ ] 创建 `pyproject.toml`
- [ ] 配置 `pre-commit`
- [ ] 创建文档模板
- [ ] 编写工作流程文档

### 阶段二：第一个学习主题（第 3-4 周）

**任务清单**：
- [ ] 创建 `topics/01-basics/` 目录
- [ ] 编写主题 README
- [ ] 完成学习笔记
- [ ] 创建代码示例
- [ ] 完成实践项目
- [ ] 应用 Git 工作流

### 阶段三：完善和迭代（持续）

**任务清单**：
- [ ] 根据使用体验优化流程
- [ ] 添加更多学习主题
- [ ] 改进自动化检查
- [ ] 整理最佳实践
- [ ] 分享和交流

### 成功标准

- ✅ 项目结构清晰，易于导航
- ✅ 文档规范统一，易于维护
- ✅ Git 历史清晰，提交信息规范
- ✅ 代码格式统一，通过自动检查
- ✅ 学习进度可追踪
- ✅ 可以作为参考分享给他人

---

## 8. 附录

### 8.1 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Conventional Commits 规范](https://www.conventionalcommits.org/)
- [Pre-commit 文档](https://pre-commit.com/)
- [Python 代码风格指南 PEP 8](https://peps.python.org/pep-0008/)

### 8.2 文档维护

**何时更新**：
- 发现规范与实际使用不符时
- 引入新的工具或流程时
- 根据学习反馈优化时

**更新流程**：
1. 在文档末尾更新版本号和日期
2. 在变更记录中记录主要修改
3. 通过 Pull Request 讨论重大变更
4. 保持向后兼容性，或明确标注不兼容变更

### 8.3 常用命令速查

```bash
# Git 相关
git status
git add .
git commit -m "type: description"
git push
git pull
git checkout -b feature/name
git merge feature/name

# Python 相关
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -e ".[dev]"
black .
flake8 .
mypy .

# Pre-commit
pre-commit install
pre-commit run --all-files
```

---

## 变更记录

- **v1.1** (2026-03-19)：根据审查反馈优化内容
  - 添加难度评级标准
  - 修正 Git 工作流建议
  - 添加版本号说明
  - 扩展提交类型
  - 完善技能工作流图
  - 添加文档维护章节

- **v1.0** (2026-03-19)：初始版本

---

**文档版本**：1.1
**最后更新**：2026-03-19
**维护者**：ray
