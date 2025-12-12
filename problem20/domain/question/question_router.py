import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Question
from domain.question import question_schema

router = APIRouter(
    prefix='/api/question',
    tags=['questions']
)

@router.get('/list', response_model=List[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list

@router.post('/create', status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db)):
    question = Question(subject=_question_create.subject,
                        content=_question_create.content,
                        create_date=datetime.datetime.now())
    db.add(question)
    db.commit()