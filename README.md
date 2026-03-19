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
