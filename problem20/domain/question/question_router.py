from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models import Question 
from .schemas import QuestionRead 

router = APIRouter(prefix='/api/question', tags=['questions'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/list', response_model=List[QuestionRead])
def question_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = db.query(Question).order_by(Question.create_date.desc()).offset(skip).limit(limit).all()
    return questions
