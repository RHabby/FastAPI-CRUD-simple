from fastapi import FastAPI

from .app import models
from .app.db import engine
from .app.routes import router as user_router


def create_app():
    models.Base.metadata.create_all(bind=engine)

    app = FastAPI()
    app.include_router(user_router)

    return app


app = create_app()
