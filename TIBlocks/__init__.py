from ctypes import Structure, c_int8, c_uint8
from io import BytesIO
import ctypes
import re
from .blocks import Blocks
__all__ = ["load", "World", "Player", "Block", "Blocks", "WORLD_HEIGHT", "WORLD_SIZE", "WORLD_BLOCKS"]

world_sig_regex = rb"WORLD."
world_layer_sig_regex = world_sig_regex+b"\d\d"
WORLD_HEIGHT = 16
WORLD_SIZE = 48



class Block(Structure):
    _fields_ = (("id", c_uint8),)

    @property
    def name(self):
        return Blocks(self.id).name

    def __repr__(self):
        return f"{self.name}(id={self.id})"

WORLD_BLOCKS = Block * WORLD_SIZE * WORLD_SIZE * WORLD_HEIGHT # Block_Array_48_Array_48_Array_16 array

class World(Structure):
    # blocks[y][x][z]
    block = WORLD_BLOCKS
    _fields_ = [("blocks", WORLD_BLOCKS)] # blocks[16][48][48]
    
    @staticmethod
    def decode_world(data: bytes):
        return World.from_buffer_copy(data)
    
    def encode(self):
        return bytes(self)
    
    def set_block(self, x, y, z, block):
        if isinstance(block, Blocks):
            block = Block(block.value)
        elif isinstance(block, int):
            block = Block(block)
        self.blocks[y][x][z] = block


class Player(Structure):
    _fields_ = (
            ("x", c_int8),
            ("y", c_int8),
            ("z", c_int8),
            ("current_block", Block),
            ("scroll_Xs",  c_int8*3),
            ("scroll_Ys",  c_int8*3),
            )

    @staticmethod
    def decode_player(data: bytes):
        return Player.from_buffer_copy(data)

    def encode(self):
        return bytes(self)


class Buffer(BytesIO):
    def read_c(self, ctype):
        return ctype.from_buffer_copy(self.read(ctypes.sizeof(ctype)))
    def ti_read(self, buffer: BytesIO, elements, bytes_per_element):
        """
        Reads data from the file into the given buffer.

        Args:
            buffer (bytes): The buffer to read into.
            elements (int): The number of elements to read.
            bytes_per_element (int): The number of bytes per element.
        """

        return self.write(buffer.read(elements * bytes_per_element))



class InvaildFormat(Exception):
    pass

def load(world_id: str) -> tuple[Player, World]:
    filename = f"WORLD{world_id}.8xv"
    with open(filename, "rb") as f:
        content = f.read()
        search: re.Match[bytes] = re.search(world_sig_regex, content)
        if search is None:
            raise InvaildFormat("Not a valid world file")
        content = content[search.span()[1]+8:]
        player: Player = Player.decode_player(content)
    world: World = World()

    for i in range(WORLD_HEIGHT):
        out_name = "WORLD{}{:02}.8xv".format(world_id, i)
        with open(out_name, "rb") as f:
            content = f.read()
            search = re.search(world_layer_sig_regex, content)
            if search is None:
                raise InvaildFormat("Not a valid world file: {}".format(out_name))
            
            world.blocks[i] = (Block * WORLD_SIZE * WORLD_SIZE).from_buffer_copy(content[search.span()[1]+6:-2])
    return player, world

def save(world_id: str, player: Player, world: World):
    # untested
    header = b"**TI83F*\x1a\n\x00Created via TIBlocks.py".ljust(60, b"\0")
    var_name = f"WORLD{world_id}"
    with open(var_name+".8xv", "wb") as f:
        f.write(header + var_name.encode() +  b"\x00\x00\x00\x80\x0C\x00\x0A\x00" + player.encode() + b"\x0c\x00\n\x00\x00\x08\x18\x03\x00\x01x\x00\x01p\x9a\x03")
    for i in range(WORLD_HEIGHT):
        out_name = "WORLD{}{:02}".format(world_id, i)
        with open(out_name+".8xv", "wb") as f:
            f.write(header + out_name.encode() + b"\x00\x80\x02\x09\x00\x09" + world.encode() + "\b\b")





# 0008180D000178000170
#print(load("A"))
#print(ctypes.sizeof(Player))