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

# move north

# move around the room
