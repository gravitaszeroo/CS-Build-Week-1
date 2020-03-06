# from django.contrib.auth.models import User
from adventure.models import Player, Room, Creature
from adventure.room_templates import room_arrays_dict, MAP_WIDTH, MAP_HEIGHT, BLOCKED_CHARS, EMPTY_CHARS, DOOR_CHARS
from util.blocks import place_block, place_door
from util.add_items import add_creatures
import json
import random
import os

print(BLOCKED_CHARS)
# ƺ
# generate creatures in rooms


wd = os.getcwd()
Room.objects.all().delete()
Creature.objects.all().delete()
no_of_rooms = 10

# get words for room titles
f = open(wd+'/util/nounlist.txt')
nouns = (f.read().split("\n"))
f.close()
f = open(wd+'/util/english-nouns.txt')
engnouns = (f.read().split("\n"))
f.close()
f = open(wd+'/util/english-adjectives.txt')
engadj = (f.read().split("\n"))
f.close()



# generate rooms with templated arrays
rooms = []
for i in range(no_of_rooms):
    room_noun = random.choice(nouns)
    room_adj = random.choice(engadj)
    room_snoun = random.choice(engnouns)
    roomtitle = room_noun + " "+room_adj+" " +room_snoun
    # randomly choose room template
    new_array_choice = random.choice(list(room_arrays_dict.keys()))
    new_room_array = room_arrays_dict[new_array_choice].copy()
    # randomly place blocks inside the room array
    new_room_array = place_block(new_room_array)
    created_room = Room(title=roomtitle,
                        description = "you should avoid " + room_snoun + \
                                        " and conquer " + room_noun,
                        room_array=json.dumps(new_room_array))
    created_room.save()
    rooms.append(created_room)

# reserve a first and last room
exit_room = rooms[-1]
# rooms.remove(entry_room)
# rooms.remove(exit_room)
select_room = rooms.pop()
opposite_direction = None
opposites = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
while len(rooms)> 4:
    no_of_doors = random.choice([1,2,3])
    directions = ['n','s','e','w']
    if opposite_direction:
        # don't pick the same direction twice
        directions.remove(opposite_direction)
        ## pick a room to modify, remove it from rooms (RUINS LINEARITY)
        # select_room = random.choice(rooms)
        ## for the first while loop, connect entry room
    select_room_array = json.loads(select_room.room_array)
    # add neighbors
    for i in range(no_of_doors):
        # get pair of directions for neighboring rooms
        select_direction = random.choice(directions)
        opposite_direction = opposites[select_direction]
        # select rooms
        new_room = random.choice(rooms)
        # make doors, linkages between the two rooms
        place_door(select_room, select_direction, new_room)
        # remove that direction from options
        #print("74")
        directions.remove(select_direction)
        print(select_room.title, "<>", new_room.title)
        rooms.remove(new_room)

    # chain to the next room in While loop
    select_room = new_room

# connect remaining 4 rooms
directions = ['n','s','e','w']
directions.remove(select_direction)
new_direction = random.choice(directions)
remaining = len(rooms)
for i in range(remaining):
    select_room = rooms[i]
    place_door(select_room, new_direction, new_room)
    print(select_room.title, "<>", new_room.title)
    # chain to the next room
    new_room = rooms[i]

place_door(new_room, new_direction, exit_room)




# add creatures to all rooms
for target_room in Room.objects.all():
    add_creatures(target_room)

print("done!")
