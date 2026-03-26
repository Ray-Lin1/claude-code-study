"""
示例 3: 使用 Plan Agent 设计实现方案

这个示例展示如何使用 Plan Agent 在编写代码前规划实现策略
"""

def plan_agent_example():
    """
    场景：你需要实现一个复杂功能，比如"添加用户认证系统"

    不要直接开始写代码！使用 Plan Agent 先规划：
    """

    planning_request = """
    使用 Plan Agent 规划"用户认证系统"的实现：

    1. 需要哪些文件和模块？
    2. 使用什么认证方法（JWT？Session？OAuth？）
    3. 数据库需要什么表？
    4. 需要哪些 API 端点？
    5. 安全性考虑有哪些？
    """

    # Plan Agent 会：
    # 1. 探索代码库，了解现有架构
    # 2. 识别关键文件和依赖关系
    # 3. 设计实现方案
    # 4. 考虑不同的技术选型和权衡
    # 5. 提供步骤化的实施计划

    return planning_request


# Plan vs Explore 的选择
def when_to_use_plan_vs_explore():
    """
    Explore Agent: 用于理解和发现
    - "这个功能在哪里？"
    - "项目结构是怎样的？"
    - "找到所有 X 相关的代码"

    Plan Agent: 用于设计和规划
    - "如何实现这个功能？"
    - "应该用什么架构？"
    - "设计实现方案"
    """

    scenarios = {
        "探索阶段": {
            "question": "用户登录功能在哪里实现？",
            "agent": "Explore",
            "reason": "这是查找和理解现有代码"
        },
        "规划阶段": {
            "question": "如何添加双因素认证功能？",
            "agent": "Plan",
            "reason": "这是设计新功能的实现方案"
        }
    }

    return scenarios
