"""
Map layers (layers module) API endpoints/handlers.
"""
from fastapi import FastAPI, HTTPException, APIRouter, BackgroundTasks, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.db.utils import get_db

from app.config import DATABASE_URI
from fastapi.encoders import jsonable_encoder
import os 

router = APIRouter()

def bgtask():
    time.sleep(1)

@router.get('/hello/{hi}')
def hello_world(hi: str):
    """ function goes here """
    return hi

@router.get('/background')
def background(background_tasks: BackgroundTasks):
    background_tasks.add_task(bgtask)
    return {"message": "added background task"}


@router.get('/dbexample')
def dbexample(db: Session = Depends(get_db)):
    """ function goes here """

    q = """
    select 42
    """

    result = db.execute(q)
    result = result.fetchone()[0]

    return result

@router.post("/create_file/")
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