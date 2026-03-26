---
name: code-review-feedback
description: Use when providing code review feedback or receiving review comments
---

<EXTREMELY-IMPORTANT>
Code review feedback must be constructive, specific, and actionable. Focus on the code, not the person.
</EXTREMELY-IMPORTANT>

## When Providing Feedback

### Structure Your Feedback

For each issue you identify:

1. **Location** - File path and line number
2. **Problem** - Clear description of what's wrong
3. **Why it matters** - Explain the impact
4. **Suggestion** - Concrete recommendation for fixing

### Feedback Template

```markdown
### Issue: [Brief Title]

**Location**: `path/to/file.py:42`

**Problem**: [Clear description of the issue]

**Why it matters**: [Explain the impact - security, performance, maintainability, etc.]

**Suggested fix**:
```python
# Show the corrected code
```

**Priority**: 🔴 Must Fix / 🟡 Should Fix / 🟢 Nice to Have
```

### Feedback Guidelines

**Do**:
- Be specific and precise
- Explain the "why"
- Provide examples
- Acknowledge good work
- Suggest, don't demand

**Don't**:
- Use vague language ("it's weird")
- Criticize the person
- Say "fix this" without explanation
- Use sarcasm or humor
- Ignore the context

### Examples

**Good feedback**:
```markdown
### Issue: Missing type annotation

**Location**: `src/utils.py:42`

**Problem**: The `process_data` function is missing return type annotation.

**Why it matters**: Type annotations help with:
- IDE autocomplete and error detection
- Static type checking with mypy
- Documentation for other developers

**Suggested fix**:
```python
def process_data(items: List[Dict[str, Any]]) -> List[str]:
    return [item['name'] for item in items]
```

**Priority**: 🟡 Should Fix
```

**Bad feedback**:
```markdown
Line 42 is wrong. Add types.

Also the code is messy.
```

---

## When Receiving Feedback

### Process for Handling Review Comments

1. **Read carefully** - Understand each comment
2. **Ask questions** - If anything is unclear
3. **Consider the feedback** - Even if you disagree initially
4. **Implement changes** - Or explain why not
5. **Respond to all comments** - Even the ones you don't act on

### Responding to Feedback

**For accepted changes**:
```markdown
✓ Fixed - Updated the type annotation as suggested
```

**For declined changes**:
```markdown
⊘ Not changing - I considered this but decided against it because:
[Reasoning]

Alternative approach:
[What you're doing instead]
```

**For questions**:
```markdown
? Clarification needed - Could you explain more about:
[What's unclear]
```

### Handling Disagreement

If you disagree with feedback:

1. **Assume good intent** - The reviewer wants to help
2. **Understand the concern** - What are they worried about?
3. **Explain your reasoning** - Why did you make this choice?
4. **Discuss alternatives** - Is there a middle ground?
5. **Be willing to concede** - You might be wrong

**Example response**:
```markdown
Thanks for the feedback! I understand your concern about performance here.

However, I chose this approach because:
1. Readability is more important for this particular function
2. The performance difference is negligible (<1ms)
3. This matches the pattern used elsewhere in the codebase

That said, I'm open to alternatives. Would it help if I:
- Added a comment explaining the trade-off?
- Used a faster approach only in hot paths?
```

---

## Review Etiquette

### For Reviewers

- **Be timely** - Don't leave people waiting
- **Be thorough** - But don't delay for perfection
- **Be kind** - Assume good intentions
- **Be constructive** - Help, don't just critique

### For Authors

- **Be receptive** - Feedback helps you improve
- **Be responsive** - Answer questions promptly
- **Be patient** - Reviewers are volunteering time
- **Be grateful** - Someone is helping you

---

## Common Review Scenarios

### Style Issues

```markdown
### Issue: Code style

The code doesn't follow PEP 8 guidelines.

**Suggestion**: Run `black file.py` to auto-format
```

### Security Concerns

```markdown
### Issue: Security vulnerability

**Location**: `src/auth.py:15`

**Problem**: SQL injection risk - user input is directly interpolated into the query.

**Why it matters**: This could allow attackers to manipulate your database.

**Suggested fix**:
```python
# Instead of:
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Use parameterized queries:
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Priority**: 🔴 Must Fix - Critical security issue
```

### Performance Issues

```markdown
### Issue: Potential performance bottleneck

**Location**: `src/data.py:42-50`

**Problem**: The nested loop results in O(n²) complexity. For large datasets, this will be slow.

**Why it matters**: With 10,000 records, this takes ~5 seconds.

**Suggested fix**:
```python
# Use a dictionary for O(1) lookups
lookup = {item.id: item for item in items}
result = [lookup[key] for key in keys]
```

**Priority**: 🟡 Should Fix - Not critical now, but will become a problem
```

---

## Checklist for Effective Reviews

**For Reviewers**:
- [ ] Read the entire change first
- [ ] Understand the context and intent
- [ ] Check for bugs and logic errors
- [ ] Verify tests are included
- [ ] Check for security issues
- [ ] Consider performance implications
- [ ] Review code style and readability
- [ ] Verify documentation is updated
- [ ] Provide balanced feedback (positive + negative)
- [ ] Respond to follow-up questions

**For Authors**:
- [ ] Self-review before submitting
- [ ] Write a clear description of changes
- [ ] Include tests
- [ ] Update documentation
- [ ] Run the test suite
- [ ] Check for style issues
- [ ] Review similar previous changes
- [ ] Respond to all feedback
- [ ] Update the PR based on feedback
