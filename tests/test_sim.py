import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from imperium.sim import World, generate

class SimulationTests(unittest.TestCase):
    def test_determinism(self):
        for seed in range(20):
            self.assertEqual(generate(seed), generate(seed))
        self.assertNotEqual(generate(1).tiles, generate(2).tiles)

    def test_save_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'save.json'
            world = generate(-4, 12, 8)
            for _ in range(25):
                world.advance()
            world.save(path)
            self.assertEqual(world, World.load(path))

    def test_invalid_dimensions(self):
        for dimensions in ((0, 4), (257, 4), (4, -1), (1.5, 4)):
            with self.assertRaises(ValueError):
                generate(42, *dimensions)

    def test_invalid_save(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'bad.json'
            for data in ({'version': 2}, {'version': 1, 'seed': 1, 'width': 2, 'height': 2, 'tiles': ['plain'], 'turn': 0}):
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    World.load(path)

    def test_headless_cli(self):
        result = subprocess.run([sys.executable, '-m', 'imperium', '--headless', '--turns', '100'], capture_output=True, text=True, check=True)
        self.assertIn('Turn 100', result.stdout)

if __name__ == '__main__':
    unittest.main()
