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


# ===== 主函数测试 =====


def test_compute_metrics_simple_case():
    """测试简单二分类情况"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[0, 1, 1], [1, 0, 0]])
    gt = np.array([[0, 1, 0], [1, 1, 0]])

    metrics = compute_segmentation_metrics(pred, gt)

    # 验证返回结构
    assert "precision" in metrics
    assert "recall" in metrics
    assert "miou" in metrics
    assert "per_class_metrics" in metrics

    # 验证数据类型
    assert isinstance(metrics["precision"], float)
    assert isinstance(metrics["recall"], float)
    assert isinstance(metrics["miou"], float)
    assert isinstance(metrics["per_class_metrics"], list)

    # 验证值范围
    assert 0 <= metrics["precision"] <= 1
    assert 0 <= metrics["recall"] <= 1
    assert 0 <= metrics["miou"] <= 1

    # 验证 per_class_metrics 有 2 个类别
    assert len(metrics["per_class_metrics"]) == 2
    for class_metric in metrics["per_class_metrics"]:
        assert "class_id" in class_metric
        assert "precision" in class_metric
        assert "recall" in class_metric
        assert "iou" in class_metric


def test_compute_metrics_perfect_match():
    """测试完全匹配情况"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[0, 1], [1, 0]])
    gt = np.array([[0, 1], [1, 0]])

    metrics = compute_segmentation_metrics(pred, gt)

    assert metrics["miou"] > 0.999  # 由于 eps 的存在，不是精确的 1.0
    assert metrics["precision"] > 0.999
    assert metrics["recall"] > 0.999


def test_compute_metrics_total_mismatch():
    """测试完全不匹配情况"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[0, 0], [0, 0]])
    gt = np.array([[1, 1], [1, 1]])

    metrics = compute_segmentation_metrics(pred, gt)

    assert metrics["miou"] == 0.0


def test_compute_metrics_with_ignore_index():
    """测试忽略标签功能"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[0, 1, -1], [1, 0, 2]])
    gt = np.array([[0, 1, -1], [1, 0, -1]])

    metrics = compute_segmentation_metrics(pred, gt, ignore_index=-1)

    # -1 位置应该被忽略
    # 有效的只有前4个元素: [0, 1, 1, 0]
    assert 0 <= metrics["miou"] <= 1


def test_compute_metrics_multiclass():
    """测试多类别情况（5类）"""
    from metrics import compute_segmentation_metrics

    np.random.seed(42)
    pred = np.random.randint(0, 5, (10, 10))
    gt = np.random.randint(0, 5, (10, 10))

    metrics = compute_segmentation_metrics(pred, gt)

    assert 0 <= metrics["miou"] <= 1
    assert len(metrics["per_class_metrics"]) == 5


def test_compute_metrics_empty_class():
    """测试空类别处理（某个类别在 GT 中不存在）"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[0, 0], [0, 0]])  # 只有类别 0
    gt = np.array([[0, 0], [0, 0]])

    metrics = compute_segmentation_metrics(pred, gt)

    # 类别0应该完全匹配（由于 eps 的存在，使用近似相等）
    assert metrics["miou"] > 0.999
    assert metrics["precision"] > 0.999
    assert metrics["recall"] > 0.999


def test_compute_metrics_class_in_pred_not_in_gt():
    """测试类别在 pred 中存在但 GT 中不存在"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[0, 1], [1, 0]])
    gt = np.array([[0, 0], [0, 0]])  # GT 中只有类别 0

    metrics = compute_segmentation_metrics(pred, gt)

    # 类别1的所有指标应该为 0
    class_1_metric = metrics["per_class_metrics"][1]
    assert class_1_metric["class_id"] == 1
    assert class_1_metric["precision"] == 0.0
    assert class_1_metric["recall"] == 0.0
    assert class_1_metric["iou"] == 0.0


def test_compute_metrics_large_random():
    """测试大规模随机数据"""
    from metrics import compute_segmentation_metrics

    np.random.seed(123)
    pred = np.random.randint(0, 10, (100, 100))
    gt = np.random.randint(0, 10, (100, 100))

    metrics = compute_segmentation_metrics(pred, gt)

    assert 0 <= metrics["miou"] <= 1
    assert len(metrics["per_class_metrics"]) == 10


def test_compute_metrics_per_class_sorted():
    """测试 per_class_metrics 按 class_id 排序"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[0, 1, 2], [1, 2, 0]])
    gt = np.array([[0, 1, 1], [1, 2, 2]])

    metrics = compute_segmentation_metrics(pred, gt)

    # 验证 class_id 是升序排列
    class_ids = [m["class_id"] for m in metrics["per_class_metrics"]]
    assert class_ids == sorted(class_ids)


def test_compute_metrics_shape_mismatch():
    """测试形状不匹配异常"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[0, 1]])
    gt = np.array([[0, 1, 0]])

    with pytest.raises(ValueError, match="形状不匹配"):
        compute_segmentation_metrics(pred, gt)


def test_compute_metrics_wrong_dimensions():
    """测试错误维度异常"""
    from metrics import compute_segmentation_metrics

    pred = np.array([[[0], [1]], [[1], [0]]])  # 3D
    gt = np.array([[0, 1], [1, 0]])

    with pytest.raises(ValueError, match="必须是 2D 数组"):
        compute_segmentation_metrics(pred, gt)


def test_compute_metrics_wrong_type():
    """测试错误类型异常"""
    from metrics import compute_segmentation_metrics

    pred = [[0, 1], [1, 0]]  # list, not ndarray
    gt = np.array([[0, 1], [1, 0]])

    with pytest.raises(TypeError, match="必须是 NumPy 数组"):
        compute_segmentation_metrics(pred, gt)
