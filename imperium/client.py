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
    zoom, x, y = 22.0, 20.0, 130.0
    running, count = True, 0
    message = 'Click a neighboring tile to move; B founds your first settlement'
    selected = world.unit if world.unit is not None else 0
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] >= 106:
                    col = int((event.pos[0] - x) // zoom)
                    row = int((event.pos[1] - y) // zoom)
                    if 0 <= col < world.width and 0 <= row < world.height:
                        selected = row * world.width + col
                        try:
                            world.move(selected)
                            message = 'Pioneer moved'
                        except ValueError as error:
                            message = str(error)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        world.advance()
                    elif event.key == pygame.K_b:
                        try:
                            world.found()
                            message = 'Settlement founded! End turns to collect resources.'
                        except ValueError as error:
                            message = str(error)
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
            visible, explored = world.visible(), set(world.explored)
            for row in range(world.height):
                for col in range(world.width):
                    rect = pygame.Rect(round(x + col * zoom), round(y + row * zoom), int(zoom) + 1, int(zoom) + 1)
                    if rect.colliderect(screen.get_rect()):
                        tile = row * world.width + col
                        color = COLORS[world.tiles[tile]] if tile in explored else '#1c2934'
                        pygame.draw.rect(screen, color, rect)
                        if tile in explored and tile not in visible:
                            shade = pygame.Surface(rect.size, pygame.SRCALPHA)
                            shade.fill((0, 0, 0, 125))
                            screen.blit(shade, rect)
                        if tile == world.unit:
                            pygame.draw.circle(screen, '#ffe6a0', rect.center, max(2, int(zoom / 3)))
                        if tile in world.cities:
                            pygame.draw.rect(screen, '#f2c875', rect.inflate(-int(zoom/3), -int(zoom/3)))
                        if tile == selected:
                            pygame.draw.rect(screen, '#ffffff', rect, 2)
                        if zoom > 15:
                            pygame.draw.rect(screen, '#263337', rect, 1)
            pygame.draw.rect(screen, '#131e2a', (0, 0, screen.get_width(), 106))
            lines = [f'IMPERIUM DAWN | Turn {world.turn} | Movement {world.moves}/2 | Food {world.food} | Materials {world.materials}',
                     'Click: move/survey   B: found   Space: end turn   Arrows: pan   Wheel: zoom   F5/F9: save/load', message]
            if selected in explored:
                food, materials = world.survey(selected)
                lines.append(f'Survey: {world.tiles[selected]} | Known local yield: {food} food, {materials} materials / turn')
            for i, line in enumerate(lines):
                screen.blit(font.render(line, True, '#e8debf'), (18, 9 + i * 24))
            pygame.display.flip()
            count += 1
            if frames is not None and count >= frames:
                running = False
    finally:
        pygame.quit()
    return world
