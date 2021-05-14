"""
Main application entrypoint that initializes FastAPI
"""
import time
from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from app.db.session import Session as DBSession
from app.middleware.limit_upload_size import LimitUploadSize
from app.fisher.routes import router

app = FastAPI(title="Fisher Habitat")

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LimitUploadSize, max_upload_size=5_000_000_000)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = DBSession()
    response = await call_next(request)
    request.state.db.close()
    return response

app.include_router(router, prefix="/api/v1")
