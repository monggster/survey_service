from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .tables import Base, User, Survey, Question, Choice, SurveyResponse

class SurveyService:
    def __init__(self, db_uri):
        engine = create_engine(db_uri)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def create_survey(self, user_id, survey_name):
        session = self.Session()
        survey = Survey(user_id=user_id, survey_name=survey_name, created_at=datetime.now())
        session.add(survey)
        session.commit()
        session.close()
        return survey.survey_id

    def delete_survey(self, survey_id):
        session = self.Session()
        survey = session.query(Survey).get(survey_id)
        if survey:
            session.delete(survey)
            session.commit()
        session.close()

    def get_survey(self, survey_id):
        session = self.Session()
        survey = session.query(Survey).get(survey_id)
        session.close()
        return survey
