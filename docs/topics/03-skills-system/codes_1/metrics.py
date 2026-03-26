"""
语义分割精度指标计算模块

提供 PR (Precision-Recall) 和 mIoU (mean Intersection over Union) 指标的计算。
适用于语义分割任务的模型评估。
"""

from typing import Any

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


def compute_segmentation_metrics(
    pred: np.ndarray,
    gt: np.ndarray,
    ignore_index: int = -1,
    eps: float = 1e-10,
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

        per_class_metrics.append(
            {
                "class_id": i,
                "precision": float(precision),
                "recall": float(recall),
                "iou": float(iou),
            }
        )

    # 计算平均指标
    avg_precision = np.mean([m["precision"] for m in per_class_metrics])
    avg_recall = np.mean([m["recall"] for m in per_class_metrics])
    avg_iou = np.mean([m["iou"] for m in per_class_metrics])

    return {
        "precision": float(avg_precision),
        "recall": float(avg_recall),
        "miou": float(avg_iou),
        "per_class_metrics": per_class_metrics,
    }
