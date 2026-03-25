"""匈牙利算法测试"""

import numpy as np
from hungarian_algorithm import HungarianAlgorithm


class TestHungarianAlgorithm:
    """测试匈牙利算法"""

    def test_init(self):
        """测试初始化"""
        cost = np.array([[1, 2], [3, 4]])
        solver = HungarianAlgorithm(cost)
        assert solver is not None
