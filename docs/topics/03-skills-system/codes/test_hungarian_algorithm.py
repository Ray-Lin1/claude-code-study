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
