import requests
import json
import hashlib

token = "LbyDaYQfoqWfYmTt"

md5_hash = hashlib.md5()
user = "gidroliz"
password = "123456"
email = "gidroliz@yandex.ru"

md5_hash.update(password.encode("utf-8"))
hashed_password = md5_hash.hexdigest()

url = "http://localhost:5656"


def make_request(body, headers, return_token=False):
    resp = requests.post(url, data=json.dumps(body), headers=headers)
    print(resp.status_code, resp.reason, resp.json())
    if return_token:
        return resp.json()["answer"]["token"]


headers = {"Authorization": token}

# body = {"command": "get_all_tasks", "data": None}
# make_request(body, headers)

# body={"command": "new_user", "data": {"name": user, "email": email, "password": hashed_password}}
body = {"command": "authorization", "data": {"name": user, "password": hashed_password}}
token = make_request(body, headers, True)
headers = {"Authorization": token}

# body = {"command": "get_task", "data": {"hard": 1}}
# make_request(body, headers)

# body = {
#     "command": "get_task",
#     "data": {
#         "hard": "custom",
#         "min": -10,
#         "max": 50,
#         "operators": ["+", "-"],
#         "numofoperands": 5,
#         "brackets": True,
#     },
# }
# make_request(body, headers)

# body = {"command": "counter", "data": "custom"}
# make_request(body, headers)

# body = {"command": "correct_solution", "data": 0}
# make_request(body, headers)

# body = {"command": "wrong_solution", "data": "custom"}
# make_request(body, headers)

# body = {"command": "get_leaderboards", "data": None}
# make_request(body, headers)

# body = {"command": "get_achievements", "data": None}
# make_request(body, headers)