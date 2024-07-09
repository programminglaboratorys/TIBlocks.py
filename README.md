# TIBlocks.py

Library to allow you to read TI-84 Blocks world

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
world.set_block(0, 0, 0, Blocks.GRAVEL) # or 18, Block(18)
print("player current block is", player.current_block.name)
```

convert your it-84 BLOCKS world into a Minecraft world

```bash
$ python -m TIBlocks
#or
$ TIBlocks
```

> [!NOTE]
> you must be in the same folder as the world.

### try it yourself!

```bash
$ cd worlds/World-A
$ python -m TIBlocks
NOTE you must be in the same directory as the .8xv files
world id (A,B,C,D,E): A
done processing TI-84 blocks world
07-09-24 22:24:02 - world folder created
07-09-24 22:24:02 - level.dat created
07-09-24 22:24:02 - region file r.0.0.mca created
07-09-24 22:24:02 - all region files created, world is ready
```

> [!WARNING]
> The library was tested on Minecraft 1.16.5. Opening a world might freeze the game; close and reopen to resolve.

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
