import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from entrypoint.routes import *
from infra.adapter.database import DatabaseFactory

load_dotenv()
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("Application starting...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    with DatabaseFactory().create_postgres_connection() as connection:
        app.state.connection = connection
        print("database connection successfully opened")
        yield

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

app.include_router(accounts_route)

print("The API is running on port 8000")
