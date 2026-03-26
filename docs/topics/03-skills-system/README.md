# 主题名称：Skills 系统

## 概述

本主题深入介绍 Claude Code 的 Skills 系统，学习如何创建、配置和使用自定义技能来自动化工作流程、强制执行最佳实践，并提升开发效率。

## 前置知识

- [Claude Code 基础](../01-basics/) - 已完成 ✅
- [Agent 与任务管理](../02-agents-and-tasks/) - 已完成 ✅
- 理解模板和提示词工程的基本概念

## 学习内容

1. [Skills 系统概述](notes.md#skills-系统概述)
2. [Skill 结构与语法](notes.md#skill-结构与语法)
3. [Skill 类型分类](notes.md#skill-类型分类)
4. [创建自定义 Skills](notes.md#创建自定义-skills)
5. [最佳实践与设计原则](notes.md#最佳实践与设计原则)
6. [高级特性](notes.md#高级特性)

## 实践项目

- [创建第一个 Skill](practice/hello-skill/) - 难度：⭐☆☆☆☆
  - 创建简单的 greeting skill，理解基本结构
- [代码审查 Skill](practice/code-review-skill/) - 难度：⭐⭐☆☆☆
  - 创建项目特定的代码审查规范和检查规则
- [自定义工作流 Skill](practice/custom-workflow/) - 难度：⭐⭐⭐☆☆
  - 组合多个最佳实践，创建完整的开发流程

## 代码示例

参见 [examples/](./examples/) 目录：
- `simple-skill.md` - 最简单的 skill 示例
- `parameterized-skill.md` - 带参数的 skill
- `interactive-skill.md` - 需要用户交互的 skill

## 参考资料

- [Claude Code Skills 文档](https://docs.anthropic.com/claude-code/skills)
- [Superpowers Skills 仓库](https://github.com/anthropics/superpowers)
- [Skill 编写指南](notes.md#skill-编写指南)

## 学习进度

- [ ] 阅读笔记
- [ ] 运行示例
- [ ] 完成实践项目
- [ ] 创建自己的 skill
- [ ] 整理心得

## 关键要点

### 什么是 Skills？

Skills 是可重用的提示词模板，可以：
- 自动化重复性工作流程
- 强制执行最佳实践
- 确保团队一致性
- 减少认知负担

### Skill 的核心价值

1. **一致性**：确保相同任务每次都以相同方式执行
2. **效率**：避免重复解释相同的工作流程
3. **质量**：内嵌专家知识和最佳实践
4. **可维护性**：集中管理工作流程定义

---
最后更新：2026-03-22
