# TIBlocks.py

Library to allow you to read TI-84 Blocks world
python setup.py install

## Install it

clone and install it with:

```cmd
pip install TIBlocks.py/
```

## Usage

```py
from TIBlocks import load, Blocks
# A,B,C,D,E
player, world = load(world_id)
# blocks[y][x][z]
# blocks[16][48][48]
print(world.blocks)
world.set_block(0, 0, 0, Blocks.GRAVEL) # or 18,
print("player current block is", player.current_block.name)
```

convert your it-84 BLOCKS world into minecraft java edition world

```bash
$ python -m TIBlocks
#or
$ TIBlocks
```

> [!NOTE]
> you must be in the same folder as the world

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
