from adventure.models import Player, Room, Creature
from adventure.room_templates import room_arrays_dict, MAP_WIDTH, MAP_HEIGHT, BLOCKED_CHARS, EMPTY_CHARS, DOOR_CHARS
import json
import random

def add_creatures(target_room):
    MIN_CREATURES = 1
    MAX_CREATURES = 3
    for i in range(3):
        # get room and find a legal starting point
        room_array = json.loads(target_room.room_array)
        target_char = '█' # dummy
        while target_char in (BLOCKED_CHARS or DOOR_CHARS):
            x = random.randrange(1, len(room_array[0]))
            y = random.randrange(1, len(room_array))
            target_char = room_array[y][x]
        creature = Creature(name='Gorgon',
                            x = x,
                            y = y,
                            currentRoom = target_room.id
                            )
        creature.save()