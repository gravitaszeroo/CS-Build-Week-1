from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
from .room_templates import *
import json

#actual size of the window
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 70

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, room_array, dx, dy):
        #move by the given amount, if the destination is not blocked
        if not room_array[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    room_array = models.CharField(max_length=2000, default=json.dumps(get_array('default')))

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUsers(self, currentPlayerID):
        return [p.user for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerObjects(self, currentPlayerID):
        return [p for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()
    def get_position(self):
        return self.x, self.y
    def move(self, x, y):
        self.x = x
        self.y = y
    def change_room(self, direction, nextRoomID=None):
        """Move a player from room to room.

        player : request.user.player
            Player class in models.py
        """
        assert direction in DOOR_CHARS
        room = self.room()
        nextRoomID = None
        if direction == "n":
            nextRoomID = room.n_to
        elif direction == "s":
            nextRoomID = room.s_to
        elif direction == "e":
            nextRoomID = room.e_to
        elif direction == "w":
            nextRoomID = room.w_to
        if nextRoomID is not None and nextRoomID > 0:
            nextRoom = Room.objects.get(id=nextRoomID)
            self.currentRoom = nextRoomID
            # TODO: change user position to match new room
            # DON'T put the user on the door in the new room!!
            self.save()

    def validate_move(self, x, y):
        x = min(MAP_WIDTH-1, x)
        y = min(MAP_HEIGHT-1, y)
        x = max(1, x)
        y = max(1, y)
        room = json.loads(self.room().room_array)
        target_char = room[y][x]
        if target_char in DOOR_CHARS:
            self.change_room(target_char)
            return
        if not room[y][x] in BLOCKED_CHARS:
            self.move(x, y)
            self.save()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
