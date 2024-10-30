import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from infra.adapter.database import DatabaseConnection
from entrypoint.routes import *

load_dotenv()
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("Application starting...")

connection = DatabaseConnection()

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection.open()
    app.state.connection = connection
    print("database connection successfully opened")
    yield

    connection.close()
    print("database connection successfully closed")


app = FastAPI(lifespan=lifespan)

origins = [
    os.getenv("DASHBOARD_FRONTEND_API_HOST"),
    os.getenv("REPORT_FRONTEND_API_HOST")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("The API is running on port 8000")

app.include_router(accounts_route)
