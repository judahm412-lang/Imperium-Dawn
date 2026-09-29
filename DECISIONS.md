# Decisions (append only)

## 2026-09-28 — Stack and scope
Choose Python 3.11+ and pygame-ce. Python keeps the simulation easy to test and run in bulk; pygame provides a small desktop rendering layer. Godot offers stronger authoring tools but would add engine-specific tooling to headless experiments. A browser client would add packaging and integration work before the core loop exists.

The simulation uses only the standard library and never imports pygame. The client sends commands to simulation state. JSON saves carry a schema version and reject unsupported versions. Use a square grid initially for simple movement and rendering. Seeded generation uses a local random generator.

## 2026-09-28 — Feedback triage
Accept the user's request to begin development after authentication. First ship the Phase 0 documents, then M1. GitHub push dry run succeeded.
