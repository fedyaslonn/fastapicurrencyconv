from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel
from converter.routes import converter_router
from users.routes import users_router
import uvicorn

app = FastAPI(title="Обменник валют")


app.include_router(converter_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)