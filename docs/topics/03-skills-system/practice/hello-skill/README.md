# 实践项目：创建第一个 Skill

## 目标

创建一个简单的 greeting skill，学习 Skill 的基本结构和激活机制。

## 难度

⭐☆☆☆☆

## 学习要点

- Skill 的基本结构
- 元数据字段（name, description）
- 指令块的使用
- 如何激活和测试 skill

## 步骤

### 1. 创建 Skill 文件

在你的项目目录下创建：

```bash
mkdir -p .claude/skills
```

### 2. 编写 Skill

创建 `.claude/skills/friendly-greeting.md`：

```markdown
---
name: friendly-greeting
description: Use when starting a conversation or greeting the user
---

<EXTREMELY-IMPORTANT>
Always greet users in a friendly, personalized manner.
</EXTREMELY-IMPORTANT>

## Greeting Guidelines

When starting a conversation:

1. **Use their name** if known (e.g., "Hello Ray!")
2. **Be welcoming** and positive
3. **Keep it concise** - 1-2 sentences maximum
4. **Offer help** - Ask how you can assist

## Examples

✅ **Good greetings**:
- "Hello Ray! How can I help you today?"
- "Hi Ray! What would you like to work on?"
- "Hey Ray! Ready to tackle some code?"

❌ **Bad greetings**:
- "Hi."
- "What do you want?"
- [No greeting at all]

## Notes

- Don't be overly formal
- Don't use emojis unless requested
- Don't write long paragraphs
- Always end with a question or offer to help
```

### 3. 测试 Skill

启动 Claude Code 并尝试：

```
# 直接问候
Hello!

# 或者说
Hi
```

### 4. 观察行为

注意 Claude 如何：
- 使用你的名字（如果知道）
- 保持友好但专业
- 简洁地问候
- 主动提供帮助

## 验证检查点

- [ ] Skill 文件创建在正确位置
- [ ] Claude Code 自动加载了 skill
- [ ] 问候行为符合预期
- [ ] 使用了友好的语气
- [ ] 提供了帮助的意愿

## 扩展练习

完成基本版本后，尝试：

1. **添加中文支持**：
   ```markdown
   ## Language Support

   Greet in the user's preferred language:
   - English: "Hello [name]!"
   - 中文: "你好 [name]！"
   - 根据对话上下文判断语言
   ```

2. **添加时间感知**：
   ```markdown
   ## Time-Aware Greetings

   - 早上 (6-12): "Good morning, [name]!"
   - 下午 (12-18): "Good afternoon, [name]!"
   - 晚上 (18-22): "Good evening, [name]!"
   - 深夜 (22-6): "Working late, [name]?"
   ```

3. **添加上下文记忆**：
   ```markdown
   ## Context Awareness

   If continuing a previous conversation:
   - Reference what we were working on
   - Ask if they want to continue

   Example: "Welcome back, Ray! Would you like to continue
   working on the Skills system documentation?"
   ```

## 常见问题

**Q: Skill 没有激活？**

A: 检查：
1. 文件路径是否正确（`.claude/skills/`）
2. 文件名是否是 `.md` 结尾
3. description 是否描述了何时使用

**Q: 如何确认 skill 已加载？**

A: 启动 Claude Code 时，查看加载信息：
```
Loaded skill: friendly-greeting
```

**Q: Skill 行为不符合预期？**

A: 检查 `<EXTREMELY-IMPORTANT>` 块中的规则是否清晰

## 下一步

完成本练习后，继续：
- [代码审查 Skill](../code-review-skill/) - 学习更复杂的 skill
- [自定义工作流 Skill](../custom-workflow/) - 组合多个最佳实践

## 参考答案

参见 [examples/simple-skill.md](../../examples/simple-skill.md)
