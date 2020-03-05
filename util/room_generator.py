# from django.contrib.auth.models import User
from adventure.models import Player, Room
from adventure.room_templates import room_arrays_dict, MAP_WIDTH, MAP_HEIGHT
from util.blocks import place_block
import json
import random
import os


wd = os.getcwd()
Room.objects.all().delete()
no_of_rooms = 10

f = open(wd+'/util/nounlist.txt')
nouns = (f.read().split("\n"))
f.close()
f = open(wd+'/util/english-nouns.txt')
engnouns = (f.read().split("\n"))
f.close()
f = open(wd+'/util/english-adjectives.txt')
engadj = (f.read().split("\n"))
f.close()

rooms = []
for i in range(no_of_rooms):
    room_noun = random.choice(nouns)
    room_adj = random.choice(engadj)
    room_snoun = random.choice(engnouns)
    roomtitle = room_noun + " "+room_adj+" " +room_snoun
    print(roomtitle)
    new_array_choice = random.choice(list(room_arrays_dict.keys()))
    new_room_array = room_arrays_dict[new_array_choice]
    new_room_array = place_block(new_room_array)
    created_room = Room(title=roomtitle,
                        description = "you should avoid " + room_snoun + \
                                        " and conquer " + room_noun,
                        room_array=json.dumps(new_room_array))
    created_room.save()
    rooms.append(created_room)

entry_room = rooms[0]
exit_room = rooms[no_of_rooms-1]
rooms.remove(entry_room)
rooms.remove(exit_room)
new_room = entry_room
opposite_direction = None
while len(rooms)> 4:
    no_of_doors = random.choice([1,2,3])
    directions = ['n','s','e','w']
    if opposite_direction:
        directions.remove(opposite_direction)
    for i in range(no_of_doors):
        select_room = random.choice(rooms)
        select_direction = random.choice(directions)
        if select_direction == 'n':
            opposite_direction = 's'
        if select_direction == 's':
            opposite_direction = 'n'
        if select_direction == 'e':
            opposite_direction = 'w'
        if select_direction == 'w':
            opposite_direction = 'e'
        new_room.connectRooms(select_room,select_direction)
        select_room.connectRooms(new_room,opposite_direction)
        rooms.remove(select_room)
        directions.remove(select_direction)
    new_room = select_room

directions = ['n','s','e','w']
directions.remove(select_direction)
new_direction = random.choice(directions)
if new_direction == 'n':
    opposite_direction = 's'

if new_direction == 's':
    opposite_direction = 'n'

if new_direction == 'e':
    opposite_direction = 'w'

if new_direction == 'w':
    opposite_direction = 'e'

remaining = len(rooms)
for i in range(remaining):
    new_room.connectRooms(rooms[i],new_direction)
    rooms[i].connectRooms(new_room,opposite_direction)
    new_room = rooms[i]

#print(len(rooms))
exit_room.connectRooms(new_room,opposite_direction)
new_room.connectRooms(exit_room,new_direction)
