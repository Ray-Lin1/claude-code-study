"""
语义分割精度指标计算模块

提供 PR (Precision-Recall) 和 mIoU (mean Intersection over Union) 指标的计算。
适用于语义分割任务的模型评估。
"""

import numpy as np

__version__ = "0.1.0"


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

    # 2. 维度检查（必须在形状检查之前）
    if pred.ndim != 2 or gt.ndim != 2:
        raise ValueError("输入必须是 2D 数组")

    # 3. 形状检查
    if pred.shape != gt.shape:
        raise ValueError(f"pred 和 gt 形状不匹配: {pred.shape} vs {gt.shape}")

    # 4. 数值范围检查（允许 -1 作为常见的 ignore_index）
    if (pred < -1).any() or (gt < -1).any():
        raise ValueError("标签索引不能为负数")
