## Pull Request template

Please, go through these steps before you submit a PR.

1. Make sure that your PR is not a duplicate.
2. If not, then make sure that:

   a. You have done your changes in a separate branch. Branches MUST have descriptive names that start with either the `fix/` or `feature/` prefixes. Good examples are: `fix/signin-issue` or `feature/issue-templates`.

   b. You have a descriptive commit message with a short title (first line).

   c. You have only one commit (if not, squash them into one commit).

   d. `npm test` doesn't throw any error. If it does, fix them first and amend your commit (`git commit --amend`).

3. **After** these steps, you're ready to open a pull request.

   a. Your pull request MUST NOT target the `master` branch on this repository. You probably want to target `staging` instead.

   b. Give a descriptive title to your PR.

   c. Describe your changes.

   d. Put `closes #XXXX` in your comment to auto-close the issue that your PR fixes (if such).

IMPORTANT: Please review the [CONTRIBUTING.md](../CONTRIBUTING.md) file for detailed contributing guidelines.

**PLEASE REMOVE MESSAGE ABOVE THIS POINT BEFORE SUBMITTING**

- **Please check if the PR fulfills these requirements**

* [ ] The commit message follows our guidelines
* [ ] Tests for the changes have been added (for bug fixes/features)
* [ ] Docs have been added / updated (for bug fixes / features)
* [ ] Have you checked to ensure there aren't other open [Pull Requests](../../../pulls) for the same update/change?

- **What kind of change does this PR introduce?** (Bug fix, feature, docs update, ...)

- **What is the current behavior?** (You can also link to an open issue here)

- **What is the new behavior (if this is a feature change)?**

- **Does this PR introduce a breaking change?** (What changes might users need to make in their application due to this PR?)

- **Other information**:

<!-- You can erase any parts of this template not applicable to your Pull Request. -->

### New Feature Submissions:

1. [ ] Does your submission pass tests?
2. [ ] Have you lint your code locally before submission?

### Changes to Core Features:

- [ ] Have you added an explanation of what your changes do and why you'd like us to include them?
- [ ] Have you written new tests for your core changes, as applicable?
- [ ] Have you successfully run tests locally with your changes?
