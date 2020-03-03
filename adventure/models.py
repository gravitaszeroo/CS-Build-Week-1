from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

# actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 10


class Tile:
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class Object:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, room_array, dx, dy):
        # move by the given amount, if the destination is not blocked
        if not room_array[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION"
        )
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    # array representing objects in the room
    room_array = [
        ['█' for y in range(MAP_WIDTH)]
        for x in range(MAP_HEIGHT)
    ]
    # █

    room_array[0][0] = '@'

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
        return [p.user.username for p in
                Player.objects.filter(currentRoom=self.id)
                if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id)
                if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    x = 0
    y = 0

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


# Generic creature Django object for both enemies and NPCs
class Creature(models.Model):
    # Create and set unique ID
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    # Create and set character field for creature name
    name = models.CharField(max_length=200)

    # Set the default x, y position of the creature on map
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    # Set the current room of the creature, default 0
    currentRoom = models.IntegerField(default=0)

    # Set the hostile/passive state of the creture
    hostile = models.BooleanField(default=True)


# Generic item object
class Items(models.Model):
    # Create and set unique ID
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    # Set the default x, y position of the item on map
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    # Set the current room of the item, default 0
    currentRoom = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
