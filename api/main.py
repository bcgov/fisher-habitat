"""
Main application entrypoint that initializes FastAPI
"""
import time
from fastapi import FastAPI, HTTPException, BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from app.config import DATABASE_URI

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


def bgtask():
    time.sleep(1)


@app.get('/api/v1/hello/{hi}')
def hello_world(hi: str):
    """ function goes here """
    return hi

@app.get('/api/v1/background')
def background(background_tasks: BackgroundTasks):
    background_tasks.add_task(bgtask)
    return {"message": "added background task"}
