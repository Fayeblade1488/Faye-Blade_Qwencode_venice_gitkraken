# Recommended Branch Protection Rules

This document outlines the recommended branch protection rules for this repository. These should be configured in GitHub repository settings.

## Main Branch Protection

Navigate to: **Settings** → **Branches** → **Add branch protection rule**

### Branch Name Pattern
```
main
```

### Protection Settings

#### ✅ Required Reviews
- **Require pull request reviews before merging**: ✓
  - Required approving reviews: `1`
  - Dismiss stale pull request approvals when new commits are pushed: ✓
  - Require review from Code Owners: ✓ (if CODEOWNERS file exists)

#### ✅ Status Checks
- **Require status checks to pass before merging**: ✓
  - Require branches to be up to date before merging: ✓
  - Status checks that are required:
    - `test` (from tests.yml workflow)
    - `lint` (from linting.yml workflow)
    - `security` (from security.yml workflow)

#### ✅ Conversation Resolution
- **Require conversation resolution before merging**: ✓

#### ✅ Commit Signature
- **Require signed commits**: ✓ (recommended but optional)

#### ✅ Linear History
- **Require linear history**: ✓ (recommended for cleaner history)

#### ✅ Force Push Protection
- **Do not allow force pushes**: ✓
- **Do not allow deletions**: ✓

#### ⚠️ Administration
- **Allow administrators to bypass**: ✗ (unchecked - even admins should follow rules)
- **Restrict who can push to matching branches**: Consider restricting to maintainers only

## Additional Recommendations

### CODEOWNERS File
Create a `.github/CODEOWNERS` file to automatically request reviews:

```
# Global owners
* @Fayeblade1488

# Specific file owners
/docs/ @Fayeblade1488
/.github/ @Fayeblade1488
```

### Rulesets (GitHub Rulesets - Beta Feature)
Consider using GitHub's new Rulesets feature for more granular control:

1. Navigate to **Settings** → **Rules** → **Rulesets**
2. Create a new ruleset with:
   - Target branches: `main`
   - Rules:
     - Restrict creations
     - Restrict updates
     - Restrict deletions
     - Require pull request before merging
     - Require status checks to pass

### Tag Protection
Protect release tags:
1. Navigate to **Settings** → **Tags** → **Protected tags**
2. Add pattern: `v*`
3. Allow only maintainers to create tags

## Security Settings

### Dependency Graph
- **Enable Dependency graph**: ✓ (in Security & Analysis)
- **Enable Dependabot alerts**: ✓
- **Enable Dependabot security updates**: ✓

### Code Scanning
- **Enable CodeQL**: ✓
- Configure to run on: `push`, `pull_request`, `schedule`

### Secret Scanning
- **Enable secret scanning**: ✓
- **Enable push protection**: ✓ (prevents accidental commits of secrets)

## Continuous Integration

Ensure these workflows are active:
- **Tests** (`.github/workflows/tests.yml`)
- **Linting** (`.github/workflows/linting.yml`)
- **Security Scanning** (`.github/workflows/security.yml`)

## Merge Settings

Recommended merge button settings:
- **Allow merge commits**: ✓
- **Allow squash merging**: ✓
- **Allow rebase merging**: ✓
- **Automatically delete head branches**: ✓

Default merge commit message:
- **Default to pull request title and description**

## For Collaborators

### Required Actions Before Merge
1. All CI checks must pass
2. At least 1 approving review
3. All conversations resolved
4. Branch is up to date with main
5. No merge conflicts

### Commit Message Guidelines
Follow conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Tests
- `chore:` Maintenance

## Emergency Override

In case of critical production issues:
1. Document the reason for override
2. Create an incident report
3. Fix the issue
4. Create a follow-up PR to address properly

---

**Implementation Status**: ⚠️ To be configured in GitHub repository settings

**Last Updated**: 2025-09-30