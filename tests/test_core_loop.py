import tempfile
from pathlib import Path
import unittest
from imperium.sim import World, generate

class CoreLoopTests(unittest.TestCase):
    def setUp(self):
        self.world = World(1, 5, 5, ['plain'] * 25, unit=12)
        self.world.reveal()

    def test_movement_budget_and_reset(self):
        self.world.move(13)
        self.world.move(14)
        with self.assertRaises(ValueError):
            self.world.move(19)
        self.assertEqual(self.world.unit, 14)
        self.world.advance()
        self.world.move(19)
        self.assertEqual(self.world.moves, 1)

    def test_blocked_and_nonadjacent_moves_do_not_change_state(self):
        self.world.tiles[13] = 'water'
        for target in (13, 0, -1, 25):
            with self.assertRaises(ValueError):
                self.world.move(target)
            self.assertEqual((self.world.unit, self.world.moves), (12, 2))

    def test_forest_costs_two(self):
        self.world.tiles[13] = 'forest'
        self.world.move(13)
        self.assertEqual(self.world.moves, 0)

    def test_found_and_twenty_turn_economy(self):
        self.world.found()
        self.assertEqual(self.world.cities, [12])
        self.assertIsNone(self.world.unit)
        with self.assertRaises(ValueError):
            self.world.found()
        for _ in range(20):
            self.world.advance()
        self.assertEqual((self.world.food, self.world.materials), (300, 100))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'world.json'
            self.world.save(path)
            loaded = World.load(path)
            loaded.advance()
            self.assertEqual((loaded.turn, loaded.food), (21, 315))

    def test_exploration_persists_and_survey_hides_unknown(self):
        self.assertNotIn(0, self.world.explored)
        with self.assertRaises(ValueError):
            self.world.survey(0)
        old = set(self.world.explored)
        self.world.move(13)
        self.assertTrue(old <= set(self.world.explored))
        self.assertIn(14, self.world.visible())

    def test_tiny_map_has_a_start(self):
        for seed in range(20):
            world = generate(seed, 1, 1)
            world.found()
            world.advance()
            self.assertGreater(world.food, 0)
