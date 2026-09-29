"""Desktop map viewer. All game state lives in sim."""
from pathlib import Path
import pygame
from .sim import World

COLORS = {'water': '#25465b', 'plain': '#aa9b66', 'forest': '#486e57', 'mountain': '#777780'}


def run(world, frames=None):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption('Imperium Dawn — Twilight Frontier')
    font = pygame.font.Font(None, 25)
    clock = pygame.time.Clock()
    zoom, x, y = 22.0, 20.0, 90.0
    running, count = True, 0
    message = 'Welcome to the twilight frontier'
    save_path = Path('savegame.json')
    try:
        while running:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL:
                    mx, my = pygame.mouse.get_pos()
                    new_zoom = max(6, min(80, zoom * 1.15 ** event.y))
                    x = mx - (mx - x) * new_zoom / zoom
                    y = my - (my - y) * new_zoom / zoom
                    zoom = new_zoom
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        world.advance()
                    elif event.key == pygame.K_F5:
                        try:
                            world.save(save_path)
                            message = 'Saved to savegame.json'
                        except OSError as error:
                            message = f'Save failed: {error}'
                    elif event.key == pygame.K_F9:
                        try:
                            world = World.load(save_path)
                            message = 'Loaded savegame.json'
                        except (OSError, ValueError, TypeError, KeyError) as error:
                            message = f'Load failed: {error}'
            keys = pygame.key.get_pressed()
            x += (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * 450 * dt
            y += (keys[pygame.K_UP] - keys[pygame.K_DOWN]) * 450 * dt
            screen.fill('#131e2a')
            for row in range(world.height):
                for col in range(world.width):
                    rect = pygame.Rect(round(x + col * zoom), round(y + row * zoom), int(zoom) + 1, int(zoom) + 1)
                    if rect.colliderect(screen.get_rect()):
                        pygame.draw.rect(screen, COLORS[world.tiles[row * world.width + col]], rect)
                        if zoom > 15:
                            pygame.draw.rect(screen, '#263337', rect, 1)
            pygame.draw.rect(screen, '#131e2a', (0, 0, screen.get_width(), 82))
            lines = [f'IMPERIUM DAWN   |   Seed {world.seed}   |   Turn {world.turn}',
                     'Arrows: pan   Wheel: zoom   Space: advance   F5: save   F9: load   Esc: exit', message]
            for i, line in enumerate(lines):
                screen.blit(font.render(line, True, '#e8debf'), (18, 9 + i * 24))
            pygame.display.flip()
            count += 1
            if frames is not None and count >= frames:
                running = False
    finally:
        pygame.quit()
    return world
