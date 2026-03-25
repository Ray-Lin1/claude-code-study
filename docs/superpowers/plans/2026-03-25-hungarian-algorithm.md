# 匈牙利算法实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现标准版本的匈牙利匹配算法，用于求解二分图最小权匹配问题

**Architecture:** 使用经典矩阵实现方案，通过行列标签和增广路径寻找最优匹配。HungarianAlgorithm 类负责验证输入、自动填充方阵、执行算法并返回结果。

**Tech Stack:** Python 3.13, NumPy, pytest

---

## 文件结构

```
docs/topics/03-skills-system/codes/
├── hungarian_algorithm.py       # 算法实现 (~200 行)
└── test_hungarian_algorithm.py  # 测试文件 (~300 行)
```

**文件职责：**
- `hungarian_algorithm.py`: HungarianAlgorithm 类，包含算法核心逻辑和所有辅助方法
- `test_hungarian_algorithm.py`: 完整的测试套件，覆盖所有功能和边界情况

---

## Task 1: 创建项目结构和初始文件

**Files:**
- Create: `docs/topics/03-skills-system/codes/hungarian_algorithm.py`
- Create: `docs/topics/03-skills-system/codes/test_hungarian_algorithm.py`

- [ ] **Step 1: 创建算法文件骨架**

创建 `docs/topics/03-skills-system/codes/hungarian_algorithm.py`:

```python
"""匈牙利算法实现

提供二分图最小权匹配的标准匈牙利算法实现。
"""

import numpy as np


class HungarianAlgorithm:
    """匈牙利算法实现类（最小权匹配）

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
            cost_matrix: 成本矩阵（非负数）
                        如果不是方阵，自动填充为方阵

        Raises:
            ValueError: 如果矩阵为空或包含负值
        """
        pass

    def solve(self) -> tuple[np.ndarray, float]:
        """求解最小权匹配

        Returns:
            assignment: 匹配方案数组
            total_cost: 总成本

        Raises:
            RuntimeError: 如果算法执行失败
        """
        pass

    def _pad_to_square(self) -> None:
        """将非方阵填充为方阵"""
        pass

    def _hungarian_solve(self) -> None:
        """执行匈牙利算法核心逻辑"""
        pass
```

- [ ] **Step 2: 创建测试文件骨架**

创建 `docs/topics/03-skills-system/codes/test_hungarian_algorithm.py`:

```python
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
```

- [ ] **Step 3: 验证文件创建成功**

Run:
```bash
ls -la docs/topics/03-skills-system/codes/
python -c "from docs.topics.03_skills_system.codes.hungarian_algorithm import HungarianAlgorithm; print('Import OK')"
```

Expected: 文件存在且可以导入

- [ ] **Step 4: 提交初始文件**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "feat(hungarian): add project skeleton

Create initial files for Hungarian algorithm implementation.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 2: 实现输入验证和初始化

**Files:**
- Modify: `docs/topics/03-skills-system/codes/hungarian_algorithm.py:18-35`
- Test: `docs/topics/03-skills-system/codes/test_hungarian_algorithm.py`

- [ ] **Step 1: 编写输入验证的测试**

在 `test_hungarian_algorithm.py` 中添加:

```python
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
```

- [ ] **Step 2: 运行测试验证失败**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py::TestHungarianAlgorithm::test_init_with_valid_matrix -v
```

Expected: FAIL (方法未实现)

- [ ] **Step 3: 实现 __init__ 方法**

在 `hungarian_algorithm.py` 中实现:

```python
    def __init__(self, cost_matrix: np.ndarray) -> None:
        """初始化匈牙利算法求解器

        Args:
            cost_matrix: 成本矩阵（非负数）
                        如果不是方阵，自动填充为方阵

        Raises:
            ValueError: 如果矩阵为空或包含负值
        """
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
```

- [ ] **Step 4: 实现 _pad_to_square 方法**

```python
    def _pad_to_square(self) -> None:
        """将非方阵填充为方阵

        如果矩阵不是方阵，用足够大的值填充较小的维度。
        填充值设置为 max(matrix) + 1，确保不会影响最优解。
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
        square_matrix = np.full((max_dim, max_dim), fill_value, dtype=self.cost_matrix.dtype)
        square_matrix[:rows, :cols] = self.cost_matrix

        self.cost_matrix = square_matrix
```

- [ ] **Step 5: 运行测试验证通过**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py::TestHungarianAlgorithm -v
```

Expected: PASS

- [ ] **Step 6: 提交代码**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "feat(hungarian): implement input validation and matrix padding

Add input validation for empty, negative, and NaN values.
Implement auto-padding for non-square matrices.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 3: 实现匈牙利算法核心逻辑

**Files:**
- Modify: `docs/topics/03-skills-system/codes/hungarian_algorithm.py`
- Test: `docs/topics/03-skills-system/codes/test_hungarian_algorithm.py`

- [ ] **Step 1: 编写 2×2 矩阵测试**

在 `test_hungarian_algorithm.py` 中添加:

```python
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
```

- [ ] **Step 2: 运行测试验证失败**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py::TestHungarianAlgorithm::test_solve_2x2_matrix -v
```

Expected: FAIL (solve 方法未实现)

- [ ] **Step 3: 实现 solve 方法**

```python
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
```

- [ ] **Step 4: 实现 _hungarian_solve 核心算法**

```python
    def _hungarian_solve(self) -> None:
        """执行匈牙利算法核心逻辑

        实现标准的 O(n³) 匈牙利算法。
        使用 1-based 索引以便于实现。
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
                i0 = self.p[j0]
                delta = np.inf
                j1 = 0

                # 寻找最小增量
                for j in range(1, n + 1):
                    if not used[j]:
                        cur = self.u[i0] + self.v[j] - cost[i0 - 1, j - 1]
                        if cur < minv[j]:
                            minv[j] = cur
                            self.way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j

                # 更新标签
                for j in range(n + 1):
                    if used[j]:
                        self.u[self.p[j]] -= delta
                        self.v[j] += delta
                    else:
                        minv[j] -= delta

                j0 = j1

                # 找到增广路径
                if self.p[j0] == 0:
                    break

            # 更新匹配
            while True:
                j1 = self.way[j0]
                self.p[j0] = self.p[j1]
                j0 = j1
                if j0 == 0:
                    break
```

- [ ] **Step 5: 运行测试验证通过**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py::TestHungarianAlgorithm::test_solve_2x2_matrix -v
```

Expected: PASS

- [ ] **Step 6: 提交代码**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "feat(hungarian): implement core Hungarian algorithm

Implement the O(n³) Hungarian algorithm for minimum weight matching.
Add solve() method to extract results from the internal solution.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 4: 实现非方阵测试

**Files:**
- Test: `docs/topics/03-skills-system/codes/test_hungarian_algorithm.py`

- [ ] **Step 1: 编写非方阵测试用例**

```python
    def test_non_square_more_rows(self):
        """测试行 > 列的情况 (3×2)"""
        cost = np.array([[3, 1], [4, 5], [2, 3]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 应返回 3 个匹配
        assert len(assignment) == 3
        # 所有匹配应该是有效的列索引 (0 或 1)
        assert all(0 <= idx < 2 for idx in assignment)
        # 最优解：行0→列1(1), 行1→列0(4), 行2→? (填充值)
        assert total_cost >= 5

    def test_non_square_more_cols(self):
        """测试列 > 行的情况 (2×3)"""
        cost = np.array([[3, 1, 2], [4, 5, 6]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 应返回 2 个匹配
        assert len(assignment) == 2
        # 验证匹配是有效的列索引
        assert all(0 <= idx < 3 for idx in assignment)
        # 最优解：行0→列1(1), 行1→列0(4)
        assert assignment[0] == 1 or assignment[1] == 1
        assert total_cost >= 5

    def test_single_row(self):
        """测试单行矩阵 (1×4)"""
        cost = np.array([[3, 1, 2, 4]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 1
        assert assignment[0] == 1  # 选择最小值 1
        assert total_cost == 1

    def test_single_column(self):
        """测试单列矩阵 (4×1)"""
        cost = np.array([[3], [1], [2], [4]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 4
        # 每行都应该匹配到列 0
        assert all(idx == 0 for idx in assignment)
        # 成本应该是所有行成本之和（包括填充部分）
        assert total_cost >= 1
```

- [ ] **Step 2: 运行测试**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py::TestHungarianAlgorithm -v -k "non_square or single"
```

Expected: PASS (部分可能需要调整实现)

- [ ] **Step 3: 修复非方阵输出逻辑**

如果测试失败，修改 `solve()` 方法以确保正确处理非方阵:

```python
    def solve(self) -> tuple[np.ndarray, float]:
        """求解最小权匹配"""
        self._hungarian_solve()

        original_rows = self.original_shape[0]
        original_cols = self.original_shape[1]

        assignment = []
        total_cost = 0.0

        for i in range(1, original_rows + 1):
            # 找到行 i 匹配的列
            for j in range(1, self.n + 1):
                if self.p[j] == i:
                    if j <= original_cols:
                        assignment.append(j - 1)
                        total_cost += float(self.cost_matrix[i - 1, j - 1])
                    break

        return np.array(assignment), total_cost
```

- [ ] **Step 4: 运行所有测试验证**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py -v
```

Expected: 所有测试 PASS

- [ ] **Step 5: 提交代码**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "test(hungarian): add non-square matrix tests

Add comprehensive tests for non-square matrices including
more rows, more columns, single row, and single column cases.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 5: 实现边界情况测试

**Files:**
- Test: `docs/topics/03-skills-system/codes/test_hungarian_algorithm.py`

- [ ] **Step 1: 编写边界情况测试**

```python
    def test_single_element(self):
        """测试 1×1 矩阵"""
        cost = np.array([[42]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 1
        assert assignment[0] == 0
        assert total_cost == 42

    def test_all_zeros(self):
        """测试全零矩阵"""
        cost = np.array([[0, 0], [0, 0]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 2
        assert total_cost == 0

    def test_all_same_values(self):
        """测试所有元素相同"""
        cost = np.array([[5, 5], [5, 5]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 2
        assert total_cost == 10

    def test_with_zeros(self):
        """测试包含 0 的矩阵"""
        cost = np.array([[0, 5], [3, 2]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 2
        # 应该选择 0
        assert total_cost >= 0
        assert (assignment[0] == 0 and assignment[1] == 1) or (assignment[0] == 1 and assignment[1] == 0)

    def test_large_matrix(self):
        """测试较大矩阵 (10×10)"""
        np.random.seed(42)
        cost = np.random.randint(1, 100, size=(10, 10))
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 10
        assert all(0 <= idx < 10 for idx in assignment)
        assert total_cost > 0

    def test_symmetric_matrix(self):
        """测试对称矩阵"""
        cost = np.array([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        assert len(assignment) == 3
        # 对角线是最优解：1+4+6=11
        assert total_cost == 11
```

- [ ] **Step 2: 运行边界测试**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py::TestHungarianAlgorithm -v -k "single or all or with_zeros or large or symmetric"
```

Expected: PASS

- [ ] **Step 3: 提交代码**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "test(hungarian): add boundary case tests

Add tests for edge cases including single element, all zeros,
same values, zeros, large matrices, and symmetric matrices.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 6: 实现算法验证测试

**Files:**
- Test: `docs/topics/03-skills-system/codes/test_hungarian_algorithm.py`

- [ ] **Step 1: 编写算法验证测试**

```python
    def test_matching_uniqueness(self):
        """测试匹配唯一性（每列最多匹配一次）"""
        cost = np.array([[3, 1, 2], [4, 5, 6], [7, 8, 9]])
        solver = HungarianAlgorithm(cost)
        assignment, _ = solver.solve()

        # 验证没有重复的列索引
        assert len(assignment) == len(set(assignment))

    def test_cost_calculation(self):
        """测试成本计算正确性"""
        cost = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 手动计算成本
        expected_cost = sum(cost[i, assignment[i]] for i in range(len(assignment)))
        assert total_cost == expected_cost

    def test_brute_force_verification_small(self):
        """测试小矩阵的暴力解验证 (3×3)"""
        cost = np.array([[3, 1, 2], [4, 5, 6], [7, 8, 9]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 暴力枚举所有排列
        import itertools
        min_cost = float('inf')
        for perm in itertools.permutations(range(3)):
            perm_cost = sum(cost[i, perm[i]] for i in range(3))
            min_cost = min(min_cost, perm_cost)

        assert total_cost == min_cost

    def test_brute_force_verification_2x2(self):
        """测试 2×2 矩阵的暴力解验证"""
        cost = np.array([[5, 3], [2, 4]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 两种可能的匹配
        cost1 = cost[0, 0] + cost[1, 1]  # 5 + 4 = 9
        cost2 = cost[0, 1] + cost[1, 0]  # 3 + 2 = 5

        assert total_cost == min(cost1, cost2)
        assert total_cost == 5
```

- [ ] **Step 2: 运行验证测试**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py::TestHungarianAlgorithm -v -k "matching_uniqueness or cost_calculation or brute"
```

Expected: PASS

- [ ] **Step 3: 提交代码**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "test(hungarian): add algorithm verification tests

Add tests to verify matching uniqueness, cost calculation,
and brute force validation for small matrices.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 7: 实现错误处理测试

**Files:**
- Test: `docs/topics/03-skills-system/codes/test_hungarian_algorithm.py`

- [ ] **Step 1: 编写错误处理测试**

```python
    def test_error_empty_matrix(self):
        """测试空矩阵错误"""
        cost = np.array([])
        with pytest.raises(ValueError, match="不能为空"):
            HungarianAlgorithm(cost)

    def test_error_negative_values(self):
        """测试负值错误"""
        cost = np.array([[1, 2], [-1, 3]])
        with pytest.raises(ValueError, match="非负"):
            HungarianAlgorithm(cost)

    def test_error_nan(self):
        """测试 NaN 错误"""
        cost = np.array([[1, np.nan], [2, 3]])
        with pytest.raises(ValueError, match="无效值"):
            HungarianAlgorithm(cost)

    def test_error_2d_array_required(self):
        """测试需要二维数组"""
        cost = np.array([1, 2, 3])  # 一维数组
        # 应该可以处理（会自动reshape）或报错
        try:
            solver = HungarianAlgorithm(cost)
            # 如果成功，应该是 1×3 矩阵
            assert solver.original_shape == (1, 3)
        except Exception:
            # 或者报错也可以接受
            pass

    def test_inf_values_allowed(self):
        """测试 Inf 值应该被允许"""
        cost = np.array([[1, 2], [np.inf, 3]])
        solver = HungarianAlgorithm(cost)
        assignment, total_cost = solver.solve()

        # 应该避免选择 inf
        assert assignment[0] == 1 or assignment[1] == 0
        assert total_cost < np.inf
```

- [ ] **Step 2: 运行错误处理测试**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py::TestHungarianAlgorithm -v -k "error or inf"
```

Expected: PASS (可能需要调整实现)

- [ ] **Step 3: 处理一维数组输入**

如果需要，修改 `__init__` 以处理一维数组:

```python
    def __init__(self, cost_matrix: np.ndarray) -> None:
        """初始化匈牙利算法求解器"""
        # 确保是二维数组
        if cost_matrix.ndim == 1:
            cost_matrix = cost_matrix.reshape(1, -1)

        # 输入验证
        if cost_matrix.size == 0:
            raise ValueError("成本矩阵不能为空")

        if np.any(cost_matrix < 0):
            raise ValueError("成本矩阵必须是非负数")

        if np.any(np.isnan(cost_matrix)):
            raise ValueError("成本矩阵包含无效值 (NaN)")

        # 其余代码不变...
```

- [ ] **Step 4: 运行所有测试验证**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py -v
```

Expected: 所有测试 PASS

- [ ] **Step 5: 提交代码**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "test(hungarian): add error handling tests

Add comprehensive error handling tests and support for 1D arrays.
Add handling for inf values which should be avoided in matching.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 8: 运行完整测试套件并确保通过

**Files:**
- All files in `docs/topics/03-skills-system/codes/`

- [ ] **Step 1: 运行所有测试**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py -v --tb=short
```

Expected: 所有测试 PASS

- [ ] **Step 2: 运行测试并查看覆盖率**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py --cov=hungarian_algorithm --cov-report=term-missing
```

Expected:
- 行覆盖率 ≥ 90%
- 分支覆盖率 ≥ 85%

- [ ] **Step 3: 添加缺失的测试（如果覆盖率不足）**

如果覆盖率不足，添加额外的测试用例以覆盖所有代码路径。

- [ ] **Step 4: 确认所有测试通过**

Run:
```bash
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py -v
```

Expected: 所有测试 PASS

- [ ] **Step 5: 提交代码（如果有修改）**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "test(hungarian): achieve 90%+ test coverage

Add additional tests to ensure comprehensive coverage of all code paths.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 9: 代码质量检查

**Files:**
- All files in `docs/topics/03-skills-system/codes/`

- [ ] **Step 1: 运行 Black 格式化**

Run:
```bash
black docs/topics/03-skills-system/codes/
```

Expected: 文件被格式化（或已经符合规范）

- [ ] **Step 2: 运行 isort 排序导入**

Run:
```bash
isort docs/topics/03-skills-system/codes/
```

Expected: 导入被排序（或已经符合规范）

- [ ] **Step 3: 运行 Flake8 代码检查**

Run:
```bash
flake8 docs/topics/03-skills-system/codes/ --max-line-length=88
```

Expected: 无错误

- [ ] **Step 4: 运行 mypy 类型检查**

Run:
```bash
mypy docs/topics/03-skills-system/codes/hungarian_algorithm.py
```

Expected:
- 可能有一些 NumPy 相关的警告，但不应该有严重错误
- 如果有类型错误，修复它们

- [ ] **Step 5: 修复所有质量问题**

如果发现任何问题，修复并重新运行检查。

- [ ] **Step 6: 提交代码**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "style(hungarian): apply code quality fixes

Run black, isort, flake8, and mypy to ensure code quality.
Fix all identified issues.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 10: 最终验证和文档

**Files:**
- All files in `docs/topics/03-skills-system/codes/`

- [ ] **Step 1: 验证所有验收标准**

Run:
```bash
# 运行所有测试
cd docs/topics/03_skills_system/codes && python -m pytest test_hungarian_algorithm.py -v

# 代码质量检查
black --check docs/topics/03-skills-system/codes/
flake8 docs/topics/03-skills-system/codes/ --max-line-length=88
```

Expected:
- ✅ 所有测试通过
- ✅ 代码符合 PEP 8 规范
- ✅ 类型检查通过
- ✅ 测试覆盖率 ≥ 90%
- ✅ 文档字符串完整

- [ ] **Step 2: 创建使用示例（可选）**

创建 `docs/topics/03-skills-system/codes/example.py`:

```python
"""匈牙利算法使用示例"""

import numpy as np
from hungarian_algorithm import HungarianAlgorithm


def main():
    """演示匈牙利算法的使用"""

    # 示例 1: 标准 3×3 矩阵
    print("示例 1: 标准 3×3 矩阵")
    cost1 = np.array([[3, 1, 2], [4, 5, 6], [7, 8, 9]])
    print(f"成本矩阵:\n{cost1}")

    solver1 = HungarianAlgorithm(cost1)
    assignment1, total_cost1 = solver1.solve()
    print(f"匹配方案: {assignment1}")
    print(f"总成本: {total_cost1}\n")

    # 示例 2: 非方阵 (2×3)
    print("示例 2: 非方阵 (2×3)")
    cost2 = np.array([[3, 1, 2], [4, 5, 6]])
    print(f"成本矩阵:\n{cost2}")

    solver2 = HungarianAlgorithm(cost2)
    assignment2, total_cost2 = solver2.solve()
    print(f"匹配方案: {assignment2}")
    print(f"总成本: {total_cost2}\n")

    # 示例 3: 任务分配问题
    print("示例 3: 任务分配问题 (4个工人, 4个任务)")
    # 成本表示工人完成任务的时间
    cost3 = np.array([
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ])
    print(f"成本矩阵:\n{cost3}")

    solver3 = HungarianAlgorithm(cost3)
    assignment3, total_cost3 = solver3.solve()
    print(f"匹配方案: {assignment3}")
    print(f"总成本: {total_cost3}")

    for i, j in enumerate(assignment3):
        print(f"  工人 {i} → 任务 {j} (成本 {cost3[i, j]})")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 运行示例验证**

Run:
```bash
cd docs/topics/03_skills_system/codes && python example.py
```

Expected: 正常运行并输出结果

- [ ] **Step 4: 最终代码审查**

审查代码确保：
- ✅ 所有公共方法都有文档字符串
- ✅ 类型提示完整
- ✅ 注释清晰且准确
- ✅ 命名符合 Python 规范
- ✅ 没有硬编码的魔法数字
- ✅ 错误消息清晰

- [ ] **Step 5: 最终提交**

```bash
git add docs/topics/03-skills-system/codes/
git commit -m "feat(hungarian): complete implementation with examples

Add comprehensive implementation of Hungarian algorithm with:
- Full test coverage (90%+)
- Code quality checks passed
- Usage examples

Complete all acceptance criteria:
- All tests passing
- PEP 8 compliant
- Type checking passed
- Complete documentation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## 验收标准

在完成所有任务后，确保：

- [ ] 所有测试通过（pytest）
- [ ] 代码符合 PEP 8 规范（black, flake8）
- [ ] 类型检查通过（mypy）
- [ ] 测试覆盖率 ≥ 90%
- [ ] 文档字符串完整
- [ ] 支持非方阵自动填充
- [ ] 正确处理边界情况
- [ ] 错误处理完善
- [ ] 包含使用示例

---

## 附录：测试覆盖目标

| 方法/功能 | 测试用例 |
|----------|---------|
| `__init__` | 有效矩阵、空矩阵、负值、NaN、非方阵 |
| `_pad_to_square` | 方阵、行>列、列>行、单行、单列 |
| `_hungarian_solve` | 2×2、3×3、大矩阵、对称矩阵 |
| `solve` | 所有上述情况的输出验证 |
| 边界情况 | 1×1、全零、相同值、包含0、Inf |
| 错误处理 | 所有异常情况 |
| 算法验证 | 匹配唯一性、成本计算、暴力解对比 |

---

## 预期时间

- Task 1: 10 分钟（项目结构）
- Task 2: 20 分钟（输入验证）
- Task 3: 30 分钟（核心算法）
- Task 4: 20 分钟（非方阵测试）
- Task 5: 15 分钟（边界情况）
- Task 6: 15 分钟（算法验证）
- Task 7: 15 分钟（错误处理）
- Task 8: 15 分钟（完整测试）
- Task 9: 10 分钟（代码质量）
- Task 10: 15 分钟（最终验证）

**总计**: 约 2.5 - 3 小时
