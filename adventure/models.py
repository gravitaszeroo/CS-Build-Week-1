from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

#actual size of the window
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 70

#size of the map
MAP_WIDTH = 150
MAP_HEIGHT = 100

# Tilesets
BLOCKED_CHARS = ['X']


class Tile:
    # a tile of the map_array and its properties
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
        ['█' for x in range(MAP_WIDTH)]
        for y in range(MAP_HEIGHT)
    ]
    # █
    room_array[0][50] = 'X'
    room_array[1][50] = 'X'
    room_array[2][50] = 'X'
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

    def playerUsers(self, currentPlayerID):
        return [p.user for p in Player.objects.filter(currentRoom=self.id)
                if p.id != int(currentPlayerID)]

    def playerObjects(self, currentPlayerID):
        return [p for p in Player.objects.filter(currentRoom=self.id)
                if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id)
                if p.id != int(currentPlayerID)]


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
    def valid_move(self, x, y):
        x = min(MAP_WIDTH, x)
        y = min(MAP_HEIGHT, y)
        x = max(0, x)
        y = max(0, y)
        room = self.room().room_array
        print(len(room))
        print(len(room[0]))
        if not room[y][x] in BLOCKED_CHARS:
            return True
        else:
            False


# Node class to assisst in the A* pathfinding
class Node():
    def __init__(self, parent=None, position=None):
        # Parent node, aka node closer to start point.
        self.parent = parent
        # x, y position of the node
        self.position = position

        # Tile value cost
        # Exact cost of node
        self.g = 0
        # Heuristic estimated cost of node to goal
        self.h = 0
        # Cost of the lowest cost neighbor
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# Generic creature Django object for both enemies and NPCs
class Creature(models.Model):
    # Create and set unique ID
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    # Create and set character field for creature name
    name = models.CharField(max_length=200)

    # Set the default x, y position of the creature on map_array
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    # Set the current room of the creature, default 0
    currentRoom = models.IntegerField(default=0)

    # Set the hostile/passive state of the creture
    attackable = models.BooleanField(default=True)
    hostile = models.BooleanField(default=True)

    # Set attack damage of the creature
    creature_damage = models.IntegerField(default=1)

    # Set default hit points and death state of the creature
    hp = models.IntegerField(default=1)
    death_state = models.BooleanField(default=False)

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

    def combat(self, attack_damage=0):
        # If creature is not attackable, disallow the attack
        if self.attackable is False:
            return 'You cannot attack this creature.'
        # If creature is attackable, but not hostile, set hostile flag to true
        if self.hostile is False:
            self.hostile = True

        # Take attack damage away from HP
        self.hp -= attack_damage
        # If hp is 0 or less, set death flag to True
        if self.hp <= 0:
            self.death_state = True

        if self.death_state = False:
            return attack_damage
        else:
            return 'You have killed the creature'

    def pathfind_astar(self, map_array, end):
        '''
        Returns list of tuples as a path from current(start) position
        to the end.
        Requires map array and tuple (x, y) endpoint
        '''
        # Create the start and end nodes
        start_node = Node(None, (self.x, self.y))
        end_node = Node(None, end)

        # Init an open and closed list
        open_list = []
        closed_list = []

        # Add start node to the open list
        open_list.append(start_node)

        # Loop until end is found
        while len(open_list) > 0:

            # Get current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off the open list and add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # If found goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return the reversed path

            # Generate the children
            children = []
            for new_position in [
                (0, -1), (0, 1), (-1, 0), (1, 0),
                (-1, -1), (-1, 1), (1, -1), (1, 1)
                    ]:  # Adjacent squares
                # Get node position
                node_position = (current_node.position[0] + new_position[0],
                                 current_node.position[1] + new_position[1])

            # Make sure the new position is within range of the map_array
            if node_position[0] > (len(map_array) - 1)
            or node_position[0] < 0
            or node_position[1] > (len(map_array[len(map_array)-1]) - 1)
            or node_position[1] < 0:
                continue

            # Make sure that the terrain is walkable
            # TODO, replace 0 with the wall/void tile character
            if map_array[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append the new node
            children.append(new_node)

            # Loop through the children
            for child in children:
                # For child in closed list
                for closed_child in closed_list:
                    # If child already in closed, continue without updating
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) +\
                          ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child already in open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


# Generic item object
class Items(models.Model):
    # Create and set unique ID
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    # Set the default x, y position of the item on map_array
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    # Set the current room of the item, default 0
    currentRoom = models.IntegerField(default=0)

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


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
