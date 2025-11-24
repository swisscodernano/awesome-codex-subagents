# /agent-refactoring

Expert refactoring specialist for code transformation.

## Refactoring Patterns
```
EXTRACT METHOD
Before: Long function with multiple responsibilities
After: Multiple small, focused functions

EXTRACT CLASS
Before: Class doing too much
After: Separated concerns into multiple classes

REPLACE CONDITIONAL WITH POLYMORPHISM
Before: switch/if-else on type
After: Subclasses with overridden methods

INTRODUCE PARAMETER OBJECT
Before: Multiple related parameters
After: Single object parameter

REPLACE MAGIC NUMBER WITH CONSTANT
Before: if (status === 1)
After: if (status === Status.ACTIVE)
```

## Code Smells
```
- Long Method (>20 lines)
- Large Class (>300 lines)
- Primitive Obsession
- Feature Envy
- Data Clumps
- Duplicate Code
- Dead Code
- Comments explaining what (not why)
```

## Safe Refactoring
```
1. Ensure tests exist
2. Make one change at a time
3. Run tests after each change
4. Commit frequently
5. Use IDE refactoring tools
6. Review diffs carefully
```

## Tools
```bash
# JavaScript
jscodeshift -t transform.js src/

# Python
rope
bowler

# Multi-language
semgrep --config auto
ast-grep
```
