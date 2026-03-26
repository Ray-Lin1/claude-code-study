# PR、mIoU 精度指标计算实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标**: 实现用于语义分割任务评估的 PR（Precision-Recall）和 mIoU（mean Intersection over Union）精度指标计算算法

**架构**: 使用纯 NumPy 实现向量化计算，通过混淆矩阵推导各项指标，采用 TDD 开发方式

**技术栈**: Python 3.x, NumPy ≥ 1.20.0, pytest

---

## 文件结构

```
docs/topics/03-skills-system/codes_1/
├── metrics.py              # 核心指标计算模块
│   ├── _validate_inputs()         # 输入验证函数（私有）
│   ├── _compute_confusion_matrix() # 混淆矩阵计算函数（私有）
│   └── compute_segmentation_metrics() # 主函数（公共）
├── tests/
│   └── test_metrics.py     # 单元测试
├── README.md               # 使用文档
└── requirements.txt        # 依赖声明
```

**职责划分**:
- `metrics.py`: 所有指标计算逻辑，包含三个核心函数
- `test_metrics.py`: 完整的测试覆盖，包括功能、边界和异常测试
- `README.md`: 用户文档和示例
- `requirements.txt`: 项目依赖

---

## Task 1: 创建项目基础结构

**Files:**
- Create: `docs/topics/03-skills-system/codes_1/metrics.py`
- Create: `docs/topics/03-skills-system/codes_1/requirements.txt`
- Create: `docs/topics/03-skills-system/codes_1/tests/__init__.py`

### 步骤 1.1: 创建空的 metrics.py 模块

创建文件并添加模块文档字符串：

```python
"""
语义分割精度指标计算模块

提供 PR (Precision-Recall) 和 mIoU (mean Intersection over Union) 指标的计算。
适用于语义分割任务的模型评估。
"""

__version__ = "0.1.0"
```

保存到: `docs/topics/03-skills-system/codes_1/metrics.py`

### 步骤 1.2: 创建 requirements.txt

```text
numpy>=1.20.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

保存到: `docs/topics/03-skills-system/codes_1/requirements.txt`

### 步骤 1.3: 创建 tests 目录结构

创建空的 `__init__.py` 文件：

```python
"""Tests for semantic segmentation metrics."""
```

保存到: `docs/topics/03-skills-system/codes_1/tests/__init__.py`

### 步骤 1.4: 验证结构

运行:
```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -c "import sys; sys.path.insert(0, '.'); import metrics; print(metrics.__version__)"
```

预期输出: `0.1.0`

### 步骤 1.5: 提交初始结构

```bash
git add docs/topics/03-skills-system/codes_1/
git commit -m "feat: initialize project structure for metrics module"
```

---

## Task 2: 实现输入验证函数（TDD）

**Files:**
- Create: `docs/topics/03-skills-system/codes_1/tests/test_metrics.py`
- Modify: `docs/topics/03-skills-system/codes_1/metrics.py`

### 步骤 2.1: 编写输入验证的失败测试

创建测试文件:

```python
"""Unit tests for semantic segmentation metrics."""

import numpy as np
import pytest
from metrics import _validate_inputs


def test_validate_inputs_with_numpy_arrays():
    """测试正确的 NumPy 数组输入"""
    pred = np.array([[0, 1], [1, 0]])
    gt = np.array([[0, 1], [1, 0]])
    # 不应该抛出异常
    _validate_inputs(pred, gt)


def test_validate_inputs_with_wrong_type():
    """测试非 NumPy 数组输入"""
    pred = [[0, 1], [1, 0]]  # Python list
    gt = np.array([[0, 1], [1, 0]])
    with pytest.raises(TypeError, match="必须是 NumPy 数组"):
        _validate_inputs(pred, gt)


def test_validate_inputs_with_shape_mismatch():
    """测试形状不匹配"""
    pred = np.array([[0, 1], [1, 0]])
    gt = np.array([[0, 1, 2], [1, 0, 1]])  # 不同形状
    with pytest.raises(ValueError, match="形状不匹配"):
        _validate_inputs(pred, gt)


def test_validate_inputs_with_wrong_dimensions():
    """测试非二维数组"""
    pred = np.array([[[0], [1]], [[1], [0]]])  # 3D 数组
    gt = np.array([[0, 1], [1, 0]])
    with pytest.raises(ValueError, match="必须是 2D 数组"):
        _validate_inputs(pred, gt)


def test_validate_inputs_with_negative_labels():
    """测试负数标签（非 ignore 情况）"""
    pred = np.array([[0, 1], [1, -2]])  # -2 不是有效的 ignore_index
    gt = np.array([[0, 1], [1, 0]])
    with pytest.raises(ValueError, match="标签索引不能为负数"):
        _validate_inputs(pred, gt)


def test_validate_inputs_with_negative_ignore_index_allowed():
    """测试允许负数作为 ignore_index 的情况"""
    # 注意：这个测试会失败，因为我们的验证函数不知道 ignore_index
    # 这个测试将在实现 ignore_index 支持时通过
    pred = np.array([[0, 1], [1, -1]])
    gt = np.array([[0, 1], [1, -1]])
    # -1 应该被允许，因为它是常见的 ignore_index
    # 但当前的 _validate_inputs 不接受 ignore_index 参数
    # 这个测试暂时跳过
    pytest.skip("需要实现 ignore_index 参数支持")
```

保存到: `docs/topics/03-skills-system/codes_1/tests/test_metrics.py`

### 步骤 2.2: 运行测试验证失败

运行:
```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py::test_validate_inputs_with_numpy_arrays -v
```

预期输出: `FAILED` 或 `ImportError` (因为函数还不存在)

### 步骤 2.3: 实现输入验证函数

在 `metrics.py` 中添加:

```python
"""语义分割精度指标计算模块..."""
# (保留之前的文档字符串)

from typing import Any

import numpy as np


def _validate_inputs(pred: np.ndarray, gt: np.ndarray) -> None:
    """
    验证输入的有效性

    参数:
        pred: 预测标签数组
        gt: 真实标签数组

    异常:
        TypeError: 如果输入不是 NumPy 数组
        ValueError: 如果形状、维度或数值范围不正确
    """
    # 1. 类型检查
    if not isinstance(pred, np.ndarray) or not isinstance(gt, np.ndarray):
        raise TypeError("pred 和 gt 必须是 NumPy 数组")

    # 2. 形状检查
    if pred.shape != gt.shape:
        raise ValueError(
            f"pred 和 gt 形状不匹配: {pred.shape} vs {gt.shape}"
        )

    # 3. 维度检查
    if pred.ndim != 2:
        raise ValueError(
            f"输入必须是 2D 数组 (H, W)，当前维度: {pred.ndim}"
        )

    # 4. 数值范围检查（允许 -1 作为常见的 ignore_index）
    if (pred < -1).any() or (gt < -1).any():
        raise ValueError("标签索引不能小于 -1")
```

### 步骤 2.4: 运行测试验证通过

运行:
```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py -v
```

预期输出: 所有 `test_validate_inputs_*` 测试 `PASSED` (除了最后一个跳过的测试)

### 步骤 2.5: 提交

```bash
git add docs/topics/03-skills-system/codes_1/metrics.py docs/topics/03-skills-system/codes_1/tests/test_metrics.py
git commit -m "feat: implement input validation function with tests"
```

---

## Task 3: 实现混淆矩阵计算函数（TDD）

**Files:**
- Modify: `docs/topics/03-skills-system/codes_1/tests/test_metrics.py`
- Modify: `docs/topics/03-skills-system/codes_1/metrics.py`

### 步骤 3.1: 编写混淆矩阵的失败测试

在 `test_metrics.py` 末尾添加:

```python
from metrics import _compute_confusion_matrix


def test_compute_confusion_matrix_simple_case():
    """测试简单的二分类混淆矩阵"""
    pred = np.array([[0, 1, 1], [1, 0, 0]])
    gt = np.array([[0, 1, 0], [1, 1, 0]])

    # 手动计算预期结果:
    # 类别 0: GT有3个，预测正确2个，错误1个
    # 类别 1: GT有3个，预测正确1个，错误2个
    # cm[0, 0] = 2 (类别0预测为0)
    # cm[0, 1] = 1 (类别0预测为1)
    # cm[1, 0] = 1 (类别1预测为0)
    # cm[1, 1] = 2 (类别1预测为1)

    cm = _compute_confusion_matrix(pred, gt, num_classes=2, ignore_index=-1)

    assert cm.shape == (2, 2)
    assert cm[0, 0] == 2  # TP for class 0
    assert cm[0, 1] == 1  # class 0 predicted as 1
    assert cm[1, 0] == 1  # class 1 predicted as 0
    assert cm[1, 1] == 2  # TP for class 1


def test_compute_confusion_matrix_with_ignore_index():
    """测试带 ignore_index 的混淆矩阵"""
    pred = np.array([[0, 1, -1], [1, 0, -1]])
    gt = np.array([[0, 1, -1], [1, 0, 2]])

    # -1 的位置应该被忽略
    cm = _compute_confusion_matrix(pred, gt, num_classes=3, ignore_index=-1)

    # 只统计非 -1 的位置
    # 有效的预测: [0, 1, 1, 0]
    # 有效的GT: [0, 1, 1, 0]
    assert cm[0, 0] == 2
    assert cm[1, 1] == 2
    assert cm[2, :].sum() == 0  # 类别2没有有效样本


def test_compute_confusion_matrix_multiclass():
    """测试多类别混淆矩阵"""
    np.random.seed(42)
    pred = np.random.randint(0, 5, (10, 10))
    gt = np.random.randint(0, 5, (10, 10))

    cm = _compute_confusion_matrix(pred, gt, num_classes=5, ignore_index=-1)

    assert cm.shape == (5, 5)
    # 所有像素都应该被统计
    assert cm.sum() == 100  # 10x10 = 100 pixels
```

### 步骤 3.2: 运行测试验证失败

运行:
```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py::test_compute_confusion_matrix_simple_case -v
```

预期输出: `ImportError` 或 `FAILED` (函数还不存在或未实现)

### 步骤 3.3: 实现混淆矩阵计算函数

在 `metrics.py` 中添加:

```python
def _compute_confusion_matrix(
    pred: np.ndarray,
    gt: np.ndarray,
    num_classes: int,
    ignore_index: int
) -> np.ndarray:
    """
    计算混淆矩阵

    参数:
        pred: 预测标签 (H, W)
        gt: 真实标签 (H, W)
        num_classes: 类别数量
        ignore_index: 要忽略的标签值

    返回:
        shape (num_classes, num_classes) 的混淆矩阵
        cm[i, j] 表示真实类别 i 被预测为类别 j 的像素数
    """
    # 创建 mask 过滤 ignore_index
    mask = (gt != ignore_index)
    pred_filtered = pred[mask]
    gt_filtered = gt[mask]

    # 使用向量化操作计算混淆矩阵
    # 将 (gt, pred) 对编码为单个索引
    indices = num_classes * gt_filtered + pred_filtered

    # 使用 bincount 统计每个索引的出现次数
    cm = np.bincount(indices, minlength=num_classes ** 2)

    # 重塑为矩阵
    return cm.reshape(num_classes, num_classes)
```

### 步骤 3.4: 运行测试验证通过

运行:
```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py::test_compute_confusion_matrix -v
```

预期输出: 所有混淆矩阵测试 `PASSED`

### 步骤 3.5: 提交

```bash
git add docs/topics/03-skills-system/codes_1/
git commit -m "feat: implement confusion matrix computation with tests"
```

---

## Task 4: 实现主函数（TDD - 第1部分：基本功能）

**Files:**
- Modify: `docs/topics/03-skills-system/codes_1/tests/test_metrics.py`
- Modify: `docs/topics/03-skills-system/codes_1/metrics.py`

### 步骤 4.1: 编写基本功能的失败测试

在 `test_metrics.py` 末尾添加:

```python
from metrics import compute_segmentation_metrics


def test_compute_metrics_simple_case():
    """测试简单二分类情况"""
    pred = np.array([[0, 1, 1], [1, 0, 0]])
    gt = np.array([[0, 1, 0], [1, 1, 0]])

    metrics = compute_segmentation_metrics(pred, gt)

    # 验证返回结构
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert 'miou' in metrics
    assert 'per_class_metrics' in metrics

    # 验证数据类型
    assert isinstance(metrics['precision'], float)
    assert isinstance(metrics['recall'], float)
    assert isinstance(metrics['miou'], float)
    assert isinstance(metrics['per_class_metrics'], list)

    # 验证值范围
    assert 0 <= metrics['precision'] <= 1
    assert 0 <= metrics['recall'] <= 1
    assert 0 <= metrics['miou'] <= 1

    # 验证 per_class_metrics 有 2 个类别
    assert len(metrics['per_class_metrics']) == 2
    for class_metric in metrics['per_class_metrics']:
        assert 'class_id' in class_metric
        assert 'precision' in class_metric
        assert 'recall' in class_metric
        assert 'iou' in class_metric


def test_compute_metrics_perfect_match():
    """测试完全匹配情况"""
    pred = np.array([[0, 1], [1, 0]])
    gt = np.array([[0, 1], [1, 0]])

    metrics = compute_segmentation_metrics(pred, gt)

    assert metrics['miou'] == 1.0
    assert metrics['precision'] == 1.0
    assert metrics['recall'] == 1.0


def test_compute_metrics_total_mismatch():
    """测试完全不匹配情况"""
    pred = np.array([[0, 0], [0, 0]])
    gt = np.array([[1, 1], [1, 1]])

    metrics = compute_segmentation_metrics(pred, gt)

    assert metrics['miou'] == 0.0
```

### 步骤 4.2: 运行测试验证失败

运行:
```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py::test_compute_metrics_simple_case -v
```

预期输出: `ImportError` (函数还不存在)

### 步骤 4.3: 实现主函数的基本功能

在 `metrics.py` 中添加:

```python
def compute_segmentation_metrics(
    pred: np.ndarray,
    gt: np.ndarray,
    ignore_index: int = -1,
    eps: float = 1e-10
) -> dict[str, Any]:
    """
    计算语义分割的 PR、mIoU 指标

    参数:
        pred: 预测标签 (H, W)，值为类别索引
        gt: 真实标签 (H, W)，值为类别索引
        ignore_index: 要忽略的标签值（默认 -1）
        eps: 防止除零的小值

    返回:
        {
            'precision': float,      # 平均 Precision
            'recall': float,         # 平均 Recall
            'miou': float,           # 平均 IoU
            'per_class_metrics': [   # 每个类别的详细指标
                {
                    'class_id': int,
                    'precision': float,
                    'recall': float,
                    'iou': float
                },
                ...
            ]
        }
    """
    # 验证输入
    _validate_inputs(pred, gt)

    # 自动推断类别数
    num_classes = max(pred.max(), gt.max()) + 1

    # 计算混淆矩阵
    cm = _compute_confusion_matrix(pred, gt, num_classes, ignore_index)

    # 计算每个类别的指标
    per_class_metrics = []
    for i in range(num_classes):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp

        precision = tp / (tp + fp + eps)
        recall = tp / (tp + fn + eps)
        iou = tp / (tp + fp + fn + eps)

        per_class_metrics.append({
            'class_id': i,
            'precision': float(precision),
            'recall': float(recall),
            'iou': float(iou)
        })

    # 计算平均指标
    avg_precision = np.mean([m['precision'] for m in per_class_metrics])
    avg_recall = np.mean([m['recall'] for m in per_class_metrics])
    avg_iou = np.mean([m['iou'] for m in per_class_metrics])

    return {
        'precision': float(avg_precision),
        'recall': float(avg_recall),
        'miou': float(avg_iou),
        'per_class_metrics': per_class_metrics
    }
```

### 步骤 4.4: 运行测试验证通过

运行:
```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py::test_compute_metrics -v
```

预期输出: 所有基本功能测试 `PASSED`

### 步骤 4.5: 提交

```bash
git add docs/topics/03-skills-system/codes_1/
git commit -m "feat: implement main metrics computation function (basic)"
```

---

## Task 5: 实现主函数（TDD - 第2部分：边界情况和异常处理）

**Files:**
- Modify: `docs/topics/03-skills-system/codes_1/tests/test_metrics.py`

### 步骤 5.1: 编写边界情况和异常测试

在 `test_metrics.py` 末尾添加:

```python
def test_compute_metrics_with_ignore_index():
    """测试忽略标签功能"""
    pred = np.array([[0, 1, -1], [1, 0, 2]])
    gt = np.array([[0, 1, -1], [1, 0, -1]])

    metrics = compute_segmentation_metrics(pred, gt, ignore_index=-1)

    # -1 位置应该被忽略
    # 有效的只有前4个元素: [0, 1, 1, 0]
    assert 0 <= metrics['miou'] <= 1


def test_compute_metrics_multiclass():
    """测试多类别情况（5类）"""
    np.random.seed(42)
    pred = np.random.randint(0, 5, (10, 10))
    gt = np.random.randint(0, 5, (10, 10))

    metrics = compute_segmentation_metrics(pred, gt)

    assert 0 <= metrics['miou'] <= 1
    assert len(metrics['per_class_metrics']) == 5


def test_compute_metrics_empty_class():
    """测试空类别处理（某个类别在 GT 中不存在）"""
    pred = np.array([[0, 0], [0, 0]])  # 只有类别 0
    gt = np.array([[0, 0], [0, 0]])

    metrics = compute_segmentation_metrics(pred, gt)

    # 类别0应该完全匹配
    assert metrics['miou'] == 1.0
    assert metrics['precision'] == 1.0
    assert metrics['recall'] == 1.0


def test_compute_metrics_class_in_pred_not_in_gt():
    """测试类别在 pred 中存在但 GT 中不存在"""
    pred = np.array([[0, 1], [1, 0]])
    gt = np.array([[0, 0], [0, 0]])  # GT 中只有类别 0

    metrics = compute_segmentation_metrics(pred, gt)

    # 类别1的所有指标应该为 0
    class_1_metric = metrics['per_class_metrics'][1]
    assert class_1_metric['class_id'] == 1
    assert class_1_metric['precision'] == 0.0
    assert class_1_metric['recall'] == 0.0
    assert class_1_metric['iou'] == 0.0


def test_compute_metrics_large_random():
    """测试大规模随机数据"""
    np.random.seed(123)
    pred = np.random.randint(0, 10, (100, 100))
    gt = np.random.randint(0, 10, (100, 100))

    metrics = compute_segmentation_metrics(pred, gt)

    assert 0 <= metrics['miou'] <= 1
    assert len(metrics['per_class_metrics']) == 10


def test_compute_metrics_per_class_sorted():
    """测试 per_class_metrics 按 class_id 排序"""
    pred = np.array([[0, 1, 2], [1, 2, 0]])
    gt = np.array([[0, 1, 1], [1, 2, 2]])

    metrics = compute_segmentation_metrics(pred, gt)

    # 验证 class_id 是升序排列
    class_ids = [m['class_id'] for m in metrics['per_class_metrics']]
    assert class_ids == sorted(class_ids)


def test_compute_metrics_shape_mismatch():
    """测试形状不匹配异常"""
    pred = np.array([[0, 1]])
    gt = np.array([[0, 1, 0]])

    with pytest.raises(ValueError, match="形状不匹配"):
        compute_segmentation_metrics(pred, gt)


def test_compute_metrics_wrong_dimensions():
    """测试错误维度异常"""
    pred = np.array([[[0], [1]], [[1], [0]]])  # 3D
    gt = np.array([[0, 1], [1, 0]])

    with pytest.raises(ValueError, match="必须是 2D 数组"):
        compute_segmentation_metrics(pred, gt)


def test_compute_metrics_wrong_type():
    """测试错误类型异常"""
    pred = [[0, 1], [1, 0]]  # list, not ndarray
    gt = np.array([[0, 1], [1, 0]])

    with pytest.raises(TypeError, match="必须是 NumPy 数组"):
        compute_segmentation_metrics(pred, gt)
```

### 步骤 5.2: 运行测试验证通过

运行:
```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py -v
```

预期输出: 所有测试 `PASSED` (主函数已经实现了完整的错误处理)

### 步骤 5.3: 提交

```bash
git add docs/topics/03-skills-system/codes_1/tests/test_metrics.py
git commit -m "test: add comprehensive edge case and exception tests"
```

---

## Task 6: 创建 README 文档

**Files:**
- Create: `docs/topics/03-skills-system/codes_1/README.md`

### 步骤 6.1: 编写 README

创建文档:

```markdown
# 语义分割精度指标计算

用于语义分割任务评估的 PR（Precision-Recall）和 mIoU（mean Intersection over Union）精度指标计算模块。

## 功能特性

- 支持 PR（Precision-Recall）和 mIoU 指标计算
- 自动推断类别数量
- 支持忽略指定标签（如边界区域）
- 返回每个类别的详细指标
- 纯 NumPy 实现，高效向量化计算

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

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

## API 参考

### `compute_segmentation_metrics(pred, gt, ignore_index=-1, eps=1e-10)`

计算语义分割的 PR、mIoU 指标。

**参数:**

- `pred` (np.ndarray): 预测标签数组，shape (H, W)，值为类别索引
- `gt` (np.ndarray): 真实标签数组，shape (H, W)，值为类别索引
- `ignore_index` (int, optional): 要忽略的标签值，默认 -1
- `eps` (float, optional): 防止除零的小值，默认 1e-10

**返回:**

字典包含:
- `precision` (float): 平均 Precision
- `recall` (float): 平均 Recall
- `miou` (float): 平均 IoU
- `per_class_metrics` (list): 每个类别的详细指标，按 `class_id` 升序排列

**异常:**

- `TypeError`: 输入不是 NumPy 数组
- `ValueError`: 形状不匹配、维度错误或数值范围错误

## 使用忽略标签

```python
# 假设 -1 表示忽略标签（如边界区域）
pred = np.array([[0, 1, -1], [1, 0, 2]])
gt = np.array([[0, 1, -1], [1, 0, -1]])

metrics = compute_segmentation_metrics(pred, gt, ignore_index=-1)
# -1 位置的像素会被忽略，不计入指标计算
```

## 运行测试

```bash
# 运行所有测试
pytest tests/test_metrics.py -v

# 运行测试并查看覆盖率
pytest tests/test_metrics.py --cov=metrics --cov-report=term-missing
```

## 指标说明

### IoU (Intersection over Union)

```
IoU = TP / (TP + FP + FN)
```

### Precision

```
Precision = TP / (TP + FP)
```

### Recall

```
Recall = TP / (TP + FN)
```

其中:
- TP (True Positive): 正确预测为该类的像素数
- FP (False Positive): 错误预测为该类的像素数
- FN (False Negative): 该类被错误预测为其他类的像素数

## 实现细节

- 使用混淆矩阵高效计算各项指标
- NumPy 向量化操作，避免 Python 循环
- 自动从数据推断类别数量
- 支持任意数量的类别

## 代码质量

```bash
# 代码格式化
black metrics.py tests/test_metrics.py

# 代码检查
flake8 metrics.py tests/test_metrics.py

# 类型检查
mypy metrics.py
```

## 许可证

MIT License

## 作者

Claude & ray

## 版本历史

- 0.1.0 (2026-03-27): 初始版本
```

保存到: `docs/topics/03-skills-system/codes_1/README.md`

### 步骤 6.2: 提交

```bash
git add docs/topics/03-skills-system/codes_1/README.md
git commit -m "docs: add comprehensive README with usage examples"
```

---

## Task 7: 代码质量检查和最终验证

**Files:**
- None (verification only)

### 步骤 7.1: 运行所有测试

```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py -v
```

预期输出: 所有测试 `PASSED`

### 步骤 7.2: 检查测试覆盖率

```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
python -m pytest tests/test_metrics.py --cov=metrics --cov-report=term-missing
```

预期输出:
- Coverage ≥ 95%
- 查看未覆盖的行（如果有）

### 步骤 7.3: 代码格式化

```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
black metrics.py tests/test_metrics.py
```

预期输出: 没有修改或已格式化

### 步骤 7.4: 代码检查

```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
flake8 metrics.py tests/test_metrics.py
```

预期输出: 没有错误

### 步骤 7.5: 类型检查

```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1
mypy metrics.py
```

预期输出: 没有错误

### 步骤 7.6: 提交任何代码质量修复

```bash
git add docs/topics/03-skills-system/codes_1/
git commit -m "style: apply code quality fixes from black, flake8, mypy"
```

---

## Task 8: 验收标准检查

### 步骤 8.1: 验证所有验收标准

检查清单:

- [ ] 所有单元测试通过
- [ ] 测试覆盖率 ≥ 95%
- [ ] 代码通过 Black、Flake8、mypy 检查
- [ ] README 文档完整
- [ ] 代码符合 PEP 8 规范
- [ ] 所有函数有完整 docstring

运行完整验证:

```bash
cd /Users/ray/code/claude-code-study/docs/topics/03-skills-system/codes_1

# 测试 + 覆盖率
pytest tests/test_metrics.py -v --cov=metrics --cov-report=term-missing --cov-report=html

# 代码质量
black --check metrics.py tests/test_metrics.py
flake8 metrics.py tests/test_metrics.py
mypy metrics.py
```

### 步骤 8.2: 最终提交

```bash
git add docs/topics/03-skills-system/codes_1/
git commit -m "feat: complete PR/mIoU metrics implementation

- Implement input validation with comprehensive error handling
- Add confusion matrix computation using vectorized operations
- Implement main metrics calculation function
- Achieve 95%+ test coverage with edge cases
- Add comprehensive README with examples
- Pass all code quality checks (Black, Flake8, mypy)"
```

---

## 执行顺序总结

按照此顺序执行任务，每完成一个任务就提交一次：

1. **Task 1**: 创建项目基础结构
2. **Task 2**: 实现输入验证函数（TDD）
3. **Task 3**: 实现混淆矩阵计算函数（TDD）
4. **Task 4**: 实现主函数 - 基本功能（TDD）
5. **Task 5**: 实现主函数 - 边界情况（TDD）
6. **Task 6**: 创建 README 文档
7. **Task 7**: 代码质量检查和修复
8. **Task 8**: 验收标准检查和最终提交

## 开发原则

- **TDD**: 先写测试，再写实现，最后重构
- **小步提交**: 每个任务完成后立即提交
- **DRY**: 避免代码重复
- **YAGNI**: 只实现当前需要的功能
- **频繁验证**: 每步都运行测试确保正确性

## 参考文档

- 设计规格: `docs/superpowers/specs/2026-03-27-pr-miou-metrics-design.md`
- 本实现计划: `docs/superpowers/plans/2026-03-27-pr-miou-metrics.md`
