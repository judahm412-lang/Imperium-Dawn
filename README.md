# Imperium Dawn

A desktop 4X game set on a twilight frontier. Current build is the M1 map viewer; empires, units, and economy are upcoming.

## Run

Python 3.11+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m imperium
```

Arrow keys pan; mouse wheel zooms around the cursor. Space advances the turn counter. F5 saves to `savegame.json`; F9 reloads it. Escape exits.

## Test and simulate

The simulation and tests require no pygame installation:

```sh
python3 -m unittest discover -s tests -v
python3 -m imperium --headless --seed 42 --turns 100 --save /tmp/imperium-save.json
python3 -m imperium --headless --load /tmp/imperium-save.json --turns 10
```

Desktop smoke check:

```sh
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python -m imperium --frames 5
```

For a visible demo, launch the client, pan and zoom, advance five turns, save, advance again, then reload and verify turn five returns. Profile simulation with `python3 -m cProfile -s cumulative -m imperium --headless --turns 100000`.

## M2 core loop

The gold circle is your pioneer. Click an adjacent plain or forest tile to move. Plains cost one movement point, forests two; water and mountains block movement. Space ends the turn and restores two movement points. Dark terrain is unexplored; dim terrain has been explored but is outside current vision.

Press B to found your settlement, consuming the pioneer. Each turn collects food and materials from the settlement and its four neighboring tiles. Click explored tiles to see their known local yield forecast. Resources accumulate; buildings and spending are planned for M3. F5/F9 preserve movement, exploration, settlements, and resources. Version 1 saves migrate automatically.

Demo: move the pioneer, press Space, choose a site using the survey, press B, then play twenty turns. Save, advance, reload, and verify the resources and turn return.
