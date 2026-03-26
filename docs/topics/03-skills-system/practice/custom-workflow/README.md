# 实践项目：自定义工作流 Skill

## 目标

创建一个完整的开发工作流 skill，组合多个最佳实践，实现从需求到部署的自动化流程。

## 难度

⭐⭐⭐☆☆

## 前置条件

- 完成 [Hello Skill](../hello-skill/) 练习
- 完成 [Code Review Skill](../code-review-skill/) 练习
- 理解 Agent 系统

## 学习要点

- 组合多个最佳实践
- 创建端到端的工作流
- 定义清晰的阶段和里程碑
- 处理工作流中的决策点

## 场景

创建一个完整的 Python 功能开发工作流，包括：

1. 需求理解和规划
2. 测试驱动开发
3. 代码实现
4. 代码审查
5. 文档编写
6. Git 提交流程

## 步骤

### 1. 设计工作流

定义流程图：

```
需求理解
    ↓
    ├→ 使用 brainstorming skill
    ↓
规划实现
    ↓
    ├→ 创建实现计划
    ↓
TDD 开发
    ↓
    ├→ 写失败测试
    ├→ 实现功能
    ├→ 测试通过
    ↓
代码审查
    ↓
    ├→ 自我审查
    ├→ 运行检查工具
    ↓
文档编写
    ↓
    ├→ 更新 README
    ├→ 添加注释
    ↓
Git 提交
    ↓
    ├→ 格式化提交信息
    ├→ 推送到远程
```

### 2. 编写 Skill

创建 `.claude/skills/python-feature-workflow.md`：

```markdown
---
name: python-feature-workflow
description: Use when implementing new features or fixing bugs in Python projects
---

<EXTREMELY-IMPORTANT>
Python 功能开发必须遵循以下顺序：
1. 理解需求（brainstorming）
2. 编写实现计划
3. TDD 开发（测试先行）
4. 代码审查（self-review）
5. 编写文档
6. Git 提交

跳过任何步骤都需要明确说明理由。
</EXTREMELY-IMPORTANT>

## 工作流概述

这是一个完整的 Python 功能开发流程，确保代码质量和团队协作。

### 阶段总览

| 阶段 | 目标 | 产出 |
|------|------|------|
| 1. 需求理解 | 明确要做什么 | 需求文档 |
| 2. 实现规划 | 设计怎么做 | 实现计划 |
| 3. TDD 开发 | 测试驱动的实现 | 测试 + 代码 |
| 4. 代码审查 | 确保质量 | 审查报告 |
| 5. 文档编写 | 记录使用方法 | 文档 |
| 6. Git 提交 | 版本控制 | 提交记录 |

---

## 阶段 1: 需求理解

### 目标
- 理解用户需求
- 明确功能边界
- 识别技术约束

### 步骤

<CHECKLIST>
- [ ] 阅读/讨论需求
- [ ] 提出澄清问题
- [ ] 识别依赖和约束
- [ ] 确认验收标准
</CHECKLIST>

### 问题框架

**功能理解**：
- 这个功能要解决什么问题？
- 谁会使用这个功能？
- 在什么场景下使用？

**边界识别**：
- 这个功能**不包括**什么？
- 什么情况应该返回错误？
- 极限情况是什么？

**技术约束**：
- 性能要求？
- 兼容性要求？
- 安全要求？

### 产出

创建或更新需求文档：

```markdown
# 功能：[名称]

## 背景
为什么要这个功能

## 需求
- 用户故事
- 验收标准

## 不包括
明确说明不在范围内的内容

## 技术考虑
- 性能
- 安全
- 兼容性
```

**示例**：
```markdown
# 功能：用户密码重置

## 背景
用户忘记密码时需要重置

## 需求
- 用户可以通过邮箱重置密码
- 重置链接 24 小时内有效
- 新密码必须符合强度要求

## 不包括
- 管理员重置用户密码（单独功能）
- 社交账号登录重置

## 技术考虑
- 安全：使用一次性 token
- 性能：邮件发送异步处理
```

---

## 阶段 2: 实现规划

### 目标
- 设计实现方案
- 识别关键文件
- 规划实现步骤

### 步骤

<CHECKLIST>
- [ ] 分析现有代码结构
- [ ] 设计 API 接口
- [ ] 识别需要修改的文件
- [ ] 规划实现步骤
- [ ] 考虑测试策略
</CHECKLIST>

### 实现计划模板

```markdown
# 实现计划：[功能名称]

## 技术方案
描述整体方案

## 文件变更
- 新增文件
- 修改文件
- 删除文件

## 实现步骤
1. 步骤 1
2. 步骤 2
3. 步骤 3

## 测试策略
- 单元测试
- 集成测试
- 边界测试
```

### 示例

```markdown
# 实现计划：密码重置

## 技术方案
1. 生成随机 token 存储在数据库
2. 发送包含 token 的邮件链接
3. 验证 token 并更新密码

## 文件变更
**新增**：
- `src/services/password_reset.py`
- `tests/test_password_reset.py`

**修改**：
- `src/api/routes.py` - 添加重置端点
- `src/models/user.py` - 添加 reset_token 字段

## 实现步骤
1. 创建密码重置服务
2. 添加 API 端点
3. 实现邮件发送
4. 编写测试

## 测试策略
- 正常重置流程
- Token 过期
- Token 无效
- 密码强度验证
```

---

## 阶段 3: TDD 开发

### 目标
- 测试先行开发
- 确保代码可测试
- 快速反馈循环

### TDD 循环

<CHECKLIST>
- [ ] 编写失败测试
- [ ] 确认测试失败
- [ ] 编写最少代码使测试通过
- [ ] 重构代码
- [ ] 重复
</CHECKLIST>

### 测试结构

```python
# tests/test_feature.py

import pytest

def test_basic_functionality():
    """测试基本功能"""
    # Arrange
    input_data = {...}

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_output

def test_edge_cases():
    """测试边界情况"""
    ...

def test_error_cases():
    """测试错误处理"""
    ...
```

### TDD 最佳实践

1. **一次一个测试**
   - 编写一个测试
   - 实现使它通过
   - 移动到下一个

2. **保持测试简单**
   - 每个测试一个断言（主要）
   - 清晰的测试名称
   - 良好的测试数据

3. **不要跳过重构**
   - 测试通过后重构
   - 确保测试仍然通过
   - 保持代码整洁

### 示例

```python
# 步骤 1: 写失败测试
def test_calculate_total():
    assert calculate_total([100, 200, 300]) == 600

# 运行: pytest -xvs
# 结果: FAILED (函数不存在)

# 步骤 2: 实现函数
def calculate_total(prices):
    return sum(prices)

# 运行: pytest -xvs
# 结果: PASSED ✓

# 步骤 3: 重构（如果需要）
# 步骤 4: 下一个测试
```

---

## 阶段 4: 代码审查

### 目标
- 确保代码质量
- 验证最佳实践
- 捕获潜在问题

### 自我审查检查清单

<CHECKLIST>
- [ ] 代码符合 PEP 8
- [ ] 所有函数有类型注解
- [ ] 公共函数有 docstring
- [ ] 错误处理适当
- [ ] 测试覆盖充分
- [ ] 没有硬编码的值
- [ ] 命名清晰有意义
- [ ] 函数职责单一
- [ ] 没有重复代码
- [ ] 性能考虑合理
</CHECKLIST>

### 自动化检查

```bash
# 在提交前运行所有检查

# 1. 代码格式化
black .

# 2. 导入排序
isort .

# 3. 代码检查
flake8 . --max-line-length=88

# 4. 类型检查
mypy .

# 5. 安全检查
bandit -r .

# 6. 测试 + 覆盖率
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

### 审查问题分类

**🔴 必须修复**：
- 类型错误
- 测试失败
- 安全问题
- 明显的 bug

**🟡 应该修复**：
- 代码风格
- 缺少文档
- 测试覆盖不足
- 命名不清晰

**🟢 建议改进**：
- 性能优化
- 代码简化
- 额外的文档

---

## 阶段 5: 文档编写

### 目标
- 记录使用方法
- 解释设计决策
- 帮助未来维护

### 文档类型

1. **代码文档**
   - 函数/类的 docstring
   - 复杂逻辑的注释

2. **用户文档**
   - README 更新
   - 使用指南
   - 示例代码

3. **技术文档**
   - API 文档
   - 架构说明
   - 设计决策记录（ADR）

### Docstring 模板

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """
    简短描述（一句话）

    详细描述（如果需要）

    Args:
        param1: 参数1的描述
        param2: 参数2的描述

    Returns:
        返回值的描述

    Raises:
        ErrorType: 何时抛出此错误

    Examples:
        >>> result = function_name(value1, value2)
        >>> expected_result
    """
    pass
```

### README 更新

如果功能对用户可见，更新 README：

```markdown
## 新功能

### 功能名称
简要描述

**使用方法**：
\```python
# 示例代码
\```

**配置选项**：
- option1: 描述
- option2: 描述

**注意事项**：
- 重要的使用说明
```

---

## 阶段 6: Git 提交

### 目标
- 清晰的版本历史
- 可追溯的变更
- 团队协作友好

### 提交前检查

<CHECKLIST>
- [ ] 所有测试通过
- [ ] 代码已格式化
- [ ] 文档已更新
- [ ] 没有调试代码
- [ ] 没有敏感信息
- [ ] 变更已审查
</CHECKLIST>

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码风格（不影响逻辑）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**：

```
feat(auth): add password reset functionality

Implement email-based password reset with time-limited tokens.

Changes:
- Add password reset service
- Create reset endpoint
- Send reset emails
- Add token validation

Tests:
- Unit tests for reset service
- Integration tests for API
- Edge case coverage

Closes #123
```

### 提交流程

```bash
# 1. 查看变更
git status
git diff

# 2. 暂存文件
git add file1.py file2.py

# 3. 提交
git commit -m "feat: add feature description"

# 4. 推送（如果合适）
git push origin feature-branch
```

### PR 描述模板

```markdown
## 变更概述
简要描述这个 PR 做了什么

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 文档更新

## 测试
描述如何测试这些变更

## 检查清单
- [ ] 代码符合风格指南
- [ ] 自我审查完成
- [ ] 添加/更新了测试
- [ ] 更新了文档
- [ ] 所有测试通过

## 相关 Issue
Closes #123
```

---

## 工作流变体

### 小型 Bug 修复

可以简化为：
1. 编写重现测试
2. 修复 bug
3. 验证测试通过
4. 提交

### 紧急热修复

可以跳过：
- 完整的规划阶段
- 详细的文档
- 但**必须**有测试！

### 大型功能

应该拆分为：
- 多个小的 PR
- 每个阶段独立审查
- 渐进式实现

---

## 注意事项

### 何时可以跳过步骤

**可以跳过**：
- 微小变更的完整规划
- 明显修复的详细文档

**不能跳过**：
- 测试（除非是纯文档变更）
- 代码审查（自我审查）
- 安全检查

### 常见陷阱

❌ **不要**：
- 在最后才写测试
- 跳过代码审查
- 忽略自动化检查
- 写模糊的提交信息

✅ **应该**：
- 按顺序执行各阶段
- 每个阶段完成检查清单
- 遵循团队约定
- 记录重要决策

---

## 工具集成

### Pre-commit Hook

```bash
# .git/hooks/pre-commit

#!/bin/bash
set -e

echo "Running pre-commit checks..."

# 格式化
black .
isort .

# 检查
flake8 .
mypy .

# 测试
pytest -x

echo "All checks passed!"
```

### Makefile 简化

```makefile
.PHONY: check test format lint

check: lint test
	@echo "All checks passed!"

test:
	pytest --cov=src --cov-fail-under=80

lint:
	flake8 .
	mypy .

format:
	black .
	isort .
```

使用：
```bash
make check    # 完整检查
make test     # 只运行测试
make format   # 格式化代码
```

---

## 成功标准

完成工作流后，应该：

- ✅ 所有检查清单完成
- ✅ 所有测试通过
- ✅ 代码符合标准
- ✅ 文档完整
- ✅ 变更已提交
- ✅ 可以安全部署

---

## 学习检查点

确保你理解：

- [ ] 为什么需要这个工作流
- [ ] 每个阶段的目的
- [ ] 何时可以简化流程
- [ ] 如何使用检查清单
- [ ] 工具如何自动化流程
- [ ] 如何处理异常情况

---

## 参考资源

- [TDD 最佳实践](https://testdriven.io/blog/tdd-best-practices/)
- [Git 提交约定](https://www.conventionalcommits.org/)
- [Python 文档约定](https://www.python.org/dev/peps/pep-0257/)
```

### 3. 测试工作流

尝试用这个 workflow 开发一个小功能：

```
使用 python-feature-workflow 实现一个计算器类，
支持加减乘除操作
```

### 4. 观察执行

注意 Claude 如何：
- 按顺序执行各个阶段
- 完成检查清单
- 在适当的时候寻求确认
- 处理决策点

## 验证检查点

- [ ] 工作流覆盖了完整的开发周期
- [ ] 每个阶段有明确的目标和产出
- [ ] Checklist 检查了关键点
- [ ] 提供了具体的示例
- [ ] 说明了何时可以简化
- [ ] 集成了自动化工具

## 扩展练习

1. **添加团队协作**：
   ```markdown
   ## 团队协作

   - 创建功能分支
   - 提交 PR
   - 请求审查
   - 处理反馈
   - 合并到主分支
   ```

2. **添加部署流程**：
   ```markdown
   ## 阶段 7: 部署

   - 更新 CHANGELOG
   - 打版本标签
   - 部署到测试环境
   - 验证部署
   - 部署到生产环境
   ```

3. **添加性能测试**：
   ```markdown
   ## 性能测试

   - 基准测试
   - 负载测试
   - 内存分析
   ```

## 常见问题

**Q: 工作流太长，每次都这样吗？**

A: 不是。小型变更可以简化，核心原则是：
- 保持测试
- 保持审查
- 保持质量

**Q: 如何处理紧急修复？**

A: 紧急修复可以快速通道，但：
- 必须有测试
- 事后补文档
- 进行事后分析

**Q: 团队不遵循这个流程？**

A: 逐步引入：
1. 从自己开始
2. 展示效果
3. 说服团队
4. 逐步采纳

## 下一步

完成本练习后，你已经掌握了：
- ✅ 创建简单 skills
- ✅ 创建领域特定 skills
- ✅ 创建完整工作流 skills

可以继续：
- 学习 [MCP 集成](../../04-mcp-integration/) - 扩展 Claude Code
- 学习 [高级工作流](../../05-advanced-workflows/) - 复杂场景

## 总结

自定义工作流 skills 是最强大的应用：
- 组合多个最佳实践
- 自动化重复流程
- 确保团队一致性
- 提高代码质量

关键要点：
1. 从小开始，逐步扩展
2. 基于实际需求设计
3. 保持灵活性和适应性
4. 持续迭代改进
