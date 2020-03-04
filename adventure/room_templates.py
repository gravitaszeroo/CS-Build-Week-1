# actual size of the window
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 70

# size of the map
MAP_WIDTH = 90
MAP_HEIGHT = 60

# Tilesets
BLOCKED_CHARS = ['X', '█', ' ']
EMPTY_CHARS = ['`']
DOOR_CHARS = ['n', 's', 'e', 'w']

# Basic room
basic = [['█' for x in range(MAP_WIDTH)]] \
        + [['█'] + ['`' for x in range(MAP_WIDTH-2)] + ['█']
            for y in range(MAP_HEIGHT-2)] \
        + [['█' for x in range(MAP_WIDTH)]] \

room_array = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]
for pos, i in enumerate(room_array[0]):
    room_array[0][pos] = '█'
for pos, i in enumerate(room_array[-1]):
    room_array[-1][pos] = '█'
for pos, i in enumerate(room_array):
    room_array[pos][0] = '█'
    room_array[pos][-1] = '█'

# █
# test wall
room_array[0][60] = '█'
room_array[1][60] = '█'
room_array[2][60] = '█'
# test doors
room_array[0][51] = 'n'
room_array[2][48] = 'w'
room_array[2][52] = 'e'
room_array[4][51] = 's'

default_array = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]

for pos, i in enumerate(default_array[0]):
    default_array[0][pos] = '█'
for pos, i in enumerate(default_array[-1]):
    default_array[-1][pos] = '█'
for pos, i in enumerate(default_array):
    default_array[pos][0] = '█'
    default_array[pos][-1] = '█'


# list of rooms
def get_array(key):
    room_arrays_dict = {
        "default": default_array
    }
    return room_arrays_dict[key]
