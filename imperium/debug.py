"""Explicit debug commands; never evaluate Python from user input."""

def execute(world, command):
    parts = command.split()
    if not parts:
        return 'Commands: help, state, reveal, grant food|materials N, turn N'
    if parts == ['help']:
        return 'state | reveal | grant food|materials N | turn N (cheats alter saves)'
    if parts == ['state']:
        return f'Turn={world.turn} pioneer={world.unit} settlements={world.cities} explored={len(world.explored)}'
    if parts == ['reveal']:
        world.explored = list(range(len(world.tiles)))
        return 'Entire map explored'
    if len(parts) == 3 and parts[0] == 'grant' and parts[1] in ('food', 'materials'):
        amount = int(parts[2])
        if not 0 <= amount <= 100000:
            raise ValueError('Grant must be between 0 and 100000')
        setattr(world, parts[1], getattr(world, parts[1]) + amount)
        return f'Granted {amount} {parts[1]}'
    if len(parts) == 2 and parts[0] == 'turn':
        count = int(parts[1])
        if not 0 <= count <= 1000:
            raise ValueError('Turn count must be between 0 and 1000')
        for _ in range(count):
            world.advance()
        return f'Advanced {count} turns'
    raise ValueError('Unknown command; type help')
