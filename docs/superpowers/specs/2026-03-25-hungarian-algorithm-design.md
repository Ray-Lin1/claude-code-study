# 匈牙利算法实现设计文档

**日期**: 2026-03-25
**作者**: Claude Code
**状态**: 设计阶段

## 1. 概述

### 1.1 目标

在 `docs/topics/03-skills-system/codes` 目录下实现一个标准版本的匈牙利匹配算法，用于求解二分图最小权匹配问题。

### 1.2 需求总结

- **问题类型**: 最小权匹配（最小成本）
- **输入格式**: NumPy 二维数组
- **矩阵处理**: 自动填充非方阵为方阵
- **输出内容**: 匹配方案 + 总成本
- **代码风格**: 遵循 PEP 8，使用类型提示和中文文档字符串

## 2. 架构设计

### 2.1 文件结构

```
docs/topics/03-skills-system/codes/
├── hungarian_algorithm.py      # 算法实现
└── test_hungarian_algorithm.py # 测试文件
```

### 2.2 核心组件

#### HungarianAlgorithm 类

**职责**:
1. 接收成本矩阵并验证
2. 自动将非方阵填充为方阵
3. 执行匈牙利算法求解
4. 返回匹配方案和总成本

**关键数据结构**:
- `cost_matrix`: 填充后的方阵成本矩阵
- `n`: 方阵维度
- `original_shape`: 原始矩阵形状 (rows, cols)
- `u`: 行标签数组（大小 n+1）
- `v`: 列标签数组（大小 n+1）
- `p`: 列匹配行数组（大小 n+1）
- `way`: 路径记录数组（大小 n+1）

### 2.3 算法流程

```
输入矩阵 → 验证 → 填充为方阵 → 初始化标签
    ↓
对每一行执行：
    寻找增广路径 → 更新标签 → 记录匹配
    ↓
提取原始矩阵的匹配 → 返回结果
```

## 3. 接口设计

### 3.1 公共接口

```python
class HungarianAlgorithm:
    """匈牙利算法实现类（最小权匹配）"""

    def __init__(self, cost_matrix: np.ndarray) -> None:
        """初始化匈牙利算法求解器

        Args:
            cost_matrix: 成本矩阵（非负数）
                        如果不是方阵，自动填充为方阵

        Raises:
            ValueError: 如果矩阵为空或包含负值
        """

    def solve(self) -> tuple[np.ndarray, float]:
        """求解最小权匹配

        Returns:
            assignment: 匹配方案数组
            total_cost: 总成本

        Raises:
            RuntimeError: 如果算法执行失败
        """
```

### 3.2 私有方法

```python
def _pad_to_square(self) -> None:
    """将非方阵填充为方阵

    用 max(matrix) + 1 填充较小维度，确保不影响最优解。
    """

def _hungarian_solve(self) -> None:
    """执行匈牙利算法核心逻辑

    实现 O(n³) 的标准匈牙利算法。
    """
```

## 4. 数据流

### 4.1 输入处理

```
原始矩阵 M × N
    ↓
验证：非空、非负
    ↓
计算 max_dim = max(M, N)
    ↓
创建 max_dim × max_dim 方阵
    ↓
填充：max_val + 1
    ↓
存储 cost_matrix 和 original_shape
```

### 4.2 输出处理

```
完整匹配方案 p[1..n]
    ↓
提取前 M 行的匹配
    ↓
过滤虚拟列匹配
    ↓
返回 assignment 和 total_cost
```

## 5. 错误处理

### 5.1 输入验证

| 错误情况 | 处理方式 |
|---------|---------|
| 空矩阵 | ValueError("成本矩阵不能为空") |
| 包含负值 | ValueError("成本矩阵必须是非负数") |
| 包含 NaN | ValueError("成本矩阵包含无效值") |

### 5.2 执行时错误

| 错误情况 | 处理方式 |
|---------|---------|
| 未找到匹配 | RuntimeError("未找到有效匹配") |
| 总成本为负 | RuntimeError("计算结果异常") |
| 匹配索引无效 | RuntimeError("匹配方案包含无效索引") |

### 5.3 边界情况

- **1×1 矩阵**: 直接返回该元素
- **单行/单列**: 选择最小值索引
- **相同元素**: 任意有效匹配
- **大型矩阵**: 正常处理（可能较慢）
- **包含 Inf**: 允许，作为极大值

## 6. 测试策略

### 6.1 测试分类

1. **基础功能测试**
   - 2×2 方阵
   - 3×3 方阵
   - 标准分配问题

2. **非方阵测试**
   - 行 > 列 (3×2)
   - 列 > 行 (2×3)
   - 单行 (1×4)
   - 单列 (4×1)

3. **边界情况测试**
   - 1×1 矩阵
   - 相同元素
   - 包含 0
   - 大型矩阵

4. **算法验证测试**
   - 匹配唯一性
   - 成本计算正确性
   - 暴力解对比

5. **错误处理测试**
   - 空矩阵
   - 负值
   - NaN

### 6.2 测试示例

```python
def test_2x2_matrix():
    cost = np.array([[3, 1], [4, 5]])
    solver = HungarianAlgorithm(cost)
    assignment, total_cost = solver.solve()

    assert assignment[0] == 1  # 行0 → 列1 (cost=1)
    assert assignment[1] == 0  # 行1 → 列0 (cost=4)
    assert total_cost == 5

def test_non_square():
    cost = np.array([[3, 1, 2], [4, 5, 6]])  # 2×3
    solver = HungarianAlgorithm(cost)
    assignment, total_cost = solver.solve()

    assert len(assignment) == 2
    assert total_cost == 5  # 1 + 4
```

### 6.3 覆盖目标

- 行覆盖率 ≥ 90%
- 分支覆盖率 ≥ 85%
- 所有公共和私有方法均有测试

## 7. 算法复杂度

- **时间复杂度**: O(n³)，其中 n 为矩阵维度
- **空间复杂度**: O(n²)，用于存储矩阵和辅助数组

## 8. 实现注意事项

1. **数组索引**: 内部使用 1-based 索引（u[0], v[0] 不使用）
2. **填充值**: 使用 max(matrix) + 1 而非 np.inf，避免浮点问题
3. **数值稳定性**: 使用 epsilon = 1e-10 处理精度问题
4. **类型安全**: 使用 np.ndarray 类型提示，支持 int 和 float

## 9. 使用示例

```python
import numpy as np
from hungarian_algorithm import HungarianAlgorithm

# 标准方阵
cost = np.array([[3, 1, 2],
                 [4, 5, 6],
                 [7, 8, 9]])
solver = HungarianAlgorithm(cost)
assignment, total_cost = solver.solve()
# assignment = [1, 0, 2]
# total_cost = 1 + 4 + 9 = 14

# 非方阵
cost = np.array([[3, 1], [4, 5], [7, 8]])  # 3×2
solver = HungarianAlgorithm(cost)
assignment, total_cost = solver.solve()
# assignment = [1, 0, ?]
# 总成本 = min(1+4, 1+7, 3+4, ...)
```

## 10. 依赖项

- NumPy (用于矩阵操作)
- pytest (用于测试)

## 11. 实现计划

1. 创建 `hungarian_algorithm.py` 文件
2. 实现 `HungarianAlgorithm.__init__()` 方法
3. 实现 `_pad_to_square()` 私有方法
4. 实现 `_hungarian_solve()` 核心算法
5. 实现 `solve()` 公共方法
6. 创建 `test_hungarian_algorithm.py`
7. 编写所有测试用例
8. 运行测试并确保通过
9. 运行代码质量检查（black, flake8, mypy）
10. 提交代码

## 12. 验收标准

- [ ] 所有测试通过
- [ ] 代码符合 PEP 8 规范
- [ ] 类型检查通过（mypy）
- [ ] 测试覆盖率 ≥ 90%
- [ ] 文档字符串完整
- [ ] 支持非方阵自动填充
- [ ] 正确处理边界情况
