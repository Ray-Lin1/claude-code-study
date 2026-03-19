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
