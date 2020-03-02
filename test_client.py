import requests
import json

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
print(s.text)

# move rooms
while True:
    direction = "empty"
    while direction.lower() not in ['n', 's', 'e', 'w']:
        direction = input("Direction: N/S/E/W? ").lower()
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

# move around the room
