# Decisions (append only)

## 2026-09-28 — Stack and scope
Choose Python 3.11+ and pygame-ce. Python keeps the simulation easy to test and run in bulk; pygame provides a small desktop rendering layer. Godot offers stronger authoring tools but would add engine-specific tooling to headless experiments. A browser client would add packaging and integration work before the core loop exists.

The simulation uses only the standard library and never imports pygame. The client sends commands to simulation state. JSON saves carry a schema version and reject unsupported versions. Use a square grid initially for simple movement and rendering. Seeded generation uses a local random generator.

## 2026-09-28 — Feedback triage
Accept the user's request to begin development after authentication. First ship the Phase 0 documents, then M1. GitHub push dry run succeeded.

## 2026-09-28 — Direct main workflow and M2 rules
User requested direct commits to main. Run tests before each commit/push; no future feature branches or PRs. M2 starts with one pioneer, two movement points per turn, forests costing two, and impassable water/mountains. Founding consumes the pioneer. Settlements collect yields from their tile and four adjacent tiles. Population, queues, recruitment and spending belong to M3. Save version 2 persists game state and migrates version 1 maps by adding a pioneer.

## 2026-09-28 — Linux distribution readiness
Plan standalone Linux distribution for M9. Keep Python and the standard-library simulation boundary. Store desktop saves in XDG user data, independent of working directory or a read-only installation. Select the bundler after desktop dependencies stabilize; acceptance requires launch without a system Python installation and persistent user saves. Terrain uses seeded interpolated elevation/moisture fields; this is geographic coherence, not a climate simulation.
