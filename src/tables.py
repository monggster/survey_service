from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime)

    responses = relationship('SurveyResponse',
                             back_populates='respondent', overlaps="responses")

class Survey(Base):
    __tablename__ = 'surveys'

    survey_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    survey_name = Column(String)
    created_at = Column(DateTime)

    # При удалении опроса, каскадно удаляются все связанные с ним вопросы
    questions = relationship('Question', cascade='all, delete', back_populates='survey')
    responses = relationship('SurveyResponse', cascade='all, delete', back_populates='survey')

class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    survey_id = Column(Integer, ForeignKey('surveys.survey_id'))
    question_text = Column(String)

    # 1 - вопрос с одним вариантом,
    # 2 - вопрос с множеством вариантов,
    # 3 - вопрос без вариантов
    question_type = Column(Integer) 

    survey = relationship('Survey', back_populates='questions')
    choices = relationship('Choice', cascade='all, delete', back_populates='question')

class Choice(Base):
    __tablename__ = 'choices'

    choice_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    choice_text = Column(String)

    question = relationship('Question', back_populates='choices')

class SurveyResponse(Base):
    __tablename__ = 'survey_responses'

    survey_response_id = Column(Integer, primary_key=True, autoincrement=True)
    survey_id = Column(Integer, ForeignKey('surveys.survey_id'))
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    user_id = Column(Integer, ForeignKey('users.user_id')) 
    response_text = Column(String)
    responded_at = Column(DateTime)

    survey = relationship('Survey', back_populates='responses')
    question = relationship('Question')
    respondent = relationship('User', overlaps='responses')
