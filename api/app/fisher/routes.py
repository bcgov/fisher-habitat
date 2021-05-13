"""
Map layers (layers module) API endpoints/handlers.
"""
from fastapi import APIRouter, Depends, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.db.utils import get_db

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
