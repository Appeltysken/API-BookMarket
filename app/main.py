from fastapi import FastAPI
import os
from app.users.router import router as router_users
from app.orders.router import router as router_orders

app = FastAPI()

@app.get("/")
def main_page():
    return {"message": "This is homepage."}

app.include_router(router_users)
app.include_router(router_orders)