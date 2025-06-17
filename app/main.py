# main.py
from fastapi import FastAPI

from app.controller.MockController import router as mock_router
from app.db import init_db


app = FastAPI()
init_db()
app = FastAPI()
app.include_router(mock_router, prefix="", tags=["Mock"])
