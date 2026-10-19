---
title: How to use this guide
summary: What the guide covers, how levels, modules, milestones and projects fit together, how long it takes and how your progress is saved.
---

## Who this guide is for
This guide is for anyone who can write small programs and wants to build AI agents professionally. You might be a student, a developer from another field or a career switcher. You should be able to write a short program on your own in any language, using variables, loops, functions and files, and fix it by reading the error message. You do not need machine learning experience or advanced maths. If you are newer to programming than that, take a beginner course such as Harvard's free CS50P first, then come back.

By the end you will be able to design, build, evaluate, secure and deploy agents that use tools, retrieve knowledge and ask a person before risky actions. You will also have eight projects on GitHub to show for it.

The guide uses Python throughout. It does not cover TypeScript agent stacks or voice and realtime agents. The ideas carry over, but for those you will need each platform's own documentation.

## How the guide is organised
The guide has seven levels and a capstone. Each level has a few modules, one project and a milestone. Work through them in order, because each level builds on the one before.

%%LEVEL_TABLE%%

The **Interview prep** section sits outside the levels. It doesn't count toward the time estimates or progress totals, so open it whenever an interview is coming up. It works best after [Level 3](#L3).

## How a module works
Every module page has the same parts, so you always know where you are.

- **Why it matters**: the problem this module solves for someone building agents.
- **What to learn**: the core ideas in plain words. Read this first, then use the resources to go deeper.
- **Resources**: hand-picked links in three groups. *Start here* is the minimum path. *Go deeper* is for topics you want to master. *Reference* is documentation to keep open while you build.
- **Practice**: small exercises that turn reading into skill.
- **Checklist**: tasks with a label. *Must ship* tasks are the core of the module and fit inside its time estimate. *Recommended* and *Stretch* tasks are extra.
- **You're ready when**: statements to test yourself against before you move on.

Tick a resource when you have read or watched it. Tick a task when it is done. When you finish a page, press **Mark page as complete** at its end. Completed pages get a tick in the sidebar and in the module lists, and every tick counts towards your progress.

## Milestones and projects
Each level ends with a project and a milestone. The project is a portfolio piece you build on your own, using what the level taught. Its page gives you a brief, requirements, stretch goals, a suggested stack, step-by-step guidance and a rubric to judge your work.

The milestone is a short list of checks at the bottom of each level page. Tick them when you can honestly say yes. When every check is ticked, the level is complete.

The [capstone](#capstone) comes last. You build a new agent from scratch that uses every core skill in the guide, then deploy it and write it up.

## Core path and optional modules
Most modules are core. A few are marked **Optional** because they suit particular roles, such as coding agents, browser agents, fine-tuning open models or system design. Choose the **Core path**, **Everything** or the **Fast track** in the sidebar. Your choice changes the time estimate, the progress totals and the next and previous links. Modules outside your choice stay readable, but they are dimmed in the sidebar and in the level lists and aren't counted.

At 10 to 12 hours a week, the core path takes about %%CORE_WEEKS%%, everything takes about %%FULL_WEEKS%% and the fast track takes about %%FAST_WEEKS%%. Time estimates cover the Start here resources, the practice, the must-ship tasks and the projects. Treat them as time boxes. If a module runs long, finish its must-ship tasks and move on; you can come back for the rest.

## Fast track for experienced developers
If you already write Python and use web APIs, SQL, git and Docker at work, choose the **Fast track**. It skips four Level 0 modules: Python, web APIs, SQL and tooling. It keeps [Just enough machine learning](#l0-ml-concepts), because most developers have not met those ideas at work.

Build the [Level 0 project](#p0-api-service) anyway. It doubles as a placement check. If it takes you a few evenings, the skipped modules would have been review. If it takes much longer, go back to the module where you got stuck.

In every other module, read **You're ready when** first. If you can already do everything it lists, do the must-ship tasks and move on. Expect most of the new material in Levels 1 to 5. Level 6 deployment will feel familiar, so spend that time on the parts specific to agents, such as durable runs, gateways and eval gates.

## How your progress is saved
Your ticks are saved in your browser's local storage on this device. Nothing is sent to a server and you do not need an account. This also means a different browser, a different device or clearing your site data starts you from zero.

To keep your progress safe, open [Your progress](#progress) and download a backup file now and then. You can restore it on any device, and you can choose to merge it with what is already there or replace it.

## Choosing between resources
- **Start with the Start here picks.** They are chosen so that, with the practice, they fit the module's time estimate.
- **Prefer official docs for anything that changes.** API parameters, SDK names and model lists change often. Articles and videos teach the ideas; docs tell you the current details.
- **Most resources are free.** A few are marked "Free tier", which means free to use with paid extras such as certificates or higher limits. Anything marked "Paid" is optional. You can finish the guide without paying for any course.
- **Use the [resource library](#resources)** to search every link in the guide by type, level or cost, or to hide what you have already finished.

Every link was checked on 16 October 2026. Links move and pages change, so if one breaks, use the page's title to search for it, and report it on the guide's [GitHub repository](%%REPO_URL%%/issues).

## What you need
- A computer that can run Python 3.11 or later, Git and a code editor such as VS Code.
- A GitHub account for your projects.
- Access to at least one LLM. Many providers offer free tiers or starter credits, and you can run open models locally with Ollama for free. If you pay for API access, set a monthly spending cap in the provider's console; most exercises use small models and cost little.
- About 10 to 12 hours a week. Less is fine; the guide simply takes longer.

## Study tips
- **Keep one learning repository.** Put your practice code, notes and checklists in it from day one. It becomes evidence of your work.
- **Build before you feel ready.** Start each level's project as soon as you have the basics, and let it pull you back into the resources.
- **Write as you go.** A short note per module, in your own words, is the fastest way to find gaps.
- **Measure, don't guess.** From Level 1 onwards, every change you make to a prompt, model or retriever should come with a number that shows whether it helped.
- **Share your work.** Post your projects and what you learned. Employers look for evidence that you can ship, evaluate and explain.
