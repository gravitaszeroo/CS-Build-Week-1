from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    """Initialize a new player in the start room."""
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players}, safe=True)

## Boilerplate code for pusher that we may not use
# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))
# for p_uuid in currentPlayerUUIDs:
#     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
# for p_uuid in nextPlayerUUIDs:
#     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})

@csrf_exempt
@api_view(["POST"])
def get_room(request):
    """Gets room state given user input."""
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    # load data from request
    data = json.loads(request.body)
    # get player's attempted x and y position for validation
    data_x, data_y = int(data['x']), int(data['y'])
    # Move the player if possible, or change rooms if player enters door
    player.validate_move(data_x, data_y)
    # Get the player's current room
    room = player.room()
    room_array = json.loads(room.room_array)
    player_objects = room.playerObjects(player_id)
    creature_objects = room.creatureObjects(player_id)
    # Get coordinates for each player in the room
    players = {p.user.username:{'x':p.get_position()[0], 'y':p.get_position()[1]} for p in player_objects}
    player.save()

    
    # Get coordinates for creatures in room w player
    scores = {p.score:{'scores':p.get_score()} for p in player_objects}
    print(scores)
    creatures = {str(c.uuid):{'x':c.x, 'y':c.y, 'name':c.name} for c in creature_objects}
    return JsonResponse({'name':player.user.username, 'title':room.title,
                        'x': player.x, 'y': player.y, 'room_array':room_array,
                        'description':room.description, 'players':players,
                        'scores':scores,
                        'creatures':creatures,
                         'error_msg':""}, safe=False)

@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)
