# MISSION: Build an open-ended 4X grand strategy game, and keep growing it

You are the sole engineer, designer, and project manager of a desktop 4X
strategy game (explore, expand, exploit, exterminate/diplomacy). This is a
long-running project. I will keep watching, giving feedback, and asking you to
continue. Your job is to make steady, well-planned, well-tested progress and
never let the project rot.

## 0. Ground rules
- Work in a git repo and push to GitHub regularly (origin will be set up by
  me; if push fails, tell me exactly what you need, then keep committing locally).
- Small commits, clear messages (conventional commits: feat:, fix:, refactor:,
  test:, docs:). Work on feature branches and open PRs into `main` for
  anything bigger than a trivial change. Write real PR descriptions.
- Never leave `main` broken. Tests must pass before merging.
- Prefer boring, readable code. Refactor when a system gets painful, and log why.
- Ask me questions only when truly blocked. Otherwise make a decision, write it
  down in DECISIONS.md, and continue.

## 1. Phase 0: Plan before you code (do this first)
Create these files and commit them before writing game code:
1. `VISION.md`: pick a theme and setting (I have no preference, so surprise me),
   the core fantasy, what makes the game distinct, and 3 design pillars.
2. `DECISIONS.md`: append-only log. Record the stack choice (Python + pygame,
   Godot, or other), with alternatives considered and why you chose it.
   Constraint: the simulation core MUST be separable from rendering and runnable
   headless, so it can be tested and simulated in bulk without a window.
3. `ROADMAP.md`: milestones M1..M10+ with goals, deliverables, and acceptance
   criteria. Mark status: planned / in progress / done / cut.
4. `JOURNAL.md`: a dated worklog. At the end of every work session write:
   what you did, what's broken, what's next, and anything a fresh
   engineer would need to resume without context.
5. `IDEAS.md`: backlog of your own feature ideas (see section 5).
6. `FEEDBACK.md`: an inbox where I drop notes (see section 4).
7. `ARCHITECTURE.md`: modules, data flow, and how to run, test, and profile.

## 2. Milestone plan (adapt it, but keep the ordering logic)
- M1 Walking skeleton: window opens, hex or square map renders, camera
  pan/zoom, deterministic seeded map generation, save/load, headless sim
  runner, CI running tests.
- M2 Core loop: turns, units, movement, fog of war, cities/settlements,
  resource production, basic UI panels.
- M3 Economy and growth: multiple resources, buildings, population,
  a production queue, an economy that is meaningfully balanced.
- M4 Tech/progression tree: data-driven (JSON/YAML), 40+ nodes, unlock
  effects that actually change gameplay.
- M5 Combat: unit types, terrain effects, readable combat resolution, a
  combat log and previews.
- M6 AI opponents: at least 3 AI empires with distinct personalities that
  expand, build, research, and fight. Must be able to play full games headless.
- M7 Diplomacy: relations, treaties, trade, war declarations, AI
  reactions, and reputation.
- M8 Victory conditions and game flow: at least 3 ways to win, endgame
  detection, a new-game setup screen, and difficulty levels.
- M9 Polish: audio hooks, animations, tooltips, tutorial or help,
  settings, keybinds, and performance profiling with a target frame time.
- M10 Balance and depth: run automated AI-vs-AI batch simulations (100+
  games), analyze the results, and tune. Write the findings up in `docs/balance/`.
- M11+ Open-ended: events, wonders, espionage, religion or culture,
  procedural history, mods support, scenario editor. Choose based on
  IDEAS.md and my feedback.

## 3. Staying on track over a long run
- At the start of every session: read ROADMAP.md, JOURNAL.md, FEEDBACK.md,
  and `git log -20`. State your plan for the session in 3-5 bullets.
- Keep a rolling "next 5 tasks" list at the top of ROADMAP.md.
- Every milestone ends with: acceptance criteria checked, tests green, docs
  updated, a tagged release (`v0.N.0`), a short demo script or GIF/screenshots,
  and a retrospective in JOURNAL.md (what went well, what to improve).
- Every 3 milestones, do a scope review: cut or re-plan anything that has
  drifted. It's fine to change the plan, but log why.
- If you notice tech debt, file it in `DEBT.md` with severity, and pay it
  down on a schedule, not just when convenient.

## 4. Testing, bugfixing, and feedback
- Unit tests for the sim core, property or determinism tests (same seed =
  same game), and a headless smoke test that plays N turns in CI.
- When a bug is found: write a failing test first, then fix, then commit the
  test with the fix. Record notable bugs in `BUGS.md` with root cause.
- Add a debug/cheat console and an in-game overlay for inspecting state.
- FEEDBACK.md protocol: I write notes there or in chat. Before doing
  anything else, triage them: acknowledge each one, mark it accepted /
  deferred / declined (with reasons), and schedule accepted ones in the
  roadmap. If my feedback conflicts with earlier design decisions, say so
  plainly, propose a resolution, and update DECISIONS.md.

## 5. Your own ideas (this is being evaluated)
- Maintain IDEAS.md. After each milestone, add at least 3 new ideas that
  are NOT in my instructions, each with: the pitch, the player-facing
  payoff, the cost estimate, and risks.
- Every second milestone, ship at least one of your own ideas that I
  didn't ask for. Explain why you chose it.
- Be ambitious but honest: mark ideas as low, medium, or high risk.

## 6. Communication
- Report at natural checkpoints: what shipped, how to run it, what to look
  at, what you're unsure about, and what you recommend next.
- Be candid about failures, flaky tests, and shortcuts. Don't claim
  something works unless you ran it.
- Never stop at "done." When a milestone finishes, propose the next
  one, and keep going until I tell you to pause.

## 7. Definition of a good day
A player can launch the game, start a new match, play real turns against AI
empires, save, quit, and reload, and every piece of that is tested,
documented, committed, and pushed.

Begin with Phase 0. Show me VISION.md and ROADMAP.md when they're ready,
then proceed into M1 without waiting unless you have a real question.
