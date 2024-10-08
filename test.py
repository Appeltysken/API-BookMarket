import requests

def get_all_users():
    url = "http://127.0.0.1:8000/users-book"
    response = requests.get(url)
    return response.json()

def get_users_with_id(id: int):
    url = "http://127.0.0.1:8000/users-book"
    response = requests.get(url, params={"id": id})
    return response.json()

users = get_all_users()
for i in users:
    print(i)
    
users = get_users_with_id(id = 1)
for i in users:
    print(i)