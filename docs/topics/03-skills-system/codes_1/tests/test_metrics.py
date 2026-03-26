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
