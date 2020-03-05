from adventure.room_templates import room_arrays_dict, MAP_WIDTH, MAP_HEIGHT
import random

def place_block(room_array):
    block = random.choice(blocks)
    anchor = (random.randrange(1, MAP_WIDTH-2-len(block[0])),
                random.randrange(1, MAP_HEIGHT-2-len(block)))
    print(anchor)
    for rownum, row in enumerate(block):
        room_array[anchor[1]+rownum][anchor[0]:anchor[0]+len(row)] = list(row)
        print(room_array[anchor[1]+rownum][anchor[0]:anchor[0]+len(row)])
    return room_array


# building blocks to
blocks = [
    ['████████████',
     '█████n██████',
     '████```█████'],

    ['████```█████',
     '█████s██████',
     '████████████'],

    ['████',
     '███w',
     '████'],

    ['████',
     'e███',
     '████'],
]
