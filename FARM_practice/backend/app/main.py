from fastapi import FastAPI
from sqlmodel import SQLModel
from app.core.db import engine
from app.admin_users.model import AdminUser
from app.admin_users.router import router as admin_user_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(admin_user_router)


@app.get("/")
def read_root():
    return {"status": "ok"}
