import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from imperium.debug import execute
from imperium.sim import World, generate
from imperium.storage import save_path

class ToolTests(unittest.TestCase):
    def test_terrain_forms_regions(self):
        world = generate(42)
        pairs = [(i, i+1) for i in range(len(world.tiles)-1) if (i+1) % world.width]
        same = sum(world.tiles[a] == world.tiles[b] for a, b in pairs)
        self.assertGreater(same / len(pairs), .7)
        self.assertGreaterEqual(len(set(world.tiles)), 3)

    def test_legacy_save_migration(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'legacy.json'
            path.write_text(json.dumps(dict(version=1, seed=1, width=2, height=2, tiles=['plain']*4, turn=8)))
            world = World.load(path)
            self.assertEqual((world.turn, world.unit), (8, 0))
            self.assertTrue(world.explored)

    def test_debug_commands_and_rejection(self):
        world = generate(1)
        execute(world, 'grant food 20')
        execute(world, 'turn 3')
        self.assertEqual((world.food, world.turn), (20, 3))
        for command in ('grant food -1', 'turn 1001', '__import__("os")', 'grant gold 10'):
            with self.assertRaises(ValueError):
                execute(world, command)
        execute(world, 'reveal')
        self.assertEqual(len(world.explored), len(world.tiles))

    def test_save_location_uses_user_data(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'XDG_DATA_HOME': folder}):
            target = save_path()
            self.assertEqual(target, Path(folder) / 'imperium-dawn' / 'savegame.json')
            generate().save(target)
            self.assertTrue(target.exists())
