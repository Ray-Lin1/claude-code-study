"""匈牙利算法测试"""

import numpy as np
import pytest
from hungarian_algorithm import HungarianAlgorithm


class TestHungarianAlgorithm:
    """测试匈牙利算法"""

    def test_init(self):
        """测试初始化"""
        cost = np.array([[1, 2], [3, 4]])
        solver = HungarianAlgorithm(cost)
        assert solver is not None

    def test_init_with_valid_matrix(self):
        """测试有效矩阵初始化"""
        cost = np.array([[1, 2], [3, 4]])
        solver = HungarianAlgorithm(cost)
        assert solver.original_shape == (2, 2)
        assert solver.n == 2

    def test_init_with_empty_matrix(self):
        """测试空矩阵应报错"""
        cost = np.array([])
        with pytest.raises(ValueError, match="不能为空"):
            HungarianAlgorithm(cost)

    def test_init_with_negative_values(self):
        """测试负值应报错"""
        cost = np.array([[1, -1], [2, 3]])
        with pytest.raises(ValueError, match="非负"):
            HungarianAlgorithm(cost)

    def test_init_with_nan(self):
        """测试 NaN 应报错"""
        cost = np.array([[1, np.nan], [2, 3]])
        with pytest.raises(ValueError, match="无效值"):
            HungarianAlgorithm(cost)

    def test_init_non_square_matrix(self):
        """测试非方阵应自动填充"""
        cost = np.array([[1, 2, 3], [4, 5, 6]])  # 2×3
        solver = HungarianAlgorithm(cost)
        assert solver.original_shape == (2, 3)
        assert solver.n == 3  # max(2, 3)

    def test_solve_2x2_matrix(self):
        """测试 2×2 矩阵求解"""
        cost = np.array([[3, 1], [4, 5]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 最优解：行0→列1(1), 行1→列0(4)
        assert len(assignment) == 2
        assert assignment[0] == 1
        assert assignment[1] == 0
        assert total_cost == 5

    def test_solve_simple_case(self):
        """测试简单情况"""
        cost = np.array([[1, 2], [2, 1]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 最优解：行0→列0(1), 行1→列1(1)
        assert assignment[0] == 0
        assert assignment[1] == 1
        assert total_cost == 2


class TestNonSquareMatrices:
    """测试非方阵情况 (Task 4)"""

    def test_non_square_more_rows(self):
        """测试行数大于列数的矩阵 (3×2)"""
        cost = np.array([[1, 2], [3, 4], [5, 6]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 3行2列,最优匹配: 行0→列0(1), 行1→列1(4)
        # 返回长度为min(rows, cols) = 2
        assert len(assignment) == 2
        assert assignment[0] == 0
        assert assignment[1] == 1
        assert total_cost == 5.0

    def test_non_square_more_cols(self):
        """测试列数大于行数的矩阵 (2×3)"""
        cost = np.array([[1, 2, 3], [4, 5, 6]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 2行3列,最优: 行0→列0(1), 行1→列1(5)
        assert len(assignment) == 2
        assert assignment[0] == 0
        assert assignment[1] == 1
        assert total_cost == 6

    def test_single_row(self):
        """测试单行矩阵 (1×4)"""
        cost = np.array([[3, 1, 4, 2]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 单行选择最小值列1
        assert len(assignment) == 1
        assert assignment[0] == 1
        assert total_cost == 1

    def test_single_column(self):
        """测试单列矩阵 (4×1)"""
        cost = np.array([[3], [1], [4], [2]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 单列,只能匹配一个最小值(行1)
        # 返回长度为1
        assert len(assignment) == 1
        # 匹配到最小值1所在的行
        assert total_cost == 1.0


class TestEdgeCases:
    """测试边界情况 (Task 5)"""

    def test_single_element(self):
        """测试1×1矩阵"""
        cost = np.array([[5]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 1
        assert assignment[0] == 0
        assert total_cost == 5

    def test_all_zeros(self):
        """测试全零矩阵"""
        cost = np.array([[0, 0], [0, 0]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 全零,任何匹配都行
        assert len(assignment) == 2
        assert total_cost == 0

    def test_all_same_values(self):
        """测试所有值相同的矩阵"""
        cost = np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 所有值相同,任何匹配都是15
        assert len(assignment) == 3
        assert total_cost == 15

    def test_with_zeros(self):
        """测试包含零的矩阵"""
        cost = np.array([[0, 2, 3], [4, 0, 6], [7, 8, 0]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 对角线都是0
        assert len(assignment) == 3
        assert total_cost == 0

    def test_large_matrix(self):
        """测试大矩阵性能 (10×10)"""
        # 创建10×10随机矩阵
        np.random.seed(42)
        cost = np.random.randint(1, 100, size=(10, 10))

        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 10
        # 验证每个列只匹配一次
        assert len(set(assignment)) == 10
        # 验证总成本合理性
        assert 10 <= total_cost <= 1000

    def test_symmetric_matrix(self):
        """测试对称矩阵"""
        cost = np.array([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 3
        # 实际最优解: (0,1)+(1,0)+(2,2) = 2+2+6=10
        assert total_cost == 10.0
        assert list(assignment) == [1, 0, 2]


class TestAlgorithmVerification:
    """测试算法正确性验证 (Task 6)"""

    def test_matching_uniqueness(self):
        """测试每个列最多匹配一次"""
        cost = np.array([[3, 1, 2], [4, 5, 6], [7, 8, 9]])
        solver = HungarianAlgorithm(cost)
        assignment, _ = solver.solve()

        # 验证每个列只出现一次
        assert len(assignment) == len(set(assignment))

    def test_cost_calculation(self):
        """测试成本计算正确性"""
        cost = np.array([[3, 1, 2], [4, 5, 6], [7, 8, 9]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 手动计算总成本
        expected_cost = sum(cost[i, assignment[i]] for i in range(len(assignment)))
        assert total_cost == expected_cost

    def test_brute_force_verification_small(self):
        """测试3×3矩阵的暴力验证"""
        cost = np.array([[3, 1, 2], [4, 5, 6], [7, 8, 9]])

        # 暴力枚举所有排列
        from itertools import permutations

        min_cost = float("inf")
        best_perm = None
        for perm in permutations([0, 1, 2]):
            current_cost = sum(cost[i, perm[i]] for i in range(3))
            if current_cost < min_cost:
                min_cost = current_cost
                best_perm = perm

        # 使用算法求解
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 验证结果与暴力枚举一致
        assert total_cost == min_cost
        assert tuple(assignment) == best_perm

    def test_brute_force_verification_2x2(self):
        """测试2×2矩阵的暴力验证"""
        cost = np.array([[3, 1], [4, 5]])

        # 暴力枚举
        cost1 = cost[0, 0] + cost[1, 1]  # 3 + 5 = 8
        cost2 = cost[0, 1] + cost[1, 0]  # 1 + 4 = 5

        expected_min = min(cost1, cost2)

        # 使用算法求解
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert total_cost == expected_min


class TestErrorHandling:
    """测试错误处理 (Task 7)"""

    def test_error_empty_matrix(self):
        """测试空矩阵错误"""
        cost = np.array([])
        with pytest.raises(ValueError, match="不能为空"):
            HungarianAlgorithm(cost)

    def test_error_negative_values(self):
        """测试负值错误"""
        cost = np.array([[1, 2], [-3, 4]])
        with pytest.raises(ValueError, match="非负"):
            HungarianAlgorithm(cost)

    def test_error_nan(self):
        """测试NaN错误"""
        cost = np.array([[1, np.nan], [2, 3]])
        with pytest.raises(ValueError, match="无效值"):
            HungarianAlgorithm(cost)

    def test_error_2d_array_required(self):
        """测试1D数组应该转换为单行矩阵"""
        # 1D数组应该被转换为1×n矩阵
        cost = np.array([3, 1, 4, 2])
        solver = HungarianAlgorithm(cost)
        assert solver.original_shape == (1, 4)

        assignment, total_cost = solver.solve()
        assert len(assignment) == 1
        assert assignment[0] == 1  # 选择最小值1
        assert total_cost == 1

    def test_inf_values_allowed(self):
        """测试Inf值应该被允许"""
        # 包含Inf的矩阵(不是NaN)
        cost = np.array([[1, 2], [np.inf, 3]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 应该避开Inf,选择(0,0)+(1,1)=1+3=4
        assert len(assignment) == 2
        assert assignment[0] == 0
        assert assignment[1] == 1
        assert total_cost == 4
