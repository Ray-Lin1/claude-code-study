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
