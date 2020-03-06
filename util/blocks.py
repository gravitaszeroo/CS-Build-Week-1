from adventure.room_templates import room_arrays_dict, MAP_WIDTH, MAP_HEIGHT
import random
import json



def place_block(room_array):
    # min and max number of blocks added to room
    # Maybe we can use numpy.random.normal later
    MIN_BLOCKS = 1
    MAX_BLOCKS = 10
    # Place some blocks in the room
    for placement in range(random.randrange(MIN_BLOCKS, MAX_BLOCKS)):
        block = random.choice(blocks)
        max_row = max(block, key=len)
        anchor = (random.randrange(1, MAP_WIDTH-2-len(max_row)),
                    random.randrange(1, MAP_HEIGHT-2-len(block)))
        for rownum, row in enumerate(block):
            room_array[anchor[1]+rownum][anchor[0]:anchor[0]+len(row)] = list(row)
    return room_array


blocks = [

    [
    '`````',
    '````',
    '```',
    '``',
    '`',
    ],

    [
    '```````````````````',
    '````````````',
    '```````',
    '```',
    '`',
    ],

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

    ['█',
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


def place_door(origin, direction, destination):
    """Creates doors and connections between two rooms

    origin : Room object
    direction : string char for directions
    destination : Room object
    """

    # get block for the corresponding door
    block = direction_blocks[direction]
    # choose a random anchor point for the door
    for neighbor in [origin, destination]:
        if direction == 'n':
            anchor = (random.randrange(1, MAP_WIDTH-2-len(block[0])), 0)
        if direction == 's':
            anchor = (random.randrange(1, MAP_WIDTH-2-len(block[-1])), MAP_HEIGHT-5)
        if direction == 'e':
            anchor = (MAP_WIDTH-5, random.randrange(1, MAP_HEIGHT-2-len(block)))
        if direction == 'w':
            anchor = (0, random.randrange(1, MAP_HEIGHT-2-len(block)))

        # load room array, add door, update room array
        room_array = json.loads(neighbor.room_array)
        for rownum, row in enumerate(block):
            room_array[anchor[1]+rownum][anchor[0]:anchor[0]+len(row)] = list(row)
        neighbor.room_array = json.dumps(room_array)
        print(anchor, direction)

    if direction == "n":
        origin.n_to = destination.id
        destination.s_to = origin.id
    elif direction == "s":
        origin.s_to = destination.id
        destination.n_to = origin.id
    elif direction == "e":
        origin.e_to = destination.id
        destination.w_to = origin.id
    elif direction == "w":
        origin.w_to = destination.id
        destination.e_to = origin.id
    else:
        print("Invalid direction")
    print(origin.title, direction, "->", destination.title)
    origin.save()
    destination.save()
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
