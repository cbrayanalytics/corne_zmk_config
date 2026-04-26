Push the current branch to GitHub and report the CI build status.

Steps:
1. Run `git status` to show the current working tree state
2. Run `git push` to push any unpushed commits
3. Run `gh run list --limit 1 --json databaseId,url,status,displayTitle --jq '.[0]'` to get the latest Actions run
4. Report the GitHub Actions run URL and current status so the user can monitor the firmware build
