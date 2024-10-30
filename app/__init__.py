from contextlib import asynccontextmanager
import os
from fastapi import FastAPI

from app.core.db import create_db_and_tables
from app.utils.logger import logger_config
from config.config import settings
from fastapi_pagination import add_pagination

# Router
from app.user.controller import router as user_router
from app.auth.controller import router as login_router
from app.role.controller import router as role_router
from app.operation.controller import router as operation_router


prefix = settings.API_V1_STR
logger = logger_config(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    logger.info("startup: triggered")
    logger.info("http://127.0.0.1:8000/docs")
    yield
    logger.info("shutdown: triggered")


def create_app(settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        lifespan=lifespan,
        description='This document contains the list of API services of the project developed with Python.',

    )
    register_extensions(app)
    register_routes(app)
    register_error_handlers(app)
    return app


def register_extensions(app):
    add_pagination(app)
    logger.info("Registering extensions")


def register_routes(app):
    
    app.include_router(user_router, prefix=prefix)
    app.include_router(login_router, prefix=prefix)
    app.include_router(role_router, prefix=prefix)
    app.include_router(operation_router, prefix=prefix)
    


def register_error_handlers(app):
    ...





