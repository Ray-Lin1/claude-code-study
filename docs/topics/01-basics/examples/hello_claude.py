#!/usr/bin/env python3
"""
Hello Claude - 第一个示例

这是一个简单的示例，演示如何使用 Claude Code
来理解和改进代码。
"""

import argparse

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


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="Hello Claude CLI 工具")
    parser.add_argument("name", nargs="?", default="Claude", help="要问候的名字")
    parser.add_argument("-g", "--greeting", default="Hello", help="问候语")
    parser.add_argument("-v", "--version", action="store_true", help="显示版本信息")

    args = parser.parse_args()

    if args.version:
        print(get_version())
    else:
        message = greet(args.name, args.greeting)
        print(message)


if __name__ == "__main__":
    main()
