import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.diagnostics import router as diagnostics_router
from src.api.v1.characters import router as characters_router

app = FastAPI(title="Shiyotte API", version="1.0.0")

_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnostics_router, prefix="/api/v1")
app.include_router(characters_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
