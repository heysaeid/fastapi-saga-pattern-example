from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_all_tables


async def start_application() -> None:
    await create_all_tables()


async def down_application() -> None:
    ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_application()

    yield

    await down_application()
