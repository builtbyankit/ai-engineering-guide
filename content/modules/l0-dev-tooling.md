---
title: Git, the command line and Docker
level: L0
kind: core
hours: 6–8
summary: Work from the terminal, track and review code with git and GitHub, package an app in a Docker container and run tests automatically on every push.
checked: 2026-10-16
---

## Why it matters

Agent projects are ordinary software projects. You will clone repositories, run commands, review changes, build containers and keep secrets out of public history. These tools also appear inside agents: coding agents run shell commands and git, and most deployed agents run in containers.

Good tooling makes your work reproducible. When a project builds the same way on your laptop, in a container and in CI, you spend your time on the agent instead of on setup problems. A clean repository with a README and passing tests is also the first thing employers and collaborators look at. [Deploying agent applications](#l6-deployment) in Level 6 builds on everything here.

## What to learn

- **The shell**: a text interface for running programs. Learn to move around (`cd`, `ls`, `pwd`), inspect files (`cat`, `less`, `grep`), chain commands with pipes and set environment variables.
- **Git's model**: git stores snapshots of your project called commits, linked into a history. A branch is a movable name that points at one commit.
- **The everyday git loop**: `git status`, `git add`, `git commit`, `git switch -c` for a new branch, `git merge`, `git pull` and `git push`. Small commits with clear messages make problems easy to find and undo.
- **GitHub and pull requests**: GitHub hosts your repository online. A pull request proposes merging a branch, shows the diff for review and runs automated checks before you merge.
- **.gitignore and secrets**: a `.gitignore` file lists files git should never track, such as `.env`, `.venv` and caches. If a key does get pushed, revoke it first, because deleting the commit leaves copies in clones and caches.
- **Images and containers**: an image is a packaged snapshot of an app plus everything it needs to run. A container is a running instance of an image, isolated from the rest of your machine.
- **Dockerfile and Compose**: a Dockerfile lists the steps to build an image, starting from a base such as an official slim Python image. Docker Compose starts several containers together, such as an API and a database, from one YAML file.
- **CI with GitHub Actions**: continuous integration (CI) means running checks automatically on every change. In GitHub Actions, a workflow file in `.github/workflows/` runs jobs when events such as a push or pull request happen. The usual first workflow installs dependencies and runs your tests.
- **A good README**: say what the project does, how to install and run it, how to run the tests and which settings it needs. A newcomer should have it running in about 10 minutes.

## Resources

### Start here

- [The Missing Semester of Your CS Education](https://missing.csail.mit.edu/) · MIT · Course · Free · 3–4 h — In the 2026 edition, watch the lectures on the shell, version control and packaging and shipping code, which cover the terminal, git internals and Docker with exercises.
- [Introduction to GitHub](https://github.com/skills/introduction-to-github) · GitHub Skills · Course · Free · 1 h — A guided exercise inside a real repository where you create a branch, commit, open a pull request and merge it.
- [Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) · GitHub · Docs · Free · 30 min — A complete workflow that sets up Python, installs dependencies and runs pytest on every push.

### Go deeper

- [Pro Git](https://git-scm.com/book/en/v2) · Scott Chacon and Ben Straub · Book · Free · self-paced — The standard git book; chapters 2, 3 and 6 cover the basics, branching and working with GitHub.
- [Learn Git Branching](https://learngitbranching.js.org/) · pcottle · Tool · Free · 1–2 h — Interactive browser levels that draw your commit graph as you branch, merge and rebase.
- [Get started](https://docs.docker.com/get-started/) · Docker · Docs · Free · 2 h — The Docker concepts series explains containers, images, Dockerfiles, layers, ports and Compose with hands-on steps.
- [Python language-specific guide](https://docs.docker.com/guides/python/) · Docker · Tutorial · Free · 1–2 h — Containerizes a small FastAPI app with a Dockerfile, `.dockerignore` and Compose file, then adds a database.
- [Understanding GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions) · GitHub · Docs · Free · 10 min — Defines workflows, events, jobs, actions and runners so the YAML files make sense.
- [Make a README](https://www.makeareadme.com/) · Danny Guo · Article · Free · 15 min — Lists the sections a README usually needs and gives an editable template to start from.

### Reference

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) · Docker · Docs · Free · reference — Every Dockerfile instruction with syntax and examples, including shell form versus exec form.
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) · GitHub · Docs · Free · reference — The full list of workflow keys such as `on`, `jobs`, `steps`, `env` and matrix strategies.
- [Python.gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore) · GitHub · Repo · Free · reference — GitHub's maintained template that already ignores `.env`, `.venv` and Python caches.
- [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) · GitHub · Docs · Free · reference — What to do after pushing a secret, starting with revoking it, and why rewriting history alone is not enough.

## Practice

1. **Shell warm-up.** In a folder of notes or text files, use only the shell to count the files, find every line containing a chosen word with `grep -r`, and save the matches to a file with `>`. Done when you can repeat it from memory.
2. **Branch and pull request.** Put your project from [Python for AI engineering](#l0-python-for-ai) on GitHub with a Python `.gitignore`. Make a change on a branch, open a pull request, read the diff and merge it. Done when `main` shows the merged commit and `git status` is clean.
3. **Containerize.** Write a Dockerfile for a small FastAPI app, build it, run it with a published port and open `/docs` in your browser. Add a `.dockerignore` so `.env` and `.venv` stay out of the image. Done when one `docker run` command starts the service.
4. **Add CI.** Add a GitHub Actions workflow that installs dependencies and runs pytest on every push and pull request. Break a test on a branch and confirm the pull request shows a failing check. Done when the check turns green after the fix.
5. **Write the README.** Include a one-line description, setup steps, how to run the tests, how to run with Docker and the environment variables needed. Done when someone else, or you in a fresh clone, can follow it without asking questions.

## Checklist

- [ ] [Must ship] Push a project to GitHub with a `.gitignore` that excludes `.env` and `.venv`.
- [ ] [Must ship] Merge at least one change through a branch and a pull request.
- [ ] [Must ship] Build and run a Docker image of a small Python app.
- [ ] [Must ship] Add a GitHub Actions workflow that runs your tests on every push.
- [ ] [Recommended] Write a README that takes a stranger from clone to passing tests.
- [ ] [Recommended] Add a `compose.yaml` that starts your app with one command.
- [ ] [Stretch] Add a workflow status badge to the README and turn on secret scanning for the repository.

## You're ready when

- You can explain the difference between a commit, a branch and a pull request.
- You can explain the difference between an image and a container and what each line of your Dockerfile does.
- Your repository has passing CI, no secrets in its history and a README that gets a newcomer running.
- You can name the first thing to do when a secret lands in a public repository.
