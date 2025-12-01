from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f'<Question id={self.id} subject={self.subject!r}>'
