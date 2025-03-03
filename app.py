from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes.auth_route import auth_router

load_dotenv()

app = FastAPI(root_path="/api")

app.include_router(auth_router)