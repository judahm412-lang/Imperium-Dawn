"""Deterministic simulation with no rendering dependencies."""
from dataclasses import dataclass
import json
from pathlib import Path
import random

TERRAINS = ('water', 'plain', 'forest', 'mountain')

@dataclass
class World:
    seed: int
    width: int
    height: int
    tiles: list[str]
    turn: int = 0

    def advance(self):
        self.turn += 1

    def save(self, path):
        target = Path(path)
        temporary = target.with_suffix(target.suffix + '.tmp')
        temporary.write_text(json.dumps({'version': 1, **vars(self)}, indent=2))
        temporary.replace(target)

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text())
        if data.pop('version', None) != 1:
            raise ValueError('Unsupported save version')
        world = cls(**data)
        world.validate()
        return world

    def validate(self):
        if any(type(value) is not int for value in (self.seed, self.width, self.height, self.turn)):
            raise ValueError('World dimensions, seed and turn must be integers')
        if not 1 <= self.width <= 256 or not 1 <= self.height <= 256 or self.turn < 0:
            raise ValueError('Invalid dimensions or turn')
        if len(self.tiles) != self.width * self.height or any(t not in TERRAINS for t in self.tiles):
            raise ValueError('Invalid terrain data')


def generate(seed=42, width=64, height=40):
    world = World(seed, width, height, [])
    if type(width) is not int or type(height) is not int or not 1 <= width <= 256 or not 1 <= height <= 256:
        raise ValueError('Map dimensions must be integers between 1 and 256')
    rng = random.Random(seed)
    world.tiles = rng.choices(TERRAINS, weights=(18, 48, 25, 9), k=width * height)
    world.validate()
    return world
