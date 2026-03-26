# Agent 与任务管理 - 学习笔记

## Agent 系统概述

### 什么是 Agent？

Agent 是 Claude Code 中的子进程，专门设计用于处理特定类型的任务。每个 Agent 类型都有专门的工具集和优化策略。

### 为什么使用 Agent？

1. **专门化**：不同 Agent 针对不同任务优化
2. **并行处理**：可同时运行多个 Agent 处理独立任务
3. **上下文隔离**：每个 Agent 有独立的对话上下文
4. **可追踪**：Agent 的执行过程可以被监控和追踪

## Task 工具使用

### 基本语法

```
Task(subagent_type="类型", prompt="任务描述", description="简短描述")
```

### 参数说明

- `subagent_type`: Agent 类型（必需）
- `prompt`: 详细的任务描述（必需）
- `description`: 3-5 词的简短描述（必需）
- `model`: 可选，指定模型（haiku/sonnet/opus）
- `resume`: 可选，恢复之前的 Agent ID

### 返回值

Agent 执行完成后会返回一个结果消息和 Agent ID。

## 可用的 Agent 类型

### 1. Bash
- **用途**：执行命令行操作
- **工具**：Bash
- **适用场景**：Git 操作、文件操作、系统命令

### 2. General-purpose
- **用途**：通用的复杂任务处理
- **工具**：所有可用工具
- **适用场景**：需要多步骤的复杂任务、不确定任务类型时

### 3. Explore
- **用途**：快速探索代码库
- **工具**：除 Task/Edit/Write/NotebookEdit 外的所有工具
- **适用场景**：
  - 查找文件模式（如 `src/components/**/*.tsx`）
  - 搜索代码关键词
  - 理解代码库结构

**Thoroughness 级别**：
- `quick`: 基本搜索
- `medium`: 适度探索
- `very thorough`: 全面分析

### 4. Plan
- **用途**：设计实现方案
- **工具**：除 Task/Edit/Write/NotebookEdit 外的所有工具
- **适用场景**：
  - 规划实现策略
  - 识别关键文件
  - 考虑架构权衡

### 5. Code-reviewer
- **用途**：代码审查
- **工具**：所有工具
- **适用场景**：
  - 验证代码与计划的一致性
  - 检查编码标准
  - 完成主要项目步骤后审查

### 6. Code-simplifier
- **用途**：简化和优化代码
- **工具**：所有工具
- **适用场景**：
  - 提高代码清晰度
  - 保持功能的同时改进可维护性

## 最佳实践

### 1. 何时使用 Task 工具

**应该使用**：
- 开放式搜索（需要多轮尝试）
- 需要多个 Glob/Grep 调用
- 复杂的多步骤任务
- 代码库探索

**不应使用**：
- 读取特定文件路径 → 用 Read
- 搜索特定类定义 → 用 Glob
- 搜索单个文件内容 → 用 Read 或 Grep

### 2. 并行调用

当任务独立时，可以在一条消息中调用多个 Agent：

```
并行执行：
- Agent 1: 处理任务 A
- Agent 2: 处理任务 B
- Agent 3: 处理任务 C
```

### 3. 任务描述规范

- **description**: 3-5 词，简洁概括
- **prompt**: 详细描述，包含所有必要的上下文

### 4. Agent 选择优先级

1. **Process skills first**: brainstorming, debugging
2. **Implementation skills second**: frontend-design, mcp-builder

## 常见场景

### 场景 1: 代码库探索

使用 Explore Agent 找到相关文件：

```
Task(subagent_type="Explore", prompt="找到所有处理用户认证的文件",
     description="查找认证相关文件")
```

### 场景 2: 实现规划

使用 Plan Agent 设计方案：

```
Task(subagent_type="Plan", prompt="设计一个用户登录功能",
     description="规划登录功能")
```

### 场景 3: 代码审查

完成实现后使用 Code-reviewer：

```
Task(subagent_type="Code-reviewer", prompt="审查登录功能的实现",
     description="审查登录实现")
```

### 场景 4: 并行处理

同时执行多个独立任务：

```
# 调用 3 个 Explore Agent 并行搜索不同模式
```

## Agent 类型参考

| Agent 类型 | 用途 | 工具限制 | 典型使用场景 |
|-----------|------|---------|------------|
| Bash | 命令执行 | Bash | Git, 文件操作 |
| General-purpose | 通用任务 | * | 不确定类型时 |
| Explore | 代码探索 | 除编辑工具 | 查找文件, 搜索代码 |
| Plan | 方案设计 | 除编辑工具 | 架构设计, 实现规划 |
| Code-reviewer | 代码审查 | * | PR 审查, 代码验证 |
| Code-simplifier | 代码优化 | * | 重构, 代码清理 |

## 注意事项

1. **Agent 不可见**：Agent 的输出不会直接显示给用户，需要你总结结果
2. **上下文传递**：拥有"访问当前上下文"权限的 Agent 可以看到完整对话历史
3. **明确任务类型**：告诉 Agent 是做研究还是写代码
4. **进度追踪**：使用 `run_in_background` 参数后台运行 Agent
5. **恢复执行**：使用 `resume` 参数和 Agent ID 恢复之前的 Agent

## 练习建议

1. 从简单的 Explore Agent 开始
2. 尝试并行调用多个 Agent
3. 学习使用 Plan Agent 进行任务拆解
4. 实践 Code-reviewer 验证自己的代码

## 下一步

完成本主题学习后，可以继续学习：
- [03-topic](待定) - 更高级的主题
- 实际项目中的应用
