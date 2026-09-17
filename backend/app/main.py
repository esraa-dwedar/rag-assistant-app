from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.query import router as api_router
from app.services.retrieval import retrieval_service
from app.services.generation import generation_service
from app.utils.logging_config import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing services during application startup...")
    retrieval_service.initialize()
    generation_service.initialize()
    yield
    logger.info("Application shutdown.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)