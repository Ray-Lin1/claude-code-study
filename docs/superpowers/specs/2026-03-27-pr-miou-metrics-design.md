# PR、mIoU 精度指标计算设计文档

**日期**: 2026-03-27
**作者**: Claude & ray
**状态**: 已批准

## 1. 概述

### 1.1 目标

实现用于语义分割任务评估的 PR（Precision-Recall）和 mIoU（mean Intersection over Union）精度指标计算算法。

### 1.2 范围

- 实现位置: `docs/topics/03-skills-system/codes_1/`
- 核心功能: 计算语义分割的精度指标
- 不涉及: 其他项目的代码读取或依赖

## 2. 需求总结

### 2.1 功能需求

1. **应用场景**: 语义分割任务评估
2. **输入格式**: NumPy 数组（标签索引，shape 为 (H, W)）
3. **类别数量**: 自动从数据中推断
4. **忽略标签**: 支持忽略指定类别（如背景类或无效标签）
5. **API 设计**: 单个函数返回所有指标
6. **PR 计算**: 每个类别分别计算后平均

### 2.2 非功能需求

- **性能**: 使用 NumPy 向量化操作，高效计算
- **可维护性**: 代码简洁，文档齐全
- **可测试性**: 完整的单元测试覆盖
- **依赖最小化**: 仅依赖 NumPy

## 3. 架构设计

### 3.1 模块结构

```
codes_1/
├── metrics.py          # 核心指标计算函数
├── tests/              # 单元测试
│   └── test_metrics.py
└── README.md           # 使用文档
```

### 3.2 核心组件

#### 3.2.1 主函数

```python
def compute_segmentation_metrics(
    pred: np.ndarray,
    gt: np.ndarray,
    ignore_index: int = -1,
    eps: float = 1e-10
) -> dict[str, Any]
```

**职责**:
- 验证输入
- 推断类别数量
- 调用混淆矩阵计算
- 计算各类指标
- 返回结果字典

**参数说明**:
- `pred`: 预测标签数组，shape (H, W)，值为类别索引
- `gt`: 真实标签数组，shape (H, W)，值为类别索引
- `ignore_index`: 要忽略的标签值（如边界区域），该像素不计入指标计算
- `eps`: 防止除零的小值，默认 1e-10。通常不需要调整，仅在数值精度问题时考虑

**返回值结构**:
```python
{
    'precision': float,           # 平均 Precision
    'recall': float,              # 平均 Recall
    'miou': float,                # 平均 IoU
    'per_class_metrics': [        # 每个类别的详细指标（按 class_id 升序排列）
        {
            'class_id': int,
            'precision': float,
            'recall': float,
            'iou': float
        },
        ...
    ]
}
```

#### 3.2.2 混淆矩阵计算

```python
def _compute_confusion_matrix(
    pred: np.ndarray,
    gt: np.ndarray,
    num_classes: int,
    ignore_index: int
) -> np.ndarray
```

**职责**:
- 过滤 ignore_index 标签
- 使用向量化操作计算混淆矩阵
- 返回 shape (num_classes, num_classes) 的矩阵

**算法**:
- `cm[i, j]` 表示真实类别 i 被预测为类别 j 的像素数
- 使用 `np.bincount` 高效统计

#### 3.2.3 输入验证

```python
def _validate_inputs(pred: np.ndarray, gt: np.ndarray) -> None
```

**验证检查**:
1. 类型检查（必须是 NumPy 数组）
2. 形状检查（pred 和 gt 形状一致）
3. 维度检查（必须是 2D 数组）
4. 数值范围检查（标签索引有效性）

### 3.3 算法细节

#### 3.3.1 混淆矩阵推导指标

对于类别 i:
- **TP (True Positive)**: `cm[i, i]`
- **FP (False Positive)**: `cm[:, i].sum() - cm[i, i]`
- **FN (False Negative)**: `cm[i, :].sum() - cm[i, i]`
- **TN (True Negative)**: 不用于分割评估

#### 3.3.2 指标计算公式

```
IoU(i) = TP / (TP + FP + FN)
Precision(i) = TP / (TP + FP)
Recall(i) = TP / (TP + FN)
```

#### 3.3.3 平均指标计算

```
mIoU = mean(IoU(i) for i in classes)
Avg Precision = mean(Precision(i) for i in classes)
Avg Recall = mean(Recall(i) for i in classes)
```

#### 3.3.4 类别数量推断

```python
num_classes = max(pred.max(), gt.max()) + 1
```

## 4. 错误处理策略

### 4.1 输入验证错误

| 错误类型 | 处理方式 | 异常类型 |
|---------|---------|---------|
| 非数组输入 | 立即返回 | TypeError |
| 形状不匹配 | 立即返回 | ValueError |
| 非二维数组 | 立即返回 | ValueError |
| 负数标签（非 ignore） | 立即返回 | ValueError |

### 4.2 边界情况处理

| 情况 | 处理方式 |
|------|----------|
| 空类别（GT中不存在） | 该类别所有指标为 0，计入平均 |
| 类别在 GT 中存在但 pred 中不存在 | Precision = 0, Recall = 0, IoU = 0 |
| 类别在 pred 中存在但 GT 中不存在 | Precision = 0, Recall = 0, IoU = 0 |
| 全部被 ignore 的图像 | 返回 0 值，给出警告 |
| 除零保护 | 使用 `eps=1e-10` 避免除零 |
| 完全匹配 | mIoU = 1.0, Precision = 1.0, Recall = 1.0 |
| 完全不匹配 | mIoU = 0.0 |

## 5. 测试策略

### 5.1 测试覆盖范围

#### 5.1.1 功能测试

```python
def test_simple_case():
    """测试简单二分类情况"""

def test_multiclass():
    """测试多类别情况（5类）"""

def test_with_ignore_index():
    """测试忽略标签功能"""

def test_large_random():
    """测试大规模随机数据"""
```

#### 5.1.2 边界测试

```python
def test_perfect_match():
    """测试完全匹配情况"""

def test_total_mismatch():
    """测试完全不匹配情况"""

def test_empty_class():
    """测试空类别处理"""
```

#### 5.1.3 异常测试

```python
def test_shape_mismatch():
    """测试形状不匹配异常"""

def test_wrong_dimensions():
    """测试错误维度异常"""

def test_wrong_type():
    """测试错误类型异常"""
```

### 5.2 测试目标

- **行覆盖率**: ≥ 95%
- **分支覆盖率**: ≥ 90%
- 所有异常路径都有测试覆盖

## 6. 实现细节

### 6.1 代码规范

- **类型提示**: 所有函数参数和返回值使用类型提示
- **文档字符串**: 所有公共函数都有完整 docstring
- **命名规范**: 遵循 PEP 8（snake_case）
- **注释**: 关键算法步骤添加行内注释

### 6.2 性能考虑

- **向量化操作**: 使用 NumPy 向量化，避免 Python 循环
- **内存效率**: 一次性计算混淆矩阵，避免重复计算
- **除零保护**: 使用 `eps` 参数而非条件判断，保持向量化

### 6.3 依赖管理

```python
# requirements.txt
numpy>=1.20.0
```

可选（用于测试）:
```python
# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=4.0.0
```

## 7. 使用示例

### 7.1 基本用法

```python
import numpy as np
from metrics import compute_segmentation_metrics

# 准备数据
pred = np.array([
    [0, 1, 2, 0],
    [1, 2, 0, 1],
    [2, 0, 1, 2]
])

gt = np.array([
    [0, 1, 1, 0],
    [1, 2, 2, 1],
    [2, 0, 0, 2]
])

# 计算指标
metrics = compute_segmentation_metrics(pred, gt)

# 打印结果
print(f"mIoU: {metrics['miou']:.4f}")
print(f"Precision: {metrics['precision']:.4f}")
print(f"Recall: {metrics['recall']:.4f}")

# 查看每个类别的详细指标
for class_metric in metrics['per_class_metrics']:
    print(f"Class {class_metric['class_id']}: "
          f"IoU={class_metric['iou']:.4f}, "
          f"Precision={class_metric['precision']:.4f}, "
          f"Recall={class_metric['recall']:.4f}")
```

### 7.2 使用忽略标签

```python
# 假设 -1 表示忽略标签（如边界区域）
pred = np.array([[0, 1, -1], [1, 0, 2]])
gt = np.array([[0, 1, -1], [1, 0, -1]])

metrics = compute_segmentation_metrics(pred, gt, ignore_index=-1)
# -1 位置的像素会被忽略，不计入指标计算
```

### 7.3 批量处理多张图像（可选扩展）

**注意**: 这是一个扩展功能的示例，不在当前实现范围内。用户可根据需要自行实现。

```python
def compute_batch_metrics(preds, gts, ignore_index=-1):
    """
    批量计算多张图像的平均指标

    参数:
        preds: List[np.ndarray], 预测标签列表
        gts: List[np.ndarray], 真实标签列表
        ignore_index: 忽略标签值

    返回:
        平均指标字典

    实现思路:
        1. 累积所有图像的混淆矩阵
        2. 基于累积的混淆矩阵计算最终指标
    """
    # 实现略 - 由用户根据需要自行实现
    pass
```

## 8. 后续扩展可能性

### 8.1 可能的增强功能

1. **批处理支持**: 支持一次性处理多张图像
2. **更多指标**: 添加 F1-score、Dice coefficient 等
3. **类别权重**: 支持加权平均
4. **可视化**: 添加混淆矩阵可视化功能
5. **PyTorch/TensorFlow 支持**: 如果需要 GPU 加速

### 8.2 设计考虑

当前设计保持简单，遵循 YAGNI（You Aren't Gonna Need It）原则。如果后续有新需求，可以在当前基础上扩展。

## 9. 验收标准

- [ ] 所有单元测试通过
- [ ] 测试覆盖率 ≥ 95%
- [ ] 代码通过 Black、Flake8、mypy 检查
- [ ] README 文档完整
- [ ] 代码符合 PEP 8 规范
- [ ] 所有函数有完整 docstring

## 10. 实现计划

下一步将创建详细的实现计划，包括：
1. 创建项目结构
2. 实现核心函数
3. 编写单元测试
4. 文档编写
5. 代码质量检查
