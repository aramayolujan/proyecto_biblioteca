from fastapi import FastAPI
from rutas import router

app = FastAPI()
app.include_router(router)