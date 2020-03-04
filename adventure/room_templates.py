# actual size of the window
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 70

# size of the map
MAP_WIDTH = 90
MAP_HEIGHT = 60

# Tilesets
# Tiles which block movement
BLOCKED_CHARS = ['X', '█', ' ', 'O']
# Tiles which allow movement
EMPTY_CHARS = ['`']
# Tiles which transport you to another room when entered
DOOR_CHARS = ['n', 's', 'e', 'w']

# Depreciated contend commented below
# # Basic room
# basic = [['█' for x in range(MAP_WIDTH)]] \
#         + [['█'] + ['`' for x in range(MAP_WIDTH-2)] + ['█']
#             for y in range(MAP_HEIGHT-2)] \
#         + [['█' for x in range(MAP_WIDTH)]] \

# room_array = [
#     ['`' for x in range(MAP_WIDTH)]
#     for y in range(MAP_HEIGHT)
# ]
# for pos, i in enumerate(room_array[0]):
#     room_array[0][pos] = '█'
# for pos, i in enumerate(room_array[-1]):
#     room_array[-1][pos] = '█'
# for pos, i in enumerate(room_array):
#     room_array[pos][0] = '█'
#     room_array[pos][-1] = '█'

# # █
# # test wall
# room_array[0][60] = '█'
# room_array[1][60] = '█'
# room_array[2][60] = '█'
# # test doors
# room_array[0][51] = 'n'
# room_array[2][48] = 'w'
# room_array[2][52] = 'e'
# room_array[4][51] = 's'

'''
Default room creation
'''
default_array = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]

# Create outer walls
for pos, i in enumerate(default_array[0]):
    default_array[0][pos] = '█'
for pos, i in enumerate(default_array[-1]):
    default_array[-1][pos] = '█'
for pos, i in enumerate(default_array):
    default_array[pos][0] = '█'
    default_array[pos][-1] = '█'


'''
2x2 void center room creation
'''
# Create room area.
center_void_array = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]

# Create outer walls
for pos, i in enumerate(center_void_array[0]):
    center_void_array[0][pos] = '█'
for pos, i in enumerate(center_void_array[-1]):
    center_void_array[-1][pos] = '█'
for pos, i in enumerate(center_void_array):
    center_void_array[pos][0] = '█'
    center_void_array[pos][-1] = '█'

# Create a 2x2 center void
center_void_array[29][44] = 'O'
center_void_array[30][44] = 'O'
center_void_array[29][45] = 'O'
center_void_array[30][45] = 'O'


'''
void x axis
'''
# Create room area.
center_void_array = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]

# Create outer walls
# Top wall
for pos, i in enumerate(center_void_array[0]):
    center_void_array[0][pos] = '█'
# Bottom wall
for pos, i in enumerate(center_void_array[-1]):
    center_void_array[-1][pos] = '█'
# Side walls
for pos, i in enumerate(center_void_array):
    center_void_array[pos][0] = '█'
    center_void_array[pos][-1] = '█'

# Create void splitting room along center across x axis
for pos, i in enumerate(center_void_array[29]):
    if center_void_array[pos][44] in EMPTY_CHARS:
        center_void_array[pos][44] = 'O'
    if center_void_array[pos][45] in EMPTY_CHARS:
        center_void_array[pos][45] = 'O'

'''
void y axis
'''
# Create room area.
center_void_array = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]

# Create outer walls
# Top wall
for pos, i in enumerate(center_void_array[0]):
    center_void_array[0][pos] = '█'
# Bottom wall
for pos, i in enumerate(center_void_array[-1]):
    center_void_array[-1][pos] = '█'
# Side walls
for pos, i in enumerate(center_void_array):
    center_void_array[pos][0] = '█'
    center_void_array[pos][-1] = '█'

# Create void splitting room along center across x axis
for pos, i in enumerate(center_void_array):
    if center_void_array[pos][pos] in EMPTY_CHARS:
        center_void_array[pos][pos] = 'O'
    if center_void_array[pos][pos] in EMPTY_CHARS:
        center_void_array[pos][pos] = 'O'


# list of rooms
def get_array(key):
    room_arrays_dict = {
        "default": default_array,
        'center_void': center_void_array
    }
    return room_arrays_dict[key]
