"""Reproducible desktop input check and screenshot. Run from repository root."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
from pathlib import Path
import tempfile
from unittest.mock import patch
import pygame
from imperium.client import run
from imperium.sim import World


def key(code, unicode=''):
    return pygame.event.Event(pygame.KEYDOWN, key=code, unicode=unicode)


def main():
    world = World(42, 24, 16, ['plain'] * (24 * 16), unit=25)
    for row in range(16):
        for col in range(24):
            if col > 15:
                world.tiles[row*24+col] = 'water'
            elif row > 6:
                world.tiles[row*24+col] = 'forest'
    world.reveal()
    first = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(75, 163)), key(pygame.K_b)]
    first += [key(pygame.K_SPACE)] * 20 + [key(pygame.K_F5), key(pygame.K_SPACE), key(pygame.K_F9)]
    second = [key(pygame.K_BACKQUOTE)] + [key(ord(c), c) for c in 'reveal'] + [key(pygame.K_RETURN), key(pygame.K_BACKQUOTE), key(pygame.K_F3)]
    output = Path('docs/demos/core-loop.png')
    output.parent.mkdir(parents=True, exist_ok=True)
    original_flip = pygame.display.flip
    def capture():
        original_flip()
        pygame.image.save(pygame.display.get_surface(), output)
    with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'XDG_DATA_HOME': folder}), patch('pygame.event.get', side_effect=[first, second, []]), patch('pygame.display.flip', side_effect=capture):
        result = run(world, frames=3)
    assert result.cities == [26] and result.unit is None
    assert (result.turn, result.food, result.materials) == (20, 300, 100)
    assert len(result.explored) == len(result.tiles)
    print(f'Desktop movement, founding, 20 turns, save/load and console passed. Screenshot: {output}')

if __name__ == '__main__':
    main()
