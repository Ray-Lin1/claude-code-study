"""匈牙利算法实现

提供二分图最小权匹配的标准匈牙利算法实现。
"""

import numpy as np


class HungarianAlgorithm:
    """匈牙利算法实现类(最小权匹配)

    使用标准匈牙利算法求解二分图最小权匹配问题。

    Attributes:
        cost_matrix: 处理后的方阵成本矩阵
        n: 矩阵维度
        original_shape: 原始矩阵形状 (rows, cols)

    Example:
        >>> import numpy as np
        >>> cost = np.array([[3, 1, 2], [4, 5, 6]])
        >>> solver = HungarianAlgorithm(cost)
        >>> assignment, total_cost = solver.solve()
        >>> print(assignment)  # [1, 0]
        >>> print(total_cost)  # 5
    """

    def __init__(self, cost_matrix: np.ndarray) -> None:
        """初始化匈牙利算法求解器

        Args:
            cost_matrix: 成本矩阵(非负数)
                        如果不是方阵,自动填充为方阵
                        如果是1D数组,转换为单行矩阵

        Raises:
            ValueError: 如果矩阵为空或包含负值
        """
        # 处理1D数组
        if cost_matrix.ndim == 1:
            cost_matrix = cost_matrix.reshape(1, -1)

        # 输入验证
        if cost_matrix.size == 0:
            raise ValueError("成本矩阵不能为空")

        if np.any(cost_matrix < 0):
            raise ValueError("成本矩阵必须是非负数")

        if np.any(np.isnan(cost_matrix)):
            raise ValueError("成本矩阵包含无效值 (NaN)")

        # 存储原始形状
        self.original_shape = cost_matrix.shape

        # 填充为方阵
        self.cost_matrix = cost_matrix.copy()
        self._pad_to_square()

        # 获取方阵维度
        self.n = self.cost_matrix.shape[0]

    def solve(self) -> tuple[np.ndarray, float]:
        """求解最小权匹配

        Returns:
            assignment: 匹配方案数组，assignment[i] 表示第 i 行匹配的列索引
                       长度等于原始矩阵的行数
            total_cost: 匹配的总成本

        Raises:
            RuntimeError: 如果算法执行失败
        """
        # 执行匈牙利算法
        self._hungarian_solve()

        # 提取原始矩阵行数的匹配
        original_rows = self.original_shape[0]
        original_cols = self.original_shape[1]

        assignment = []
        total_cost = 0.0

        for i in range(1, original_rows + 1):
            # p[j] = i 表示列 j 匹配行 i
            # 我们需要找到行 i 匹配的列
            for j in range(1, self.n + 1):
                if self.p[j] == i:
                    if j <= original_cols:
                        assignment.append(j - 1)  # 转换为 0-based
                        total_cost += float(self.cost_matrix[i - 1, j - 1])
                    break
            else:
                # 未找到匹配（不应该发生）
                raise RuntimeError(f"未找到行 {i - 1} 的匹配")

        return np.array(assignment), total_cost

    def _pad_to_square(self) -> None:
        """将非方阵填充为方阵

        如果矩阵不是方阵,用足够大的值填充较小的维度。
        填充值设置为 max(matrix) + 1,确保不会影响最优解。
        """
        rows, cols = self.cost_matrix.shape

        if rows == cols:
            return  # 已经是方阵

        max_dim = max(rows, cols)

        # 计算填充值
        if self.cost_matrix.size > 0:
            fill_value = np.max(self.cost_matrix) + 1
        else:
            fill_value = 1e9

        # 创建方阵
        square_matrix = np.full(
            (max_dim, max_dim), fill_value, dtype=self.cost_matrix.dtype
        )
        square_matrix[:rows, :cols] = self.cost_matrix

        self.cost_matrix = square_matrix

    def _hungarian_solve(self) -> None:
        """执行匈牙利算法核心逻辑

        实现标准的 O(n³) 匈牙利算法。
        使用 1-based 索引以便于实现。

        算法思路：
        - u[i] 和 v[j] 是行和列的标签
        - 对于匹配边 (i, j)，满足 u[i] + v[j] = cost[i, j]
        - 对于所有边，满足 u[i] + v[j] >= cost[i, j]
        - 通过增广路径不断改进匹配
        """
        n = self.n
        cost = self.cost_matrix

        # 初始化标签和匹配数组（1-based）
        self.u = np.zeros(n + 1, dtype=cost.dtype)
        self.v = np.zeros(n + 1, dtype=cost.dtype)
        self.p = np.zeros(n + 1, dtype=int)  # p[j] = 列 j 匹配的行
        self.way = np.zeros(n + 1, dtype=int)  # way[j] = 列 j 的前驱列

        # 对每一行寻找增广路径
        for i in range(1, n + 1):
            self.p[0] = i
            j0 = 0
            minv = np.full(n + 1, np.inf, dtype=cost.dtype)
            used = np.zeros(n + 1, dtype=bool)

            while True:
                used[j0] = True
                i0 = self.p[j0]  # 当前处理的行
                delta = np.inf
                j1 = 0

                # 寻找最小松弛量
                for j in range(1, n + 1):
                    if not used[j]:
                        # 当前边 (i0, j) 的松弛量
                        cur = cost[i0 - 1, j - 1] - self.u[i0] - self.v[j]
                        if cur < minv[j]:
                            minv[j] = cur
                            self.way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j

                # 更新标签
                for j in range(n + 1):
                    if used[j]:
                        self.u[self.p[j]] += delta
                        self.v[j] -= delta
                    else:
                        minv[j] -= delta

                j0 = j1

                # 找到增广路径（到达未匹配的列）
                if self.p[j0] == 0:
                    break

            # 更新匹配
            while True:
                j1 = self.way[j0]
                self.p[j0] = self.p[j1]
                j0 = j1
                if j0 == 0:
                    break
