from fastapi import FastAPI
from utils import json_to_dict_list
import os
from typing import Optional

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

@app.get("/users-book")
def get_all_users(id: Optional[int] = None):
    users = json_to_dict_list(path_to_json)
    if id is None:
        return users
    else:
        return_list = []
        for user in users:
            if user["id"] == id:
                return_list.append(user)
        return return_list