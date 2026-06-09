from fastapi import FastAPI

from app.api.routes.logs import router as logs_router
from app.core.config import settings


app = FastAPI(
    title="Observability Query API"
)


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(logs_router)
