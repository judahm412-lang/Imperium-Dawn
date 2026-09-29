import argparse
from .sim import World, generate


def main():
    parser = argparse.ArgumentParser(description='Imperium Dawn')
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--turns', type=int, default=0)
    parser.add_argument('--load')
    parser.add_argument('--save')
    parser.add_argument('--frames', type=int, help='Exit desktop after N frames (smoke tests)')
    args = parser.parse_args()
    if args.turns < 0 or (args.frames is not None and args.frames < 1):
        parser.error('turns must be nonnegative and frames positive')
    world = World.load(args.load) if args.load else generate(args.seed)
    for _ in range(args.turns):
        world.advance()
    if not args.headless:
        from .client import run
        world = run(world, args.frames)
    if args.save:
        world.save(args.save)
    print(f'Seed {world.seed} | {world.width}x{world.height} | Turn {world.turn}')

if __name__ == '__main__':
    main()
