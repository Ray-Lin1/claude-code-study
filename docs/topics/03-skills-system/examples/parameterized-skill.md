---
name: run-tests
description: Use when running test suites with configurable options
parameters:
  - name: coverage
    type: number
    description: Minimum test coverage percentage (default: 80)
    required: false
  - name: verbose
    type: boolean
    description: Show detailed test output (default: false)
    required: false
  - name: parallel
    type: boolean
    description: Run tests in parallel (default: false)
    required: false
---

<EXTREMELY-IMPORTANT>
Always ensure tests pass before claiming code is working. Never skip tests.
</EXTREMELY-IMPORTANT>

## Test Execution Flow

Follow this process when running tests:

### 1. Prepare Environment

```bash
# Ensure we're in a clean state
python -m pytest --clean-alluredir
```

### 2. Run Tests

**Basic run**:
```bash
python -m pytest
```

**With coverage** (if `coverage` parameter is set):
```bash
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under={{coverage}}
```

**Verbose output** (if `verbose` is true):
```bash
python -m pytest -v -s
```

**Parallel execution** (if `parallel` is true):
```bash
python -m pytest -n auto
```

### 3. Check Results

Verify:
- All tests passed
- Coverage meets minimum requirement
- No warnings or errors

### 4. Report Failure

If tests fail:
1. Identify which tests failed
2. Read the error messages
3. Understand the root cause
4. Propose a fix

## Output Format

When tests pass:
```
✓ All tests passed (N tests)
✓ Coverage: X% (minimum: {{coverage}}%)
```

When tests fail:
```
✗ Tests failed: M of N tests failed
✗ Coverage: X% (minimum: {{coverage}}%)

Failed tests:
- test_module::test_function
  Error: assertion failed
  ...
```

## Notes

- Default coverage is 80% if not specified
- Use verbose mode when debugging specific test failures
- Parallel execution can speed up large test suites but may hide race conditions
