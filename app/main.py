from fastapi import FastAPI
from utils import json_to_dict_list
import os
from typing import Optional
from .models import User

# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к JSON
path_to_json = os.path.join(parent_dir, 'users.json')

app = FastAPI()

@app.get("/")
def main_page():
    return {"message": "This is homepage."}

@app.get("/users-book", response_model=list[User])
def get_all_users():
    users = json_to_dict_list(path_to_json)
    return users
        
@app.get("/users-book/{id}", response_model=User)
def get_user_from_param_id(id: int):
    users = json_to_dict_list(path_to_json)
    for user in users:
        if user["id"] == id:
            return user
    return {"error": "User not found"}, 404
