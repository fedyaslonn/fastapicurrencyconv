from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from converter.routes import converter_router

app = FastAPI(title="Обменник валют")


app.include_router(converter_router)