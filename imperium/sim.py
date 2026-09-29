"""Deterministic simulation with no rendering dependencies."""
from dataclasses import dataclass, field
import json
from pathlib import Path
from .terrain import generate_tiles

TERRAINS = ('water', 'plain', 'forest', 'mountain')
YIELDS = {'plain': (3, 1), 'forest': (1, 3), 'mountain': (0, 2), 'water': (1, 0)}

@dataclass
class World:
    seed: int
    width: int
    height: int
    tiles: list[str]
    turn: int = 0
    unit: int | None = None
    moves: int = 2
    cities: list[int] = field(default_factory=list)
    food: int = 0
    materials: int = 0
    explored: list[int] = field(default_factory=list)

    def neighbors(self, tile, radius=1):
        x, y = tile % self.width, tile // self.width
        return [row * self.width + col
                for row in range(max(0, y-radius), min(self.height, y+radius+1))
                for col in range(max(0, x-radius), min(self.width, x+radius+1))
                if abs(col-x) + abs(row-y) <= radius]

    def visible(self):
        sources = self.cities + ([] if self.unit is None else [self.unit])
        return set(tile for source in sources for tile in self.neighbors(source, 2))

    def reveal(self):
        self.explored = sorted(set(self.explored) | self.visible())

    def move(self, target):
        if self.unit is None:
            raise ValueError('Your pioneer has founded a settlement')
        if target not in self.neighbors(self.unit) or target == self.unit:
            raise ValueError('Move one tile horizontally or vertically')
        cost = 2 if self.tiles[target] == 'forest' else 1
        if self.tiles[target] in ('water', 'mountain'):
            raise ValueError('Water and mountains are impassable')
        if cost > self.moves:
            raise ValueError('Not enough movement; end the turn')
        self.unit = target
        self.moves -= cost
        self.reveal()

    def survey(self, tile):
        if tile not in self.explored:
            raise ValueError('Explore this tile first')
        # Only known terrain contributes to the forecast.
        known = set(self.explored)
        area = [n for n in self.neighbors(tile) if n in known]
        return tuple(sum(YIELDS[self.tiles[n]][i] for n in area) for i in (0, 1))

    def found(self):
        if self.unit is None:
            raise ValueError('No pioneer available')
        self.cities.append(self.unit)
        self.unit = None
        self.reveal()

    def advance(self):
        for city in self.cities:
            food, materials = self.survey(city)
            self.food += food
            self.materials += materials
        self.turn += 1
        self.moves = 2

    def save(self, path):
        self.validate()
        target = Path(path)
        temporary = target.with_suffix(target.suffix + '.tmp')
        temporary.write_text(json.dumps({'version': 2, **vars(self)}, indent=2))
        temporary.replace(target)

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text())
        if not isinstance(data, dict):
            raise ValueError('Save must contain a world object')
        version = data.pop('version', None)
        if version not in (1, 2):
            raise ValueError('Unsupported save version')
        try:
            world = cls(**data)
            world.validate()
            if version == 1:
                world.start()
            return world
        except (TypeError, KeyError) as error:
            raise ValueError('Malformed save data') from error

    def start(self):
        self.unit = next((i for i, terrain in enumerate(self.tiles) if terrain == 'plain'), None)
        if self.unit is None:
            self.unit = 0
            self.tiles[0] = 'plain'
        self.reveal()

    def validate(self):
        integers = (self.seed, self.width, self.height, self.turn, self.moves, self.food, self.materials)
        if any(type(value) is not int for value in integers):
            raise ValueError('World counters must be integers')
        if not 1 <= self.width <= 256 or not 1 <= self.height <= 256 or min(self.turn, self.food, self.materials) < 0 or not 0 <= self.moves <= 2:
            raise ValueError('Invalid dimensions or counters')
        if not isinstance(self.tiles, list) or len(self.tiles) != self.width * self.height or any(t not in TERRAINS for t in self.tiles):
            raise ValueError('Invalid terrain data')
        def valid_tile(tile):
            return type(tile) is int and 0 <= tile < len(self.tiles)
        for collection in (self.cities, self.explored):
            if not isinstance(collection, list) or any(not valid_tile(t) for t in collection) or len(set(collection)) != len(collection):
                raise ValueError('Invalid tile positions')
        if self.unit is not None and (not valid_tile(self.unit) or self.tiles[self.unit] not in ('plain', 'forest')):
            raise ValueError('Invalid pioneer position')
        if any(self.tiles[city] not in ('plain', 'forest') for city in self.cities):
            raise ValueError('Invalid settlement terrain')


def generate(seed=42, width=64, height=40):
    if type(width) is not int or type(height) is not int or not 1 <= width <= 256 or not 1 <= height <= 256:
        raise ValueError('Map dimensions must be integers between 1 and 256')
    world = World(seed, width, height, generate_tiles(seed, width, height))
    world.start()
    world.validate()
    return world
