# /agent-git

Expert Git workflow manager.

## Git Commands
```bash
# Branching
git checkout -b feature/new-feature
git branch -d feature/merged
git branch -D feature/force-delete

# Stashing
git stash
git stash pop
git stash list
git stash drop

# History
git log --oneline -10
git log --graph --all
git blame file.py
git show commit-hash

# Undoing
git reset --soft HEAD~1  # Keep changes
git reset --hard HEAD~1  # Discard changes
git revert commit-hash   # New commit that undoes

# Cherry-pick
git cherry-pick commit-hash

# Rebasing
git rebase main
git rebase -i HEAD~3  # Interactive
```

## Branch Strategy
```
main        → Production
develop     → Integration
feature/*   → New features
bugfix/*    → Bug fixes
hotfix/*    → Production fixes
release/*   → Release prep
```

## Commit Convention
```
feat: Add user authentication
fix: Resolve login redirect issue
docs: Update API documentation
style: Format code with prettier
refactor: Extract validation logic
test: Add user service tests
chore: Update dependencies
```

## PR Template
```markdown
## Summary
[Brief description]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [ ] Unit tests pass
- [ ] Manual testing done

## Screenshots
[If applicable]
```
