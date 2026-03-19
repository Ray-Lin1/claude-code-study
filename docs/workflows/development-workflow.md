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
