from pymcworld.world import World
from TIBlocks import load
from TIBlocks.blocks import Blocks
from pymcworld.option import Option
from pymcworld.nbt import *

def main(world_id="A"):
    print("NOTE you must be in the same directory as the .8xv files")
    player, ITworld = load(world_id)
    
    #print(world.blocks.__dict__)
    world = World()
    
    
    blocks_map = {
        "GRASS":world.blocks.GRASS_BLOCK, 
        "WOOD": world.blocks.OAK_WOOD,
        "LEAVES": world.blocks.OAK_LEAVES,
        "PLANKS": world.blocks.OAK_PLANKS,
        "SLABS": world.blocks.OAK_SLAB,
        "BOOKS": world.blocks.BOOKSHELF,
        "GOLD": world.blocks.GOLD_BLOCK,
        "IRON": world.blocks.IRON_BLOCK,
        "COBBLE": world.blocks.COBBLESTONE,
        "CRAFTING": world.blocks.CRAFTING_TABLE
    }
    for y,layer in enumerate(ITworld.blocks):
        for x,slice in enumerate(layer):
            for z,block in enumerate(slice):
                if block.id == 0: # do not remove, air breaks/bugs regions
                    continue
                try:
                    id = block.id
                    block_name = Blocks(id).name.upper()
                    block_object = world.blocks.__dict__.get(block_name) or blocks_map.get(block_name)
                    block_object.properties = {"facing": "west"}
                    try:
                        assert block_object is not None, "block should not be None!"
                    except AssertionError:
                        print('block:',block_name, block_object)
                        raise
                    world.set_block(x, y, z, block_object)
                except ValueError:
                    print("block: not found", "Block:", block_name, "X:", x, "Y:", y, "Z:", z)
    print("done")
    
    
    class CUSTOM_OPTION(Option):
        def __init__(self, name, id, tag):
            self.name = name
            self.id = id
            self.tag = tag
        def create_tag(self):
            return self.tag
    
    Player_TAG_COMPOUND = TAG_Compound(name = "Player")
    
    Inventory_TAG_LIST = TAG_List(type=TAG_Compound, name = "Inventory")
    def get_block_id(id):
        block_name = Blocks(id).name.upper()
        return "minecraft:"+((world.blocks.__dict__.get(block_name) or blocks_map.get(block_name)).name)
    
    item = TAG_Compound()
    item.tags.extend([Option("Count", TAG_Byte, 1).create_tag(), Option("id", TAG_String, get_block_id(player.current_block.id)).create_tag(), Option("Slot", TAG_Byte, 0).create_tag()])
    Inventory_TAG_LIST.tags.append(item)
    Player_TAG_COMPOUND.tags.append(Inventory_TAG_LIST)
    
    world.options["SpawnX"] = Option("SpawnX", TAG_Int, player.x)
    world.options["SpawnY"] = Option("SpawnY", TAG_Int, player.y)
    world.options["SpawnZ"] = Option("SpawnZ", TAG_Int, player.z)
    
    
    world.options["Player"] = CUSTOM_OPTION("Player", TAG_COMPOUND, Player_TAG_COMPOUND)
    world.options["GameType"] = Option("GameType", TAG_Byte, 3)
    world.options["Difficulty"] = Option("Difficulty", TAG_Byte, 0)
    
    
    world.save("Village World 4")

if __name__ == "__main__":
    main(input("world id (A,B,C,D,E): "))