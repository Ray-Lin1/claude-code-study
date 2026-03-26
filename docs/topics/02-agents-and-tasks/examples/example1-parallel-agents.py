"""
示例 1: 并行调用多个 Agent

这个示例展示如何同时调用多个 Agent 处理独立任务
"""

# 场景：你想了解一个项目的不同方面
# 你可以并行调用 3 个 Explore Agent 来搜索不同的模式

# 示例代码（概念性）
def parallel_agent_example():
    """
    在 Claude Code 中，你可以这样并行调用多个 Agent：

    "请帮我同时搜索以下内容：
    1. 所有测试文件（使用 Explore Agent）
    2. 所有配置文件（使用 Explore Agent）
    3. 所有文档文件（使用 Explore Agent）
    "

    Claude Code 会在一条消息中调用 3 个 Task 工具，
    每个 Agent 独立工作，最后汇总结果。
    """

    # 等价的单线程方式（较慢）：
    tasks = [
        "搜索所有测试文件",
        "搜索所有配置文件",
        "搜索所有文档文件"
    ]

    # 串行执行（慢）
    for task in tasks:
        execute_task(task)

    # 并行执行（快）- Claude Code 自动处理
    execute_tasks_in_parallel(tasks)


# 实际使用示例
# 你对 Claude Code 说：
# "帮我找出项目中所有的测试文件、配置文件和文档文件，使用并行 Agent"
#
# Claude Code 会调用：
# Task(subagent_type="Explore", description="查找测试文件", ...)
# Task(subagent_type="Explore", description="查找配置文件", ...)
# Task(subagent_type="Explore", description="查找文档文件", ...)
