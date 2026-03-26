# Skills 系统 - 学习笔记

## Skills 系统概述

### 什么是 Skills？

**定义**：Skills 是 Claude Code 中的可重用提示词模板，用于自动化工作流程和强制执行最佳实践。

**核心特征**：
- **模板化**：预定义的提示词结构
- **可激活**：通过 Skill 工具或自动激活
- **上下文感知**：可访问当前对话状态
- **可组合**：多个 skill 可以协同工作

### Skills vs Superpowers

| 特性 | Skills | Superpowers |
|------|--------|-------------|
| 来源 | 用户创建 | 官方提供 |
| 用途 | 项目特定 | 通用最佳实践 |
| 激活 | 手动或自动 | 自动检测 |
| 可修改 | 是 | 否 |

**关系**：Superpowers 是高质量的官方 skills，可以作为参考。

### 为什么使用 Skills？

1. **自动化重复任务**
   ```
   每次提交代码都要格式化、运行测试、检查类型
   → 创建 "git-commit" skill 一次性完成
   ```

2. **强制执行标准**
   ```
   团队约定所有函数都要有类型注解
   → 创建 "add-function" skill 自动添加
   ```

3. **减少认知负担**
   ```
   不需要每次都记住完整的测试流程
   → skill 包含完整的 checklist
   ```

4. **知识共享**
   ```
   新人不需要学习所有工作流程
   → 激活相应的 skill 即可
   ```

## Skill 结构与语法

### 基本结构

```markdown
---
name: skill-name
description: 简短描述这个 skill 的用途
---

<SUBAGENT-STOP>
如果作为子 agent 被调用时跳过此 skill
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
强制执行规则
</EXTREMELY-IMPORTANT>

## 详细说明

具体的 skill 内容和指令...
```

### 元数据字段

**必需字段**：

1. **name**
   ```yaml
   name: test-driven-development
   ```
   - skill 的唯一标识符
   - 使用 kebab-case 命名
   - 用于激活和引用

2. **description**
   ```yaml
   description: Use when implementing any feature or bugfix
   ```
   - 简短描述何时使用此 skill
   - 帮助自动检测和手动选择

**可选字段**：

3. **parameters**
   ```yaml
   parameters:
     - name: coverage
       type: number
       required: false
       description: Minimum test coverage percentage
   ```

### 指令块类型

#### 1. SUBAGENT-STOP 块

```markdown
<SUBAGENT-STOP>
如果作为子 agent 执行特定任务，跳过此 skill
</SUBAGENT-STOP>
```

**用途**：防止在子 agent 中递归激活同一个 skill

**示例**：
- brainstorming skill 不需要在 Plan agent 中激活
- TDD skill 不需要在新子 agent 中重复激活

#### 2. EXTREMELY-IMPORTANT 块

```markdown
<EXTREMELY-IMPORTANT>
这些规则不可协商，必须严格遵守
</EXTREMELY-IMPORTANT>
```

**用途**：标记核心、不可违反的规则

**示例**：
- "必须在写代码前写测试"
- "绝对不能跳过类型检查"

#### 3. CHECKLIST 块

```markdown
<CHECKLIST>
- [ ] 步骤 1
- [ ] 步骤 2
- [ ] 步骤 3
</CHECKLIST>
```

**用途**：定义必须完成的任务清单

**效果**：自动创建待办事项，逐步完成

## Skill 类型分类

### 按灵活性分类

#### 1. 刚性 Skills (Rigid)

**特征**：
- 严格按步骤执行
- 不允许偏离或跳过
- 通常是检查清单式

**示例**：
- TDD（测试驱动开发）
- Systematic Debugging
- Verification Before Completion

**使用场景**：
- 安全关键任务
- 合规要求
- 质量保证流程

#### 2. 灵活 Skills (Flexible)

**特征**：
- 提供原则和指导
- 可根据上下文调整
- 允许判断和适应

**示例**：
- Brainstorming
- Code Patterns
- Frontend Design

**使用场景**：
- 创意任务
- 需要判断的决策
- 不同上下文的变化

### 按用途分类

#### 1. 进程 Skills (Process)

**控制如何工作**：
- `brainstorming` - 创造性工作前的头脑风暴
- `systematic-debugging` - 调试问题的结构化方法
- `test-driven-development` - 测试先行的开发流程
- `writing-plans` - 编写实现计划

#### 2. 实现 Skills (Implementation)

**指导具体执行**：
- `frontend-design` - 前端组件设计
- `mcp-builder` - MCP 服务器构建
- 特定语言/框架的 skills

#### 3. 用户可调用 Skills (User-Invocable)

**通过斜杠命令调用**：
- `/commit` - Git 提交
- `/review-pr` - PR 审查
- 自定义命令

**格式**：
```yaml
name: my-command
user_invocable: true
```

### 按 Skill 优先级

当多个 skills 可能适用时：

1. **进程优先**：
   ```
   "让我们构建 X"
   → brainstorming first (process)
   → frontend-design second (implementation)
   ```

2. **具体性优先**：
   ```
   通用 TDD vs React-specific TDD
   → 使用更具体的那个
   ```

3. **用户指令最高**：
   ```
   Skill 说 "使用 TDD"
   但 CLAUDE.md 说 "不需要测试"
   → 遵循 CLAUDE.md
   ```

## 创建自定义 Skills

### Step 1: 识别需求

**问题模式**：
```
每次做 X 时，我都要重复解释：
1. ...
2. ...
3. ...
```

**转化为 skill**：
```
创建一个 skill，让 Claude Code 自动知道这个流程
```

**常见场景**：
- 项目特定的提交流程
- 特定的代码风格要求
- 复杂的测试设置
- 部署流程

### Step 2: 编写 Skill

**模板**：

```markdown
---
name: your-skill-name
description: 何时使用此 skill
---

<EXTREMELY-IMPORTANT>
核心不可违反的规则
</EXTREMELY-IMPORTANT>

## 背景信息

解释为什么需要这个 skill，它解决了什么问题。

## 工作流程

<CHECKLIST>
- [ ] 步骤 1：描述
- [ ] 步骤 2：描述
- [ ] 步骤 3：描述
</CHECKLIST>

## 详细说明

每个步骤的具体说明...

## 注意事项

- 什么不要做
- 常见陷阱
- 特殊考虑
```

### Step 3: 存放 Skill

**选项 1：项目级别**
```
your-project/
└── .claude/
    └── skills/
        └── your-skill.md
```

**选项 2：全局级别**
```
~/.claude/
└── skills/
    └── your-skill.md
```

### Step 4: 测试 Skill

1. **激活 skill**：
   ```bash
   # Claude Code 会自动检测
   # 或手动激活
   /activate-skill your-skill-name
   ```

2. **验证行为**：
   - 检查是否按预期执行
   - 确认步骤顺序正确
   - 验证输出符合期望

3. **迭代改进**：
   - 根据实际使用调整
   - 添加遗漏的细节
   - 简化冗余部分

## 最佳实践与设计原则

### 1. 清晰的命名

**好的命名**：
```
❌ bad: "do-stuff"
✅ good: "test-driven-development"
✅ good: "python-code-review"
```

**原则**：
- 使用动词-名词结构
- 描述性但不冗长
- 遵循 kebab-case

### 2. 具体的描述

```
❌ 模糊：description: "A skill for code"
✅ 具体：description: "Use when implementing any feature or bugfix"
```

### 3. 适度的约束

**过度约束**：
```markdown
<EXTREMELY-IMPORTANT>
- 必须使用精确的 4 空格缩进
- 每行必须在 88 字符
- 必须有类型注解
- 必须有文档字符串
- 必须通过 mypy
- 必须通过 black
- 必须通过 flake8
- ... (太多!)
</EXTREMELY-IMPORTANT>
```

**适度约束**：
```markdown
<EXTREMELY-IMPORTANT>
在写实现代码前，先写失败的测试
</EXTREMELY-IMPORTANT>

其他建议：
- 遵循项目代码风格（CLAUDE.md）
- 运行格式化工具
- 通过类型检查
```

### 4. 提供上下文

```markdown
## 背景

这个 skill 基于 Clean Code 原则。
我们的项目价值：简洁 > 聪明

因此：
- 优先使用简单解决方案
- 避免过早优化
- 代码可读性优于巧妙性
```

### 5. 避免"保姆式" Skills

**不好的做法**：
```markdown
每做任何事之前：
1. 检查是否...
2. 确认是否...
3. 验证是否...
```

**好的做法**：
```markdown
何时使用：
- 需要实现新功能时
- 修复 bug 时

不要使用：
- 简单的重命名
- 明显的 typo 修复
```

### 6. 指令优先级

**优先级顺序**：
1. **用户直接指令** - 最高
2. **Skills** - 中等
3. **默认行为** - 最低

**示例**：
```
用户说："快速修复这个 typo"
Skill 说："写测试前不要写代码"
→ 遵循用户指令（快速修复）
```

### 7. 平台兼容性

**工具映射**：
```markdown
在 Claude Code 中使用 Read 工具
在 Gemini 中使用 file_reader 工具

参见工具映射表：references/codex-tools.md
```

### 8. 模块化和组合

**小而专注**：
```
✅ tdd-skill - 只负责 TDD 流程
✅ python-style-skill - 只负责 Python 风格
✅ django-pattern-skill - 只负责 Django 模式
```

**可组合使用**：
```
实现 Django 功能：
1. brainstorming (规划)
2. tdd (开发)
3. django-pattern (实现)
4. python-style (格式化)
```

## 高级特性

### 1. 条件激活

**基于上下文**：
```yaml
description: Use when working with React components
```

Claude Code 会根据任务描述自动判断是否激活。

### 2. 参数化 Skills

**定义参数**：
```yaml
---
name: run-tests
description: Run test suite with configurable options
parameters:
  - name: coverage
    type: number
    required: false
    default: 80
    description: Minimum coverage percentage
  - name: verbose
    type: boolean
    required: false
    default: false
    description: Show detailed output
---
```

**使用参数**：
```
/run-tests --coverage 90 --verbose
```

### 3. Skill 组合

**一个 skill 调用另一个**：
```markdown
## 流程

1. 首先激活 brainstorming-skill
2. 然后激活 tdd-skill
3. 最后激活 code-review-skill
```

### 4. 动态 Checklist

**基于条件生成**：
```markdown
<CHECKLIST>
{{ if python }}
- [ ] Run mypy
- [ ] Run black
- [ ] Run pytest
{{ endif }}

{{ if javascript }}
- [ ] Run eslint
- [ ] Run prettier
- [ ] Run jest
{{ endif }}
</CHECKLIST>
```

### 5. 交互式 Skills

**需要用户输入**：
```markdown
## 配置

此 skill 需要配置：

请提供：
1. 默认分支名称（main/master）
2. 测试框架（pytest/unittest）
3. 代码风格指南（PEP 8/Google）

在 CLAUDE.md 中配置这些选项。
```

## 常见问题

### Q: Skill 没有激活？

**检查**：
1. description 是否清晰？
2. 是否符合当前任务？
3. 是否被 `<SUBAGENT-STOP>` 阻止？
4. 用户指令是否覆盖了 skill？

### Q: Skill 太僵化？

**解决**：
1. 将刚性规则移到 `<EXTREMELY-IMPORTANT>`
2. 将建议性规则作为普通文本
3. 添加"何时不要使用"部分

### Q: 多个 Skills 冲突？

**优先级**：
1. 用户指令 > 所有
2. 具体 > 通用
3. 后激活 > 先激活

### Q: 如何调试 Skill？

**方法**：
1. 添加调试输出：
   ```markdown
   ## 调试信息

   Skill 已激活，当前步骤：X
   ```
2. 简化 skill，逐步添加
3. 使用简单任务测试

## Skill 编写指南

### 模板清单

编写 skill 时确保包含：

- [ ] 清晰的 name（kebab-case）
- [ ] 具体的 description（何时使用）
- [ ] SUBAGENT-STOP 块（如需要）
- [ ] EXTREMELY-IMPORTANT 块（核心规则）
- [ ] 背景和上下文
- [ ] CHECKLIST（步骤清单）
- [ ] 详细说明
- [ ] 注意事项和陷阱
- [ ] 示例（如有帮助）

### 审查标准

**好的 skill**：
- ✅ 目标明确
- ✅ 步骤清晰
- ✅ 不过度约束
- ✅ 可验证结果
- ✅ 易于理解

**需要改进**：
- ❌ 模糊不清
- ❌ 过度复杂
- ❌ 过于僵化
- ❌ 缺少上下文
- ❌ 难以遵循

## 实际示例

### 示例 1: 简单 Greeting Skill

```markdown
---
name: friendly-greeting
description: Use when greeting users at the start of conversation
---

<EXTREMELY-IMPORTANT>
Always greet users in a friendly, professional manner.
</EXTREMELY-IMPORTANT>

## Greeting Guidelines

- Use the user's name if known
- Be welcoming and positive
- Keep it concise (1-2 sentences)
- Ask how you can help

## Examples

Good: "Hello Ray! How can I help you today?"
Bad: "Hi. What do you want?"
```

### 示例 2: Python Function Skill

```markdown
---
name: python-function
description: Use when creating new Python functions
---

<EXTREMELY-IMPORTANT>
Every function must have:
1. Type hints for all parameters and return value
2. A docstring explaining what it does
3. At least one example usage in docstring
</EXTREMELY-IMPORTANT>

## Checklist

<CHECKLIST>
- [ ] Write function signature with type hints
- [ ] Add docstring with:
  - Brief description
  - Parameters (with types)
  - Returns (with type)
  - Raises (if any)
  - Example
- [ ] Implement function body
- [ ] Add edge case handling
- [ ] Write unit tests
</CHECKLIST>

## Code Template

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """
    Brief description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ErrorType: When error condition occurs

    Example:
        >>> result = function_name(value1, value2)
        >>> expected_output
    """
    # Implementation here
    pass
```

## Don't Forget

- Keep functions focused on one responsibility
- Use descriptive names
- Avoid global state
- Handle errors gracefully
```

## 下一步学习

完成本主题后，可以继续学习：
- [MCP 服务器集成](../04-mcp-integration/) - 扩展 Claude Code 能力
- [高级工作流](../05-advanced-workflows/) - 复杂场景的最佳实践
- [团队协作](../06-team-collaboration/) - 在团队中使用 Skills

## 练习建议

1. 从简单开始：创建一个 greeting skill
2. 观察现有 skills：学习 superpowers skills 的结构
3. 解决实际问题：创建解决重复任务的 skill
4. 迭代改进：根据使用反馈优化
5. 分享交流：与团队分享有用的 skills
