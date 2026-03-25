"""匈牙利算法使用示例

演示如何使用 HungarianAlgorithm 类解决二分图最小权匹配问题。
"""

import numpy as np
from hungarian_algorithm import HungarianAlgorithm


def main():
    """演示匈牙利算法的使用"""

    print("=" * 60)
    print("匈牙利算法使用示例")
    print("=" * 60)
    print()

    # 示例 1: 标准 3×3 矩阵
    print("示例 1: 标准 3×3 矩阵")
    print("-" * 60)
    cost1 = np.array([[3, 1, 2], [4, 5, 6], [7, 8, 9]])
    print(f"成本矩阵:\n{cost1}")

    solver1 = HungarianAlgorithm(cost1)
    assignment1, total_cost1 = solver1.solve()
    print(f"匹配方案: {assignment1}")
    print(f"总成本: {total_cost1}")

    for i, j in enumerate(assignment1):
        print(f"  行 {i} → 列 {j} (成本 {cost1[i, j]})")
    print()

    # 示例 2: 非方阵 (2×3)
    print("示例 2: 非方阵 (2×3)")
    print("-" * 60)
    cost2 = np.array([[3, 1, 2], [4, 5, 6]])
    print(f"成本矩阵:\n{cost2}")

    solver2 = HungarianAlgorithm(cost2)
    assignment2, total_cost2 = solver2.solve()
    print(f"匹配方案: {assignment2}")
    print(f"总成本: {total_cost2}")

    for i, j in enumerate(assignment2):
        print(f"  行 {i} → 列 {j} (成本 {cost2[i, j]})")
    print()

    # 示例 3: 任务分配问题 (4个工人, 4个任务)
    print("示例 3: 任务分配问题 (4个工人, 4个任务)")
    print("-" * 60)
    # 成本表示工人完成任务的时间
    cost3 = np.array([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]])
    print(f"成本矩阵:\n{cost3}")

    solver3 = HungarianAlgorithm(cost3)
    assignment3, total_cost3 = solver3.solve()
    print(f"匹配方案: {assignment3}")
    print(f"总成本: {total_cost3}")

    for i, j in enumerate(assignment3):
        print(f"  工人 {i} → 任务 {j} (时间 {cost3[i, j]})")
    print()

    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
