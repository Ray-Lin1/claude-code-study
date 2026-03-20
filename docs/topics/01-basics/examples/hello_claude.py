#!/usr/bin/env python3
"""
Hello Claude - 第一个示例

这是一个简单的示例，演示如何使用 Claude Code
来理解和改进代码。
"""

import argparse  # noqa: F401
import sys  # noqa: F401
from typing import Literal  # noqa: F401

# 版本信息
VERSION = "1.0.0"


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


def get_version() -> str:
    """
    获取版本信息

    Returns:
        版本字符串
    """
    return f"hello-claude {VERSION}"


# ============================================================================
# CLI命令层
# ============================================================================


class GreetCommand:
    """CLI命令封装类"""

    def __init__(self) -> None:
        """初始化命令解析器"""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        创建并配置参数解析器

        Returns:
            配置好的ArgumentParser实例
        """
        parser = argparse.ArgumentParser(
            prog="hello_claude.py", description="Hello Claude - CLI工具示例"
        )

        # 添加参数选项
        parser.add_argument(
            "--name",
            "-n",
            type=str,
            default="Claude",
            metavar="NAME",
            help="要问候的名字 (default: Claude)",
        )

        parser.add_argument(
            "--greeting",
            "-g",
            type=str,
            default="Hello",
            metavar="GREETING",
            help="自定义问候语 (default: Hello)",
        )

        parser.add_argument(
            "--count",
            "-c",
            type=int,
            default=1,
            metavar="COUNT",
            help="重复次数 (1-10) (default: 1)",
        )

        parser.add_argument("--demo", "-d", action="store_true", help="运行演示模式")

        parser.add_argument("--version", action="version", version=get_version())

        return parser

    def parse_args(self, argv: list[str] | None = None) -> argparse.Namespace:
        """
        解析命令行参数

        Args:
            argv: 命令行参数列表，None表示使用sys.argv

        Returns:
            解析后的参数命名空间
        """
        return self.parser.parse_args(argv)

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
