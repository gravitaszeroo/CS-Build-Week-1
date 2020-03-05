from adventure.room_templates import room_arrays_dict, MAP_WIDTH, MAP_HEIGHT
import random



def place_block(room_array):
    # min and max number of blocks added to room
    # Maybe we can use numpy.random.normal later
    MIN_BLOCKS = 1
    MAX_BLOCKS = 10
    # Place some blocks in the room
    for placement in range(random.randrange(MIN_BLOCKS, MAX_BLOCKS)):
        block = random.choice(blocks)
        anchor = (random.randrange(1, MAP_WIDTH-2-len(block[0])),
                    random.randrange(1, MAP_HEIGHT-2-len(block)))
        for rownum, row in enumerate(block):
            room_array[anchor[1]+rownum][anchor[0]:anchor[0]+len(row)] = list(row)
    return room_array

blocks = [

    [
    '▖▗▘'
    ],

    [
    '``ƒƒƒƒƒƒƒƒ',
    'ƒƒ``ƒƒƒ``ƒ',
    'ƒƒƒ``ƒƒƒ``',
    '``ƒƒ`ƒƒƒƒƒ',
    'ƒƒƒƒƒƒƒƒ``',
    '`ƒƒƒƒƒƒ`ƒ`',
    ],

    [
    'ƒlƒ``ƒƒl``',
    '``ƒƒlƒƒƒƒƒ',
    'ƒƒlƒƒƒlƒ``',
    '``ƒl`lƒƒƒƒ',
    'ƒƒllƒƒ`ƒ``',
    'ƒl``ƒlƒ``ƒ'
    ],

    [
    'ƒƒƒƒƒƒƒƒ``',
    '``ƒƒƒƒƒƒƒƒ',
    'ƒƒƒ``ƒƒƒƒ`',
    'ƒƒ``ƒƒƒ``ƒ',
    '``ƒƒ`ƒƒƒƒƒ',
    'ƒƒƒƒƒƒ`ƒ``',
    ],

    ['██████████████',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     ],

    ['██████████████',
     '`````````````█',
     '`````````````█',
     '`````````````█',
     '`````````````█',
     '`````````````█',
     '`````````````█',
     '`````````````█',
     '`````````````█',
     '`````````````█',
     '`````````````█',
     '`````````````█',

     ],

    ['█```````````````',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '█',
     '██████████████',
     ],

    [
    '```````````````█',
    '```````````````█',
    '```````````````█',
    '```````````````█',
    '```````````````█',
    '```````````````█',
    '```````````````█',
    '```````````````█',
    '```````````````█',
    '```````````````█',
    '```````````````█',
     '██████████████',
     ],

    ['▓',
     '▓▓',
     '▓▓▓',
     '▓▓▓▓',
     '▓▓▓▓',
     '▓▓▓',
     '▓▓',
     '▓'],

    ['```▓▓',
     '``▓▓',
     '`▓▓',
     '▓▓'],

    ['▓▓',
     '`▓▓',
     '``▓▓',
     '```▓▓'],

    ['▓▓▓▓▓',
     '▓▓▓▓▓',
     '▓▓▓▓▓',
     '▓▓▓▓▓',
     '▓▓▓▓▓'],

    ['▓▓▓▓▓',
     '▓▓▓▓▓',
     '▓▓▓▓▓'],

]


def place_door(room_array, direction):
    block = direction_blocks[direction]
    if direction == 'n':
        anchor = (random.randrange(1, MAP_WIDTH-2-len(block[0])), 0)
    if direction == 's':
        anchor = (random.randrange(1, MAP_WIDTH-2-len(block[-1])), MAP_HEIGHT-5)
    if direction == 'e':
        anchor = (MAP_WIDTH-5, random.randrange(1, MAP_HEIGHT-2-len(block)))
    if direction == 'w':
        anchor = (0, random.randrange(1, MAP_HEIGHT-2-len(block)))
    for rownum, row in enumerate(block):
        print(anchor, direction, len(room_array), len(room_array[0]))
        room_array[anchor[1]+rownum][anchor[0]:anchor[0]+len(row)] = list(row)
    return room_array


# directional building blocks
direction_blocks = {
    'n': ['████████████',
          '█████n██████',
          '████```█████',
          '````````````',
          '````````````',
          ],

    's': [
          '````````````',
          '````````````',
          '████```█████',
          '█████s██████',
          '████████████'
          ],

    'w': ['████``',
          '███w``',
          '████``'],

    'e': ['``████',
          '``e███',
          '``████'],
}
