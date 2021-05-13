"""
Main application entrypoint that initializes FastAPI
"""
import time
from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from starlette.middleware.cors import CORSMiddleware
from app.config import DATABASE_URI
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
import os 
from app.middleware.limit_upload_size import LimitUploadSize

from typing import List

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
app.add_middleware(LimitUploadSize, max_upload_size=50_000_000)

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

@app.post("/create_file/")
async def upload_file(shape: UploadFile = File(...)):
    print(shape.file)
    try:
        os.mkdir("shapes")
        print(os.getcwd())
    except Exception as e:
        print(e) 
    file_name = os.getcwd()+"/shapes/"+shape.filename.replace(" ", "-")
    with open(file_name,'wb+') as f:
        f.write(shape.file.read())
        f.close()
    
    file = jsonable_encoder({"imagePath":file_name})
    return {"filename": file_name}