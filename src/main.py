from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel
from converter.routes import converter_router
from users.routes import users_router

app = FastAPI(title="Обменник валют")


app.include_router(converter_router)
app.include_router(users_router)