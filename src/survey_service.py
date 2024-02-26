from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .tables import Base, User, Survey, Question, Choice, SurveyResponse

class SurveyService:
    def __init__(self, db_uri):
        engine = create_engine(db_uri)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

