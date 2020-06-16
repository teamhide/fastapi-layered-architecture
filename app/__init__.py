from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pythondi import Provider, configure

from app.users.repositories import UserRepo, UserMySQLRepo
from app.users.views.v1 import user_router
from core.config import get_config
from core.db import session
from core.exception import CustomException


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(user_router, prefix='/api/v1', tags=['User'])


def init_listeners(app: FastAPI) -> None:
    # Exception handler
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content=exc.kwargs,
        )

    # Middleware for SQLAlchemy session
    @app.middleware('http')
    async def remove_session(request: Request, call_next):
        response = await call_next(request)
        session.remove()
        return response


def init_di() -> None:
    provider = Provider()
    provider.bind(UserRepo, UserMySQLRepo)
    configure(provider=provider)


def create_app() -> FastAPI:
    app = FastAPI(
        title='Hide',
        description='Hide API',
        version='1.0.0',
        docs_url=None if get_config().ENV == 'production' else '/docs',
        redoc_url=None if get_config().ENV == 'production' else '/redoc',
    )
    init_routers(app=app)
    init_cors(app=app)
    init_listeners(app=app)
    init_di()
    return app


app = create_app()
