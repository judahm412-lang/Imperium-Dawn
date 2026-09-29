# Architecture

`imperium/sim.py`: standard-library state, seeded map generation, turn progression, versioned JSON persistence.
`imperium/client.py`: pygame window, camera, map rendering, keyboard input.
`imperium/__main__.py`: CLI selecting desktop or headless execution.
`tests/`: simulation determinism, persistence, validation, headless smoke checks.

Data flow: CLI creates/loads state → client or headless runner advances state → persistence writes JSON. Rendering reads state and never owns simulation rules.

Run, test, and profile commands live in README.md. M1 turns count time only; units and resource rules start in M2.

M2 adds movement/founding commands, Manhattan-radius visibility, persistent exploration, and settlement yields to World. The client draws state and forwards input; save schema 2 retains all state and loads schema 1 maps.

`terrain.py` builds local seeded elevation/moisture fields. `storage.py` resolves XDG user saves. `debug.py` dispatches explicit bounded commands without code evaluation. `tools/desktop_demo.py` exercises client input and renders a reproducible screenshot.
