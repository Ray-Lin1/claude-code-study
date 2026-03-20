# Hello Claude CLI工具设计文档

**项目:** Claude Code学习项目 - 01基础主题
**设计日期:** 2026-03-20
**版本:** 1.0.0
**状态:** 待审查

---

## 1. 概述

### 1.1 目标

为 `docs/topics/01-basics/examples/hello_claude.py` 添加CLI（命令行界面）工具，实现双重目标：
- **教学演示** - 展示如何为Python程序添加CLI接口，适合初学者学习
- **实用功能** - 提供功能完善的命令行问候工具

### 1.2 设计原则

- **单一职责** - 核心逻辑和CLI层分离
- **可测试性** - 各层可独立测试
- **向后兼容** - 保留原有演示代码
- **教学友好** - 代码结构清晰，注释完整
- **零依赖** - 使用Python标准库（argparse）

---

## 2. 整体架构

### 2.1 文件结构

```
hello_claude.py (单一文件，约90-100行)
├── 核心逻辑层
│   └── greet(name: str) -> str          # 保持不变，纯函数
│
├── CLI命令层
│   ├── class GreetCommand               # CLI命令封装类
│   │   ├── parse_args()                 # 参数解析
│   │   ├── validate_args()              # 参数验证
│   │   └── execute()                    # 执行命令
│   └── get_version()                    # 版本信息
│
└── 入口点
    ├── main()                            # CLI主入口（重构）
    └── demo_main()                       # 原有的演示代码（保留）
```

### 2.2 层次职责

**核心逻辑层**
- 职责：生成问候语
- 特点：纯函数，无副作用，易于测试

**CLI命令层**
- 职责：处理用户交互、参数解析、验证
- 特点：封装所有CLI相关逻辑

**入口点**
- 职责：连接CLI层和核心逻辑层
- 特点：提供清晰的程序入口

---

## 3. CLI参数设计

### 3.1 支持的参数

| 参数 | 短选项 | 长选项 | 类型 | 默认值 | 说明 |
|------|--------|--------|------|--------|------|
| 名字 | `-n` | `--name` | str | `"Claude"` | 要问候的名字 |
| 问候语 | `-g` | `--greeting` | str | `"Hello"` | 自定义问候语 |
| 重复次数 | `-c` | `--count` | int | `1` | 重复问候的次数 |
| 演示模式 | `-d` | `--demo` | flag | `False` | 运行原有的演示代码 |
| 版本 | | `--version` | flag | `False` | 显示版本信息 |
| 帮助 | `-h` | `--help` | flag | `False` | 显示帮助信息 |

### 3.2 使用示例

```bash
# 基础使用
python hello_claude.py
# 输出: Hello, Claude!

# 自定义名字
python hello_claude.py --name "World"
# 输出: Hello, World!

# 自定义问候语和名字
python hello_claude.py -g "Hi" -n "Ray"
# 输出: Hi, Ray!

# 重复3次
python hello_claude.py --name "Learner" --count 3
# 输出:
# Hello, Learner!
# Hello, Learner!
# Hello, Learner!

# 演示模式（原有行为）
python hello_claude.py --demo

# 查看版本
python hello_claude.py --version
# 输出: hello-claude 1.0.0
```

### 3.3 参数验证规则

- `--name`:
  - 非空字符串
  - 最大长度50字符
- `--greeting`:
  - 非空字符串
  - 最大长度20字符
- `--count`:
  - 1-10之间的整数（防止输出过多）

---

## 4. 数据流和执行逻辑

### 4.1 程序执行流程

```
用户输入命令
    ↓
parse_args() 解析参数
    ↓
验证参数有效性
    ├─ 无效 → 显示错误信息 + 退出（状态码2）
    └─ 有效 ↓
判断运行模式
    ├─ --demo → 调用 demo_main()
    └─ 正常模式 ↓
execute() 执行命令
    ↓
循环 count 次
    ├─ 调用 greet(name, greeting)
    └─ 打印结果
    ↓
正常退出（状态码0）
```

### 4.2 核心类设计

```python
class GreetCommand:
    """CLI命令封装类"""

    def __init__(self) -> None:
        """初始化命令解析器"""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """创建并配置参数解析器"""

    def parse_args(self, argv: list[str] | None = None) -> argparse.Namespace:
        """解析命令行参数"""

    def validate_args(self, args: argparse.Namespace) -> bool:
        """验证参数有效性"""

    def execute(self, args: argparse.Namespace) -> int:
        """执行命令，返回退出码"""
```

### 4.3 入口函数

```python
def main(argv: list[str] | None = None) -> int:
    """
    CLI主入口

    Args:
        argv: 命令行参数列表，None表示使用sys.argv

    Returns:
        int: 退出码（0=成功，2=参数错误）
    """
```

---

## 5. 错误处理和用户体验

### 5.1 错误处理场景

**1. 参数验证错误**
```bash
$ python hello_claude.py --count 0
错误: --count 必须在 1 到 10 之间
```

**2. 参数缺失错误**
```bash
$ python hello_claude.py --name ""
错误: --name 不能为空
```

**3. 帮助信息**
```bash
$ python hello_claude.py --help
usage: hello_claude.py [-h] [--name NAME] [--greeting GREETING]
                       [--count COUNT] [--demo] [--version]

Hello Claude - CLI工具示例

options:
  -h, --help            show this help message and exit
  --name NAME           要问候的名字 (default: Claude)
  --greeting GREETING   自定义问候语 (default: Hello)
  --count COUNT         重复次数 (1-10) (default: 1)
  --demo                运行演示模式
  --version             show program's version number and exit
```

**4. 版本信息**
```bash
$ python hello_claude.py --version
hello-claude 1.0.0
```

### 5.2 退出码规范

- `0` - 成功执行
- `2` - 参数错误（argparse默认）

### 5.3 用户体验优化

- 所有错误信息使用中文
- 错误信息清晰指出问题所在
- 提供合理的默认值
- 支持长短两种选项格式
- 帮助信息清晰完整

---

## 6. 代码组织

### 6.1 代码结构

```python
#!/usr/bin/env python3
"""
Hello Claude - CLI工具示例

这是一个演示如何为Python程序添加CLI接口的示例。
展示了使用argparse构建命令行工具的最佳实践。

Author: Ray & Claude Code
Version: 1.0.0
"""

import argparse
import sys
from typing import Literal


# 版本信息
VERSION = "1.0.0"

# ============================================================================
# 核心逻辑层
# ============================================================================

def greet(name: str, greeting: str = "Hello") -> str:
    """生成问候语"""
    return f"{greeting}, {name}!"


# ============================================================================
# CLI命令层
# ============================================================================

class GreetCommand:
    """CLI命令封装类"""

    # 实现代码...


def get_version() -> str:
    """获取版本信息"""
    return f"hello-claude {VERSION}"


# ============================================================================
# 入口点
# ============================================================================

def main(argv: list[str] | None = None) -> int:
    """CLI主入口"""
    # 实现代码...


def demo_main() -> None:
    """原有的演示代码（向后兼容）"""
    # 原有的main()实现...


if __name__ == "__main__":
    sys.exit(main())
```

### 6.2 文档规范

- 所有公共函数都有完整的docstring（Google风格）
- 代码分段使用注释标题（`====`分隔线）
- 类型提示完整（使用 `|` 联合类型语法，Python 3.10+）
- 关键逻辑添加行内注释

### 6.3 代码量估算

| 部分 | 行数 |
|------|------|
| 核心逻辑 | ~10行 |
| CLI类 | ~50行 |
| 入口函数 | ~20行 |
| 注释和文档 | ~20行 |
| **总计** | **~90-100行** |

---

## 7. 实现优先级

### Phase 1: 核心结构（必须）
- [ ] 创建 `GreetCommand` 类骨架
- [ ] 实现 `parse_args()` 方法
- [ ] 实现基础参数解析
- [ ] 重构 `main()` 入口函数

### Phase 2: 功能完善（必须）
- [ ] 实现 `validate_args()` 方法
- [ ] 实现 `execute()` 方法
- [ ] 添加 `--demo` 模式支持
- [ ] 添加 `--version` 支持

### Phase 3: 错误处理（重要）
- [ ] 实现参数验证逻辑
- [ ] 添加中文错误信息
- [ ] 完善帮助文档

### Phase 4: 测试和文档（可选）
- [ ] 添加单元测试
- [ ] 更新主题文档
- [ ] 添加使用示例

---

## 8. 技术决策

### 为什么选择 argparse？

1. **零依赖** - Python标准库，无需安装额外包
2. **教学价值** - 理解argparse有助于学习Python CLI开发
3. **通用性** - 知识可迁移到其他CLI库
4. **代码透明** - 显式结构，便于理解CLI工作原理

### 为什么选择单一文件结构？

1. **简化学习** - 初学者更容易理解
2. **代码集中** - 所有逻辑在一处，便于查看
3. **适合规模** - 对于90-100行的代码，分离文件反而增加复杂度

### 为什么保留原有代码？

1. **向后兼容** - 不破坏现有的教学示例
2. **渐进增强** - 通过 `--demo` 选项保留原有行为
3. **对比学习** - 展示如何从简单脚本演进为CLI工具

---

## 9. 后续改进方向

### 短期（可选）
- 添加单元测试（pytest）
- 支持从文件读取名字列表
- 添加彩色输出支持

### 长期（扩展学习）
- 使用 click 或 typer 重构（对比学习）
- 添加子命令支持
- 集成到更大的工具链

---

## 附录

### A. 参考资源

- [argparse 官方文档](https://docs.python.org/3/library/argparse.html)
- [CLI最佳实践](https://clig.dev/)
- [Python类型提示](https://docs.python.org/3/library/typing.html)

### B. 设计历史

- **2026-03-20**: 初始设计，选择模块化重构方案
