from fastapi import FastAPI

from app.api import api
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, docs_url="/")

app.include_router(api.router, prefix=settings.API_V1_STR)