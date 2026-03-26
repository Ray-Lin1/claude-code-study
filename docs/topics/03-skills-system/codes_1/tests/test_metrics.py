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
    # -1 应该被允许，因为它是常见的 ignore_index
    # 但当前的 _validate_inputs 不接受 ignore_index 参数
    # 这个测试暂时跳过
    pytest.skip("需要实现 ignore_index 参数支持")


# ===== 混淆矩阵测试 =====


def test_compute_confusion_matrix_simple_case():
    """测试简单的二分类混淆矩阵"""
    from metrics import _compute_confusion_matrix

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
    from metrics import _compute_confusion_matrix

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
    from metrics import _compute_confusion_matrix

    np.random.seed(42)
    pred = np.random.randint(0, 5, (10, 10))
    gt = np.random.randint(0, 5, (10, 10))

    cm = _compute_confusion_matrix(pred, gt, num_classes=5, ignore_index=-1)

    assert cm.shape == (5, 5)
    # 所有像素都应该被统计
    assert cm.sum() == 100  # 10x10 = 100 pixels
