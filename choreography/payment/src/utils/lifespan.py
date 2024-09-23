from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.stream import app as stream_app
from database import create_all_tables


async def start_application() -> None:
    await create_all_tables()
    await stream_app.start()


async def down_application() -> None:
    await stream_app.stop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_application()

    yield

    await down_application()
