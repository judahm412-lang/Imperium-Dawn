"""Seeded, interpolated fields form connected terrain regions."""
import random


def field(rng, width, height, scale=7):
    cols, rows = width // scale + 2, height // scale + 2
    anchors = [[rng.random() for _ in range(cols)] for _ in range(rows)]
    values = []
    for y in range(height):
        for x in range(width):
            ax, ay = x // scale, y // scale
            tx, ty = (x % scale) / scale, (y % scale) / scale
            tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
            top = anchors[ay][ax] * (1-tx) + anchors[ay][ax+1] * tx
            bottom = anchors[ay+1][ax] * (1-tx) + anchors[ay+1][ax+1] * tx
            values.append(top * (1-ty) + bottom * ty)
    return values


def generate_tiles(seed, width, height):
    rng = random.Random(seed)
    elevation = field(rng, width, height)
    moisture = field(rng, width, height, 5)
    tiles = []
    for i, height_value in enumerate(elevation):
        # The vertical axis runs from the frozen rim to the sunward desert.
        latitude = (i // width) / max(1, height - 1)
        if height_value < 0.28:
            terrain = 'water'
        elif height_value > 0.76:
            terrain = 'mountain'
        elif moisture[i] > 0.48 and 0.15 < latitude < 0.85:
            terrain = 'forest'
        else:
            terrain = 'plain'
        tiles.append(terrain)
    return tiles
