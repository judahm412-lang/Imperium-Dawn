# Journal

## 2026-09-28 — Phase 0
Verified GitHub authentication with a successful push dry run. Created the setting, stack decision, roadmap, architecture, and feedback/backlog files before game code. No game exists yet. Next: implement and verify M1 on feat/walking-skeleton. Fresh engineers should read ROADMAP.md and run the README commands once implemented.

## 2026-09-28 — M1 implementation
Implemented a square terrain viewer with arrow pan, cursor-centered wheel zoom, turn counter, F5/F9 persistence, and headless CLI. All five unit/integration tests pass. A five-frame SDL dummy-driver desktop smoke test passes. Headless saves at turn 100 reload and advance to 110. pygame-ce 2.5.7 installed in .venv; tested locally on Python 3.13.5. CI targets Python 3.11.

Limitations: terrain is independent random tiles, not coherent climate geography; turns only increment a counter. Visible desktop interaction and hosted CI still need verification, so M1 release/tag remains pending. Next: verify visible controls and CI, then M2 movement and settlements.

## 2026-09-28 — Main workflow and M2 core loop
M1 hosted CI passed; fast-forwarded and pushed main. User requested future work directly on main and AGENTS.md was updated. Added pioneer movement, terrain costs, exploration/visibility, settlement founding, resource production, and a survey forecast. Eleven tests pass including twenty turns of settlement production and persistence. Dummy-driver desktop smoke passes. M1 visible interaction verification remains pending; no release tags yet. M2 is in progress: one founding pioneer, no recruitment or resource spending yet. Next: verify desktop controls, add debug inspection and coherent terrain, then complete milestone acceptance and releases before M3.

## 2026-09-28 — Terrain, debug tools and packaging readiness
Accepted the future Linux standalone packaging requirement. Added connected terrain regions, an F3 state/camera overlay, bounded explicit cheat commands, and XDG user-data saves. Fifteen tests pass. Desktop demo verifies actual client event handling for movement, founding, twenty turns, F5/F9 and console reveal. Rendered and inspected docs/demos/core-loop.png; header, map, survey and debug panel are readable. Demo uses temporary storage. Legacy map saves migrate to schema 2; old cwd saves can be opened via --load. No Linux bundle yet. Next: hosted CI, milestone acceptance/release tags, then M3 queues and spending.
