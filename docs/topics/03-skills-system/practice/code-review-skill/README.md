# 实践项目：代码审查 Skill

## 目标

创建一个项目特定的代码审查 skill，定义代码质量标准和审查流程。

## 难度

⭐⭐☆☆☆

## 前置条件

- 完成 [Hello Skill](../hello-skill/) 练习
- 理解 Skill 的基本结构

## 学习要点

- 定义项目特定的标准
- 创建结构化的审查流程
- 使用 checklist 确保完整性
- 处理不同的代码场景

## 步骤

### 1. 分析需求

你的项目需要什么样的代码审查？

考虑：
- 编码风格标准
- 安全性要求
- 性能考虑
- 测试覆盖要求
- 文档要求

### 2. 编写 Skill

创建 `.claude/skills/code-review.md`：

```markdown
---
name: python-code-review
description: Use when reviewing Python code changes, PRs, or implementation
---

<EXTREMELY-IMPORTANT>
代码审查必须：
1. 确认所有代码符合 PEP 8 标准
2. 验证所有函数都有类型注解
3. 确认所有公共函数都有 docstring
4. 检查适当的错误处理
5. 验证测试覆盖率不低于 80%
</EXTREMELY-IMPORTANT>

## 审查流程

<CHECKLIST>
- [ ] 理解变更目的
- [ ] 检查代码风格
- [ ] 验证类型注解
- [ ] 审查错误处理
- [ ] 检查测试覆盖
- [ ] 评估性能影响
- [ ] 验证文档完整性
- [ ] 提供改进建议
</CHECKLIST>

## 1. 理解变更目的

在开始审查前：
- 阅读 PR 描述或提交信息
- 理解要解决的问题
- 了解实现方法

**提问**：
- 这个变更解决了什么问题？
- 为什么选择这种实现方式？

## 2. 代码风格检查

**Python (PEP 8)**：
- [ ] 4 空格缩进
- [ ] 每行不超过 88 字符
- [ ] 使用 snake_case 命名变量和函数
- [ ] 使用 PascalCase 命名类
- [ ] 导入顺序：标准库 → 第三方 → 本地

**工具验证**：
```bash
black . --check
flake8 .
isort . --check-only
```

## 3. 类型注解检查

**要求**：
- 所有函数参数必须有类型注解
- 所有函数必须有返回类型注解
- 使用具体类型，避免过度使用 `Any`

**示例**：
```python
# ✅ Good
def calculate_discount(price: float, percentage: float) -> float:
    return price * (1 - percentage / 100)

# ❌ Bad
def calculate_discount(price, percentage):
    return price * (1 - percentage / 100)
```

**工具验证**：
```bash
mypy .
```

## 4. 错误处理检查

**原则**：
- 指定具体的异常类型，避免裸 `except:`
- 提供有意义的错误消息
- 在适当的边界处理错误

**示例**：
```python
# ✅ Good
try:
    result = divide(a, b)
except ZeroDivisionError as e:
    logger.error(f"Cannot divide {a} by zero")
    raise ValueError("Divisor cannot be zero") from e

# ❌ Bad
try:
    result = divide(a, b)
except:
    pass
```

## 5. 测试覆盖检查

**最低要求**：80% 覆盖率

**检查项**：
- [ ] 新功能有单元测试
- [ ] 边界情况被测试
- [ ] 错误路径被测试
- [ ] 测试名称描述性

**工具验证**：
```bash
pytest --cov=src --cov-report=term-missing
```

## 6. 性能影响评估

**考虑**：
- 时间复杂度是否合理？
- 是否有不必要的循环嵌套？
- 是否应该使用生成器？
- 内存使用是否高效？

**问题**：
- 这个函数在大数据集上表现如何？
- 是否有明显的性能瓶颈？

## 7. 文档完整性

**公共 API 需要**：
- [ ] 模块级 docstring
- [ ] 类 docstring
- [ ] 公共函数/方法 docstring
- [ ] 参数说明
- [ ] 返回值说明
- [ ] 异常说明
- [ ] 使用示例

**内部函数**：
- 至少有简短的注释说明用途

## 8. 提供改进建议

**反馈格式**：

对于每个问题：
1. **指出位置**：文件路径和行号
2. **描述问题**：清晰简洁
3. **解释原因**：为什么这是问题
4. **建议改进**：具体的修复建议

**示例反馈**：
```markdown
### 问题：缺少类型注解

**位置**：`src/utils.py:42`

**描述**：`process_data` 函数缺少参数和返回类型注解

**原因**：类型注解有助于 IDE 自动补全、静态检查和文档理解

**建议**：
```python
def process_data(items: List[Dict[str, Any]]) -> List[str]:
    ...
```
```

## 审查优先级

按重要性排序：

### 🔴 必须修复 (Must Fix)
- 安全漏洞
- 类型错误
- 测试失败
- 明显的 bug

### 🟡 应该修复 (Should Fix)
- 代码风格问题
- 缺少错误处理
- 测试覆盖不足
- 文档缺失

### 🟢 建议改进 (Nice to Have)
- 性能优化
- 代码简化
- 命名改进
- 额外的文档

## 特殊场景

### 重构变更
- 关注行为是否保持一致
- 检查是否有遗漏的功能
- 验证测试是否充分

### 性能优化
- 验证性能确实提升
- 检查是否引入了 bug
- 确认代码可读性未受损

### Bug 修复
- 确认修复了根本原因
- 验证不会引入新问题
- 检查是否有回归测试

## 审查完成后

### 通过标准
- ✅ 所有 🔴 必须修复问题已解决
- ✅ 大部分 🟡 应该修复问题已解决
- ✅ 测试全部通过
- ✅ 代码质量达标

### 需要修改
- ❌ 存在未解决的 🔴 问题
- ❌ 测试失败
- ❌ 严重违反编码标准

## 注意事项

- **建设性反馈**：专注于代码，不是人
- **解释原因**：不只是说"改这个"，解释为什么
- **承认偏好**：有些问题只是风格偏好，明确标注
- **表扬优点**：也指出做得好的地方

## 工具集成

推荐的工作流：

```bash
# 1. 格式化代码
black .

# 2. 排序导入
isort .

# 3. 检查风格
flake8 .

# 4. 类型检查
mypy .

# 5. 运行测试
pytest --cov

# 6. 人工审查
# （使用本 skill）
```
```

### 3. 测试 Skill

创建一个需要审查的文件：

```python
# test_file.py

def add(a, b):
    return a + b

def calculate(data):
    result = 0
    for item in data:
        result = result + item
    return result
```

然后要求 Claude Code 审查：
```
请审查 test_file.py
```

### 4. 观察输出

确认审查包含：
- 类型注解检查
- 代码风格检查
- 文档检查
- 具体的改进建议

## 验证检查点

- [ ] Skill 定义了清晰的审查标准
- [ ] Checklist 涵盖了所有重要方面
- [ ] 提供了具体的代码示例
- [ ] 区分了不同优先级的问题
- [ ] 包含了工具验证命令

## 扩展练习

1. **添加框架特定检查**：
   ```markdown
   ## Django 特定检查

   - [ ] 使用 get() 或 get_object_or_404() 而不是 filter()
   - [ ] 模型有 __str__ 方法
   - [ ] 查询使用 select_related() 或 prefetch_related()
   ```

2. **添加安全检查**：
   ```markdown
   ## 安全检查

   - [ ] 用户输入已验证
   - [ ] SQL 注入防护
   - [ ] XSS 防护
   - [ ] 敏感数据不在日志中
   ```

3. **添加性能检查清单**：
   ```markdown
   ## 性能检查

   - [ ] 数据库查询已优化（N+1 问题）
   - [ ] 避免在循环中查询数据库
   - [ ] 使用缓存当合适时
   - [ ] 大文件使用流式处理
   ```

## 常见问题

**Q: 如何让 skill 适应不同项目？**

A: 可以创建多个特定项目的 skills：
- `python-code-review`
- `javascript-code-review`
- `go-code-review`

**Q: 如何平衡严格性和实用性？**

A: 在 `<EXTREMELY-IMPORTANT>` 中放必须项，其他作为建议

**Q: 审查太慢怎么办？**

A: 使用工具自动化大部分检查，人工审查关注逻辑和架构

## 下一步

完成本练习后，继续：
- [自定义工作流 Skill](../custom-workflow/) - 组合多个 skills

## 参考资源

- [PEP 8 风格指南](https://peps.python.org/pep-0008/)
- [Google Python 风格指南](https://google.github.io/styleguide/pyguide.html)
- [Effective Python](https://effectivepython.com/)
