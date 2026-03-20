# Hello Claude CLI工具实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标:** 为 `hello_claude.py` 添加功能完善的CLI接口，支持自定义参数，同时保持教学友好性和向后兼容性

**架构:** 使用argparse构建CLI层，通过GreetCommand类封装所有CLI逻辑，保持核心greet()函数不变。采用分层架构：核心逻辑层 → CLI命令层 → 入口点

**技术栈:** Python 3.10+, argparse (标准库)

---

## 文件结构

**修改文件:**
- `docs/topics/01-basics/examples/hello_claude.py` - 主要实现文件

**文件职责:**
- `greet(name, greeting)` - 核心逻辑（保持不变，扩展参数）
- `GreetCommand` - CLI命令封装类，处理参数解析、验证、执行
- `main()` - CLI主入口，返回退出码
- `demo_main()` - 原有演示代码，保持向后兼容
- `get_version()` - 版本信息工具函数

---

## Task 1: 基础结构和版本信息

**Files:**
- Modify: `docs/topics/01-basics/examples/hello_claude.py`

- [ ] **Step 1: 添加导入和版本常量**

在文件顶部，现有的导入后添加：

```python
import argparse
import sys
from typing import Literal

# 版本信息
VERSION = "1.0.0"
```

- [ ] **Step 2: 扩展greet()函数签名**

修改现有的greet函数，添加greeting参数（保持向后兼容）：

```python
def greet(name: str, greeting: str = "Hello") -> str:
    """
    生成问候语

    Args:
        name: 要问候的名字
        greeting: 问候语文本，默认为"Hello"

    Returns:
        问候语字符串

    Example:
        >>> greet("Claude")
        'Hello, Claude!'
        >>> greet("Ray", "Hi")
        'Hi, Ray!'
    """
    return f"{greeting}, {name}!"
```

- [ ] **Step 3: 添加get_version()工具函数**

在greet()函数后添加：

```python
def get_version() -> str:
    """
    获取版本信息

    Returns:
        版本字符串
    """
    return f"hello-claude {VERSION}"
```

- [ ] **Step 4: 验证代码运行**

运行: `python docs/topics/01-basics/examples/hello_claude.py`
预期: 程序正常执行，输出问候语

- [ ] **Step 5: 提交基础结构**

```bash
git add docs/topics/01-basics/examples/hello_claude.py
git commit -m "feat(cli): add base structure and version info

- Add argparse and typing imports
- Extend greet() to support custom greeting
- Add get_version() utility function
"
```

---

## Task 2: 创建GreetCommand类骨架

**Files:**
- Modify: `docs/topics/01-basics/examples/hello_claude.py`

- [ ] **Step 1: 添加GreetCommand类定义**

在get_version()后添加类骨架和分隔注释：

```python
# ============================================================================
# CLI命令层
# ============================================================================

class GreetCommand:
    """CLI命令封装类"""

    def __init__(self) -> None:
        """初始化命令解析器"""
        self.parser = self._create_parser()
```

- [ ] **Step 2: 添加_create_parser()方法**

在类中添加：

```python
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        创建并配置参数解析器

        Returns:
            配置好的ArgumentParser实例
        """
        parser = argparse.ArgumentParser(
            prog="hello_claude.py",
            description="Hello Claude - CLI工具示例"
        )

        # 添加参数选项
        parser.add_argument(
            "--name", "-n",
            type=str,
            default="Claude",
            metavar="NAME",
            help="要问候的名字 (default: Claude)"
        )

        parser.add_argument(
            "--greeting", "-g",
            type=str,
            default="Hello",
            metavar="GREETING",
            help="自定义问候语 (default: Hello)"
        )

        parser.add_argument(
            "--count", "-c",
            type=int,
            default=1,
            metavar="COUNT",
            help="重复次数 (1-10) (default: 1)"
        )

        parser.add_argument(
            "--demo", "-d",
            action="store_true",
            help="运行演示模式"
        )

        parser.add_argument(
            "--version",
            action="version",
            version=get_version()
        )

        return parser
```

- [ ] **Step 3: 添加parse_args()方法**

在类中添加：

```python
    def parse_args(self, argv: list[str] | None = None) -> argparse.Namespace:
        """
        解析命令行参数

        Args:
            argv: 命令行参数列表，None表示使用sys.argv

        Returns:
            解析后的参数命名空间
        """
        return self.parser.parse_args(argv)
```

- [ ] **Step 4: 验证argparse配置**

测试帮助信息：
运行: `python docs/topics/01-basics/examples/hello_claude.py --help`
预期: 显示完整的帮助信息，包含所有参数

- [ ] **Step 5: 提交GreetCommand类骨架**

```bash
git add docs/topics/01-basics/examples/hello_claude.py
git commit -m "feat(cli): add GreetCommand class skeleton

- Add GreetCommand class with argparse setup
- Implement _create_parser() with all CLI arguments
- Implement parse_args() method
- Support --name, --greeting, --count, --demo, --version
"
```

---

## Task 3: 实现参数验证

**Files:**
- Modify: `docs/topics/01-basics/examples/hello_claude.py`

- [ ] **Step 1: 添加validate_args()方法**

在GreetCommand类中添加：

```python
    def validate_args(self, args: argparse.Namespace) -> bool:
        """
        验证参数有效性

        Args:
            args: 解析后的参数

        Returns:
            True表示参数有效，False表示无效
        """
        # 验证name
        if not args.name or len(args.name.strip()) == 0:
            print("错误: --name 不能为空", file=sys.stderr)
            return False

        if len(args.name) > 50:
            print("错误: --name 最大长度为50字符", file=sys.stderr)
            return False

        # 验证greeting
        if not args.greeting or len(args.greeting.strip()) == 0:
            print("错误: --greeting 不能为空", file=sys.stderr)
            return False

        if len(args.greeting) > 20:
            print("错误: --greeting 最大长度为20字符", file=sys.stderr)
            return False

        # 验证count
        if args.count < 1 or args.count > 10:
            print("错误: --count 必须在 1 到 10 之间", file=sys.stderr)
            return False

        return True
```

- [ ] **Step 2: 手动测试验证逻辑**

测试空名字：
运行: `python docs/topics/01-basics/examples/hello_claude.py --name ""`
预期: 显示"错误: --name 不能为空"

测试超出范围的count：
运行: `python docs/topics/01-basics/examples/hello_claude.py --count 0`
预期: 显示"错误: --count 必须在 1 到 10 之间"

- [ ] **Step 3: 提交参数验证**

```bash
git add docs/topics/01-basics/examples/hello_claude.py
git commit -m "feat(cli): add parameter validation

- Implement validate_args() method
- Validate name: non-empty, max 50 chars
- Validate greeting: non-empty, max 20 chars
- Validate count: range 1-10
- Display Chinese error messages
"
```

---

## Task 4: 实现execute()方法

**Files:**
- Modify: `docs/topics/01-basics/examples/hello_claude.py`

- [ ] **Step 1: 添加execute()方法**

在GreetCommand类中添加：

```python
    def execute(self, args: argparse.Namespace) -> int:
        """
        执行命令

        Args:
            args: 验证后的参数

        Returns:
            退出码（0表示成功）
        """
        # 检查是否为演示模式
        if args.demo:
            demo_main()
            return 0

        # 正常模式：根据count重复问候
        for _ in range(args.count):
            message = greet(args.name, args.greeting)
            print(message)

        return 0
```

- [ ] **Step 2: 测试基础执行功能**

测试默认参数：
运行: `python docs/topics/01-basics/examples/hello_claude.py`
预期: 输出"Hello, Claude!"

测试自定义参数：
运行: `python docs/topics/01-basics/examples/hello_claude.py --name "World" --greeting "Hi" --count 2`
预期: 输出两行"Hi, World!"

- [ ] **Step 3: 提交execute方法**

```bash
git add docs/topics/01-basics/examples/hello_claude.py
git commit -m "feat(cli): add execute method

- Implement execute() method
- Support --demo mode to run original demo
- Support normal mode with customizable parameters
- Implement count-based repetition
"
```

---

## Task 5: 重构main()函数并添加demo_main()

**Files:**
- Modify: `docs/topics/01-basics/examples/hello_claude.py`

- [ ] **Step 1: 添加入口点分隔注释**

在文件末尾，if __name__之前添加：

```python
# ============================================================================
# 入口点
# ============================================================================

```

- [ ] **Step 2: 将现有main()重命名为demo_main()**

将现有的main()函数重命名：

```python
def demo_main() -> None:
    """
    原有的演示代码（向后兼容）

    运行原有的问候示例，展示基础功能。
    """
    # 问候 Claude
    message = greet("Claude")
    print(message)

    # 可以尝试其他名字
    other_names = ["World", "Developer", "Learner"]
    for name in other_names:
        print(greet(name))
```

- [ ] **Step 3: 创建新的main()函数**

在demo_main()之后添加：

```python
def main(argv: list[str] | None = None) -> int:
    """
    CLI主入口

    Args:
        argv: 命令行参数列表，None表示使用sys.argv

    Returns:
        int: 退出码（0=成功，2=参数错误）
    """
    command = GreetCommand()

    # 解析参数
    try:
        args = command.parse_args(argv)
    except SystemExit as e:
        # argparse处理--help和错误时会调用sys.exit()
        return e.code if e.code is not None else 2

    # 验证参数
    if not command.validate_args(args):
        return 2

    # 执行命令
    return command.execute(args)
```

- [ ] **Step 4: 更新if __name__块**

修改文件末尾的入口点：

```python
if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: 测试完整功能流程**

测试CLI模式：
运行: `python docs/topics/01-basics/examples/hello_claude.py --name "Test"`
预期: 输出"Hello, Test!"

测试演示模式：
运行: `python docs/topics/01-basics/examples/hello_claude.py --demo`
预期: 输出原有的演示问候语

测试版本信息：
运行: `python docs/topics/01-basics/examples/hello_claude.py --version`
预期: 输出"hello-claude 1.0.0"

- [ ] **Step 6: 提交入口点重构**

```bash
git add docs/topics/01-basics/examples/hello_claude.py
git commit -m "feat(cli): refactor main entry point

- Rename existing main() to demo_main() for backward compatibility
- Create new main() as CLI entry point with proper exit codes
- Update if __name__ block to call new main()
- Maintain all original functionality via --demo flag
"
```

---

## Task 6: 代码清理和文档完善

**Files:**
- Modify: `docs/topics/01-basics/examples/hello_claude.py`

- [ ] **Step 1: 添加模块级文档字符串**

更新文件顶部的文档字符串：

```python
#!/usr/bin/env python3
"""
Hello Claude - CLI工具示例

这是一个演示如何为Python程序添加CLI接口的示例。
展示了使用argparse构建命令行工具的最佳实践。

使用示例:
    基础使用:
        python hello_claude.py

    自定义参数:
        python hello_claude.py --name "World" --greeting "Hi"

    重复多次:
        python hello_claude.py --count 3

    演示模式:
        python hello_claude.py --demo

    查看帮助:
        python hello_claude.py --help

Author: Ray & Claude Code
Version: 1.0.0
Requirements: Python 3.10+
"""
```

- [ ] **Step 2: 添加内联注释**

在关键位置添加简短注释（如果还没有的话）：
- 类和方法的分隔注释已有（====）
- 复杂逻辑处添加行内注释

- [ ] **Step 3: 验证代码质量**

检查语法：
运行: `python -m py_compile docs/topics/01-basics/examples/hello_claude.py`
预期: 无语法错误

运行所有测试场景：
```bash
# 测试所有功能
python docs/topics/01-basics/examples/hello_claude.py --help
python docs/topics/01-basics/examples/hello_claude.py --version
python docs/topics/01-basics/examples/hello_claude.py
python docs/topics/01-basics/examples/hello_claude.py --name "Test" --greeting "Hi" --count 3
python docs/topics/01-basics/examples/hello_claude.py --demo
```

预期: 所有命令正常工作

- [ ] **Step 4: 检查代码行数**

运行: `wc -l docs/topics/01-basics/examples/hello_claude.py`
预期: 约90-100行

- [ ] **Step 5: 提交文档完善**

```bash
git add docs/topics/01-basics/examples/hello_claude.py
git commit -m "docs(cli): improve code documentation

- Update module docstring with usage examples
- Add inline comments for clarity
- Document Python 3.10+ requirement
- Verify code quality and line count (~90-100 lines)
"
```

---

## Task 7: 最终测试和验证

**Files:**
- No file modifications (testing only)

- [ ] **Step 1: 执行完整的CLI测试套件**

```bash
# 1. 帮助信息
python docs/topics/01-basics/examples/hello_claude.py --help

# 2. 版本信息
python docs/topics/01-basics/examples/hello_claude.py --version

# 3. 默认参数
python docs/topics/01-basics/examples/hello_claude.py

# 4. 自定义名字
python docs/topics/01-basics/examples/hello_claude.py --name "World"

# 5. 自定义问候语
python docs/topics/01-basics/examples/hello_claude.py -g "Hi" -n "Ray"

# 6. 重复次数
python docs/topics/01-basics/examples/hello_claude.py --count 3

# 7. 组合参数
python docs/topics/01-basics/examples/hello_claude.py --name "Learner" --greeting "Welcome" --count 2

# 8. 演示模式
python docs/topics/01-basics/examples/hello_claude.py --demo

# 9. 错误处理 - 空名字
python docs/topics/01-basics/examples/hello_claude.py --name ""

# 10. 错误处理 - 超出范围count
python docs/topics/01-basics/examples/hello_claude.py --count 0
python docs/topics/01-basics/examples/hello_claude.py --count 11
```

预期: 所有测试按预期工作，错误消息正确显示

- [ ] **Step 2: 验证向后兼容性**

确认原有的编程接口仍然可用：

```python
# 在Python REPL中测试
import sys
sys.path.insert(0, 'docs/topics/01-basics/examples')
from hello_claude import greet, get_version

# 测试核心函数
print(greet("Test"))  # 应输出: Hello, Test!
print(greet("World", "Hi"))  # 应输出: Hi, World!
print(get_version())  # 应输出: hello-claude 1.0.0
```

预期: 所有函数调用正常工作

- [ ] **Step 3: 验证代码规范**

运行代码风格检查（如果配置了）：
```bash
# 如果项目配置了black, flake8等工具
black --check docs/topics/01-basics/examples/hello_claude.py
flake8 docs/topics/01-basics/examples/hello_claude.py
```

预期: 通过所有检查（或符合项目配置的标准）

- [ ] **Step 4: 查看最终代码**

运行: `head -n 30 docs/topics/01-basics/examples/hello_claude.py`
预期: 查看代码结构，确认组织清晰

运行: `tail -n 20 docs/topics/01-basics/examples/hello_claude.py`
预期: 查看入口点，确认正确

- [ ] **Step 5: 最终提交**

```bash
git add docs/topics/01-basics/examples/hello_claude.py
git commit -m "test(cli): complete final testing and validation

- Test all CLI functionality thoroughly
- Verify backward compatibility with programmatic API
- Validate code style and structure
- All tests passing, ready for production use
"
```

---

## 验收标准

实施完成后，以下标准必须全部满足：

### 功能完整性
- [x] 支持 `--name` 参数自定义名字
- [x] 支持 `--greeting` 参数自定义问候语
- [x] 支持 `--count` 参数控制重复次数
- [x] 支持 `--demo` 模式运行原有演示
- [x] 支持 `--version` 显示版本信息
- [x] 支持 `--help` 显示帮助信息

### 代码质量
- [x] 代码总行数约90-100行
- [x] 所有公共函数有完整docstring
- [x] 类型提示完整（Python 3.10+语法）
- [x] 代码分段清晰，使用分隔注释
- [x] 遵循PEP 8代码规范

### 错误处理
- [x] 参数验证完整（name, greeting, count）
- [x] 错误信息使用中文
- [x] 正确的退出码（0=成功，2=错误）

### 向后兼容
- [x] 原有 `greet()` 函数保持可用
- [x] `--demo` 模式保留原有行为
- [x] 不破坏现有教学示例

### 教学价值
- [x] 代码结构清晰，易于理解
- [x] 展示CLI工具最佳实践
- [x] 适合初学者学习
- [x] 使用标准库，零依赖

## 参考资料

- 设计文档: `docs/superpowers/specs/2026-03-20-hello-claude-cli-design.md`
- argparse官方文档: https://docs.python.org/3/library/argparse.html
- CLI最佳实践: https://clig.dev/
