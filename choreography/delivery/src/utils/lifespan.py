from contextlib import asynccontextmanager

from fastapi import FastAPI




async def start_application() -> None:
    ...


async def down_application() -> None:
    ...


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_application()

    yield

    await down_application()
