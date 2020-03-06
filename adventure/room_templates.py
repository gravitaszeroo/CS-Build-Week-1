# actual size of the window
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 30

# size of the map
MAP_WIDTH = 120
MAP_HEIGHT = 28

# Tilesets
# Tiles which block movement
BLOCKED_CHARS = ['X', '█', ' ', 'O']
# Tiles which allow movement
EMPTY_CHARS = ['`']
# Tiles which transport you to another room when entered
DOOR_CHARS = ['n', 's', 'e', 'w']
# Tiles which block LoS
SIGHT_CHARS = ['f']

'''
Default room creation
'''
default_array = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]

# Create outer walls
# Top wall
for pos, i in enumerate(default_array[0]):
    default_array[0][pos] = '█'
# Bottom wall
for pos, i in enumerate(default_array[-1]):
    default_array[-1][pos] = '█'
# Side walls
for pos, i in enumerate(default_array):
    default_array[pos][0] = '█'
    default_array[pos][-1] = '█'

# Doors
default_array[MAP_HEIGHT//2 + 2][MAP_WIDTH//2] = 'n'
default_array[MAP_HEIGHT//2 - 2][MAP_WIDTH//2] = 's'
default_array[MAP_HEIGHT//2][MAP_WIDTH//2 + 2] = 'e'
default_array[MAP_HEIGHT//2][MAP_WIDTH//2 - 2] = 'w'


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
center_void_array[MAP_HEIGHT//2-1][MAP_WIDTH//2-1] = 'O'
center_void_array[MAP_HEIGHT//2][MAP_WIDTH//2-1] = 'O'
center_void_array[MAP_HEIGHT//2-1][MAP_WIDTH//2] = 'O'
center_void_array[MAP_HEIGHT//2][MAP_WIDTH//2] = 'O'

# Doors
center_void_array[MAP_HEIGHT//2 + 2][MAP_WIDTH//2] = 'n'
center_void_array[MAP_HEIGHT//2 - 2][MAP_WIDTH//2] = 's'
center_void_array[MAP_HEIGHT//2][MAP_WIDTH//2 + 2] = 'e'
center_void_array[MAP_HEIGHT//2][MAP_WIDTH//2 - 2] = 'w'

'''
void x axis
'''
# Create room area.
x_axis_void = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]

# Create outer walls
# Top wall
for pos, i in enumerate(x_axis_void[0]):
    x_axis_void[0][pos] = '█'
# Bottom wall
for pos, i in enumerate(x_axis_void[-1]):
    x_axis_void[-1][pos] = '█'
# Side walls
for pos, i in enumerate(x_axis_void):
    x_axis_void[pos][0] = '█'
    x_axis_void[pos][-1] = '█'

# Create void splitting room along center across x axis
for pos, i in enumerate(x_axis_void[29]):
    if x_axis_void[MAP_HEIGHT//2-1][pos] in EMPTY_CHARS:
        x_axis_void[MAP_HEIGHT//2-1][pos] = 'O'
    if x_axis_void[MAP_HEIGHT//2][pos] in EMPTY_CHARS:
        x_axis_void[MAP_HEIGHT//2][pos] = 'O'

# Doors
x_axis_void[MAP_HEIGHT//2 + 2][MAP_WIDTH//2] = 'n'
x_axis_void[MAP_HEIGHT//2 - 2][MAP_WIDTH//2] = 's'
x_axis_void[MAP_HEIGHT//2][MAP_WIDTH//2 + 2] = 'e'
x_axis_void[MAP_HEIGHT//2][MAP_WIDTH//2 - 2] = 'w'

'''
void y axis
'''
# Create room area.
y_axis_void = [
    ['`' for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT)
]

# Create outer walls
# Top wall
for pos, i in enumerate(y_axis_void[0]):
    y_axis_void[0][pos] = '█'
# Bottom wall
for pos, i in enumerate(y_axis_void[-1]):
    y_axis_void[-1][pos] = '█'
# Side walls
for pos, i in enumerate(y_axis_void):
    y_axis_void[pos][0] = '█'
    y_axis_void[pos][-1] = '█'

# Create void splitting room along center across y axis
for pos, i in enumerate(y_axis_void):
    if y_axis_void[pos][MAP_WIDTH//2-1] in EMPTY_CHARS:
        y_axis_void[pos][MAP_WIDTH//2-1] = 'O'
    if y_axis_void[pos][MAP_WIDTH//2] in EMPTY_CHARS:
        y_axis_void[pos][MAP_WIDTH//2] = 'O'

# Doors
y_axis_void[MAP_HEIGHT//2 + 2][MAP_WIDTH//2] = 'n'
y_axis_void[MAP_HEIGHT//2 - 2][MAP_WIDTH//2] = 's'
y_axis_void[MAP_HEIGHT//2][MAP_WIDTH//2 + 2] = 'e'
y_axis_void[MAP_HEIGHT//2][MAP_WIDTH//2 - 2] = 'w'


# list of rooms
def get_array(key):
    room_arrays_dict = {
        "default": default_array,
        'center_void': center_void_array,
        'x_axis_void': x_axis_void,
        'y_axis_void': y_axis_void
    }
    return room_arrays_dict[key]
