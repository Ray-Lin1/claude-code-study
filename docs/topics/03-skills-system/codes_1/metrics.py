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


def _compute_confusion_matrix(
    pred: np.ndarray,
    gt: np.ndarray,
    num_classes: int,
    ignore_index: int,
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
    mask = gt != ignore_index
    pred_filtered = pred[mask]
    gt_filtered = gt[mask]

    # 使用向量化操作计算混淆矩阵
    # 将 (gt, pred) 对编码为单个索引
    indices = num_classes * gt_filtered + pred_filtered

    # 使用 bincount 统计每个索引的出现次数
    cm = np.bincount(indices, minlength=num_classes**2)

    # 重塑为矩阵
    return cm.reshape(num_classes, num_classes)
