from fastapi import FastAPI
import os
from app.entities.users.router import router as router_users
from app.entities.orders.router import router as router_orders
from app.entities.roles.router import router as router_roles
from app.entities.roles.models import init_roles

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_roles()

@app.get("/", summary="Основная страница")
def main_page():
    return {"message": "This is homepage."}

app.include_router(router_users)
app.include_router(router_orders)
app.include_router(router_roles)