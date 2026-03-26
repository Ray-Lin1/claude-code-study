"""
示例 2: 使用 Explore Agent 探索代码库

这个示例展示如何使用 Explore Agent 快速了解代码库结构
"""

def explore_agent_example():
    """
    场景：你刚加入一个新项目，想了解某个功能在哪里实现

    你不需要：
    ❌ 手动使用 find 或 grep 命令
    ❌ 一个个目录查看
    ❌ 多次尝试不同的搜索模式

    你应该：
    ✅ 使用 Explore Agent，告诉它你在找什么
    """

    # 示例请求：
    request = """
    "使用 Explore Agent 找到项目中所有处理用户认证的代码，
    包括中间件、路由和验证逻辑。探索级别：medium"
    """

    # Explore Agent 会：
    # 1. 使用 Glob 查找可能的文件模式
    # 2. 使用 Grep 搜索关键词（如 "auth", "authentication", "login"）
    # 3. 读取相关文件内容
    # 4. 汇总结果给你

    return request


# 常见的探索场景
exploration_scenarios = {
    "查找 API 端点": {
        "agent": "Explore",
        "prompt": "找到所有 API 路由定义和端点",
        "thoroughness": "medium"
    },
    "查找数据库模型": {
        "agent": "Explore",
        "prompt": "找到所有的数据库模型和 schema 定义",
        "thoroughness": "medium"
    },
    "查找测试文件": {
        "agent": "Explore",
        "prompt": "找到所有测试文件和测试用例",
        "thoroughness": "quick"
    },
    "理解项目结构": {
        "agent": "Explore",
        "prompt": "分析项目的整体结构和组织方式",
        "thoroughness": "very thorough"
    }
}
