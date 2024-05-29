import requests
import json
import hashlib
token='LbyDaYQfoqWfYmTt'

md5_hash = hashlib.md5()
user='gidroliz'
password='123456'
email='gidroliz@yandex.ru'

md5_hash.update(password.encode('utf-8'))
hashed_password = md5_hash.hexdigest()

url='http://localhost:5656'

# body={"command": "get_all_tasks", "data": None}
# body={"command": "new_user", "data": {"name": user, "email": email, "password": hashed_password}}
body={"command": "authorization", "data": {"name": user, "password": hashed_password}}

headers={'Authorization': token}
resp = requests.post(url, data=json.dumps(body), headers=headers)
print(resp.status_code, resp.reason, resp.content)

token=resp.json()['answer']['token']
headers={'Authorization': token}

# body={"command": "get_task", "data": {"hard": 1}}
# body={"command": "get_task", "data": {"hard": "custom", "min": -10, "max": 50, "operators": ["+","-"], "numofoperands": 5, "brackets": True}}
# body={"command": "counter", "data": "custom"}
# body={"command": "correct_solution", "data": 2}
# body={"command": "wrong_solution", "data": "custom"}
# body={"command": "get_leaderboards", "data": None}
body={'command':'get_achievements', 'data':None}

resp = requests.post(url, data=json.dumps(body), headers=headers)
print(resp.status_code, resp.reason, resp.json())