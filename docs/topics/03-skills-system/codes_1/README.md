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
