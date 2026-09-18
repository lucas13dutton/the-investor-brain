# How the agents work

**Version 0.1 (draft)** · Owner: Lucas

## The three layers

| Layer | What it is | Where it lives | Runs when |
|---|---|---|---|
| Agents | Specialists with their own instructions, tools and context | `.claude/agents/*.md` | Called by Lucas or another agent in Claude Code |
| Scripts | Repeatable code the agents write (pipelines, scoring, calculations) | `data/`, `signal-room/`, `costs/` | On demand or on a schedule |
| Schedules | Automation that runs scripts unattended | GitHub Actions | Cron, e.g. Monday 06:00 data sweep, daily Signal Room snapshot |

Rule of thumb: if it needs judgement, it's an agent. If it's identical every time, it's a script an agent wrote.

## The five agents

| Agent | Job | Hands work to |
|---|---|---|
| researcher | Builds and updates asset dossiers | skeptic |
| skeptic | Attacks the work before the internet does | researcher or writer, then Lucas |
| writer | Turns findings into scripts, captions and the newsletter | compliance |
| compliance | Runs the house-rules checklist on everything outward-facing | Lucas |
| scout | Runs the Signal Room and writes the weekly brief | writer |

## How they communicate

Through files in this repo, never directly. The researcher writes `dossiers/gold.md`; the skeptic writes `reviews/gold-review-2026-10-01.md` beside it; the writer reads both. Every handoff is visible, and git keeps the history.

## The flow for one video

1. `scout` delivers the weekly Signal Brief.
2. Lucas picks a topic.
3. `researcher` fills any gaps in the dossier.
4. `skeptic` reviews it. Fixes happen until the verdict is Pass.
5. `writer` drafts the script.
6. `compliance` runs the checklist.
7. Lucas approves, records, and the edit is produced.
8. Nothing publishes without Lucas.

## What agents may never do

- Publish, post or send anything.
- Spend money, or sign up to paid data or tools.
- Change `docs/methodology.md` or `docs/house-rules.md`.
- Edit the evidence log to make a claim fit.
- Approve their own work: the author never reviews their own output.

## Adding an agent

Add one only when a job has been done by hand enough times to know its rules. Later additions, in likely order: producer (video assembly), data-engineer (pipelines), quant (Strategy Lab), analyst (performance review), builder (website and app), chronicler (build-in-public log).
