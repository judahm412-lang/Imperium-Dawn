# Roadmap

## Next five tasks
1. Complete visible M1 desktop verification and hosted CI; headless and dummy-driver checks passed.
2. Add turn commands and unit movement (M2).
3. Add settlements and resource production (M2).
4. Add fog of war and selection panels (M2).
5. Ship a distinctive terrain survey tool (M2 original idea).

| Milestone | Status | Deliverables and acceptance |
| --- | --- | --- |
| M1 Walking skeleton | in progress | Window, square map, pan/zoom, seeded generation, versioned save/load, headless runner, CI. Determinism and round-trip tests pass; desktop smoke check succeeds. |
| M2 Core loop | planned | Turns, movement, fog, settlements, production, panels. A player can establish a settlement and play 20 turns. |
| M3 Economy | planned | Resources, buildings, population, queues. Costs and outputs tested; economy survives 100 turns. Scope review. |
| M4 Progression | planned | 40+ data-driven technologies. Unlocks alter gameplay and dependency validation passes. |
| M5 Combat | planned | Unit roles, terrain modifiers, previews and logs. Resolution matches previews and tests. |
| M6 AI | planned | Three distinct opponents. Complete headless games and reproducible decisions. Scope review. |
| M7 Diplomacy | planned | Relations, treaties, trade, war, reputation. AI reacts and agreements enforce effects. |
| M8 Victory | planned | Three victories, setup, difficulty. Full matches reach documented end conditions. |
| M9 Polish | planned | Audio hooks, animation, help, settings, keybinds. Profile against 60 FPS at 1280x720 on recorded hardware. Scope review. |
| M10 Balance | planned | 100+ AI matches and findings in docs/balance. Tune dominant strategies using measured outcomes. |
| M11+ Expansion | planned | Choose events, wonders, espionage, culture, history, mods or editor from feedback and ideas. Define acceptance before implementation. |

Every milestone requires green tests, updated docs, a release tag, a demo, and a retrospective. Releases remain pending until acceptance is verified.
