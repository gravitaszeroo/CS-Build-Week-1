import curses
import requests
import json
import keyboard
from curses import wrapper

# register user
username = input("username?")

body = {"username":username,
 "password1":"testpassword",
 "password2":"testpassword"}

headers = {"Content-Type":"application/json"}
r = requests.post("http://127.0.0.1:8000/api/registration/", data=body)
print(r.status_code)
response = json.loads(r.text)
key = response['key']

# start game
headers = {"Authorization":f"Token {key}"}
s = requests.get('http://127.0.0.1:8000/api/adv/init/', headers=headers)
print(s.status_code)
print(s.text)

# move rooms
def move_rooms():
    while True:
        direction = "empty"
        while direction.lower() not in ['n', 's', 'e', 'w', 'room']:
            direction = str(input("N/S/E/W/room >>> ")).lower()
        if direction == 'room':
            # TODO: put doors in rooms and remove the above 4 lines
            wrapper(room_screen)
        body = {'direction':str(direction)}
        m = requests.post('http://127.0.0.1:8000/api/adv/move/', data=json.dumps(body), headers=headers)
        print(m.status_code)
        response = json.loads(m.text)
        print(response['title'])
        print(response['description'])
        print(response['players'])
        if 'room_array' in response.keys():
            for i in response['room_array']:
                print(''.join(i))


#initialize room screen
def room_screen(stdscr):
    # sc = curses.initscr()
    # h, w = sc.getmaxyx()
    # win = curses.newwin(h, w, 0, 0)
    # win.keypad(1)
    curses.curs_set(0)
    #
    # stdscr.addch(1, 1, curses.ACS_DIAMOND)

    height, width = stdscr.getmaxyx()
    keypress = 'f'
    player_x = int(width // 2)
    player_y = int((height // 2) + 3)

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # move around the room
    while keypress != ord('q'):
        # Initialization
        stdscr.clear()

        # TODO: add compensation for lag

        if keypress == curses.KEY_DOWN:
            player_y = player_y + 1
        elif keypress == curses.KEY_UP:
            player_y = player_y - 1
        elif keypress == curses.KEY_RIGHT:
            player_x = player_x + 1
        elif keypress == curses.KEY_LEFT:
            player_x = player_x - 1

        # restrict movement to screen
        player_x = max(0, player_x)
        player_x = min(width-1, player_x)
        player_y = max(0, player_y)
        player_y = min(height-1, player_y)

        # Update the server, get room
        data = {"x":player_x, "y":player_y}
        r = requests.post("http://127.0.0.1:8000/api/adv/get_room",
                            json=data, headers=headers)
        response = json.loads(r.text)

        # sync player location
        player_x = response['x']
        player_y = response['y']

        # Declaration of strings
        title = str(response['title'])[:width-1]
        subtitle = str(response['description'])[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(player_x, player_y)

        # Centering text
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_y = int((height // 2) - 2)

        # Show width and height
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-2, 0, statusbarstr)
        stdscr.addstr(height-2, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Show players in current room
        players_list = "Players: {}".format(', '.join(response['players']))
        stdscr.addstr(29, 0, players_list[:width-1], curses.color_pair(1))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addch(player_y, player_x, '@')

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        keypress = stdscr.getch()

move_rooms()

## Debug code (can be deleted)
# player_x = 0
# player_y = 0
#
# data = {"x":player_x, "y":player_y}
# r = requests.post("http://127.0.0.1:8000/api/adv/get_room",
#                     json=data, headers=headers)
# print(r.status_code)
# print(r.text[:200])
# response = json.loads(r.text)
# print(response['x'])
# print(response['y'])
# print(response['title'])
