from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models import Question
from .schemas import QuestionCreate, QuestionRead, QuestionUpdate

router = APIRouter(prefix='/questions', tags=['questions'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/', response_model=List[QuestionRead])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = db.query(Question).order_by(Question.create_date.desc()).offset(skip).limit(limit).all()
    return questions


@router.get('/{question_id}', response_model=QuestionRead)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')
    return question


@router.post('/', response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    question = Question(subject=payload.subject, content=payload.content)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.put('/{question_id}', response_model=QuestionRead)
def update_question(question_id: int, payload: QuestionUpdate, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')
    if payload.subject is not None:
        question.subject = payload.subject
    if payload.content is not None:
        question.content = payload.content
    db.commit()
    db.refresh(question)
    return question


@router.delete('/{question_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')
    db.delete(question)
    db.commit()
    return None
