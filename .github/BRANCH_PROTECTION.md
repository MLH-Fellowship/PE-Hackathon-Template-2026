# Branch Protection Setup

These rules must be configured manually in GitHub since they can't be set via code.

Go to **Settings → Branches → Add branch ruleset** for each branch.

## `main` branch protection

| Setting                                     | Value     |
|---------------------------------------------|-----------|
| Require a pull request before merging        | Yes       |
| Required approvals                           | 1         |
| Dismiss stale pull request approvals         | Yes       |
| Require status checks to pass before merging | Yes       |
| Required status checks                       | `Lint`, `Test` |
| Require branches to be up to date            | Yes       |
| Restrict who can push                        | Yes (admin only) |
| Do not allow force pushes                    | Yes       |
| Do not allow deletions                       | Yes       |

## `staging` branch protection

| Setting                                     | Value     |
|---------------------------------------------|-----------|
| Require a pull request before merging        | Yes       |
| Required approvals                           | 1         |
| Require status checks to pass before merging | Yes       |
| Required status checks                       | `Lint`, `Test` |
| Require branches to be up to date            | Yes       |
| Do not allow force pushes                    | Yes       |
| Do not allow deletions                       | Yes       |

## Setup Steps

1. Go to your repo on GitHub.
2. Navigate to **Settings → Branches**.
3. Click **Add branch ruleset**.
4. Set the branch name pattern (e.g., `main`).
5. Enable the settings from the table above.
6. Repeat for `staging`.

> **Note:** The required status checks (`Lint` and `Test`) will only appear in the dropdown after the CI workflow has run at least once. Push a branch and open a PR first to trigger CI, then configure the required checks.

## Create the `staging` branch

If the `staging` branch doesn't exist yet:

```bash
git checkout main
git checkout -b staging
git push -u origin staging
```
