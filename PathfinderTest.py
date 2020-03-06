# Tilesets
# Tiles which block movement
BLOCKED_CHARS = ['X', '█', ' ', '▓', 1]
# Tiles which allow movement
EMPTY_CHARS = ['`']
# Tiles which transport you to another room when entered
DOOR_CHARS = ['n', 's', 'e', 'w']
# Tiles which block LoS
HIDDEN_CHARS = ['f']

import json


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """
    Returns a list of tuples as a path from the
    given start to the given end in the given maze
    """

    # Create an iterator to break out of loop
    # if no path is found quickly enough, default max 100
    breakout_interator = 0

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node or breakout_interator == 100:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # Get node position
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) \
                or node_position[0] < 0 \
                    or node_position[1] > (len(maze[len(maze)-1]) - 1) \
                    or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) \
                + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

        breakout_interator += 1


def pathfind_astar(map_array, start, end):
    '''
    Returns list of tuples as a path from current(start) position
    to the end.
    Requires map array and tuple (x, y) endpoint
    '''
    # Create an iterator to break out of loop
    # if no path is found quickly enough, default max 100
    breakout_interator = 0

    # Create the start and end nodes
    start_node = Node(None, start)
    end_node = Node(None, end)
    start_node.g = start_node.h = start_node.f = 0
    end_node.g = end_node.h = end_node.f = 0

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
        if current_node == end_node or breakout_interator == 100:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            # Save path
            print("saving path", path)
            # self.path = json.dumps(path[::-1])
            # self.path.save()
            path.pop()
            return path[::-1]  # Return the reversed path

        # Generate the children
        children = []
        print('current position', current_node.position[0], current_node.position[1])
        for new_position in [
            (0, -1), (0, 1), (-1, 0), (1, 0)
            # Uncomment below if allowing diagonal movement
            # ,(-1, -1), (-1, 1), (1, -1), (1, 1)
                ]:  # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])
            

            # Make sure the new position is within range of the map_array
            if node_position[0] > (len(map_array) - 1)\
                or node_position[0] < 0\
                    or node_position[1] > \
                    (len(map_array[len(map_array)-1]) - 1)\
                    or node_position[1] < 0:
                continue

            # Make sure that the terrain is walkable,
            # aka not in the BLOCKED_CHARS global list
            # if in blocked_char, continue
            # currently, also disallow movement through doors
            if map_array[node_position[0]][node_position[1]] \
                in BLOCKED_CHARS \
                    or map_array[node_position[0]][node_position[1]] \
                    in DOOR_CHARS:
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
        # Increment the breakout operator
        breakout_interator += 1


def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
            [1, 1, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]

    start = (0, 0)
    end = (7, 9)

    # path = astar(maze, start, end)
    path = pathfind_astar(maze, start, end)
    print(path)

    json_path = json.dumps(path)
    path = json.loads(json_path)
    print(len(path))
    print(path)

    step = path.pop(0)
    print(step)

    empty = [1]
    empty.pop(0)
    json_empty = json.dumps(empty)
    empty = json.loads(json_empty)
    print(len(empty))
    print(empty)
if __name__ == '__main__':
    main()
