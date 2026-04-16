from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.base import router as base_router
from .infrastructure.sqlite.database import database
from .infrastructure.sqlite.models import User  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()

    yield


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base_router, prefix="/base", tags=["Base APIs"])

    return app
