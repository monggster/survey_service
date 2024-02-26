from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .tables import Base, User, Survey, Question, Choice, SurveyResponse

class SurveyService:
    def __init__(self, db_uri):
        engine = create_engine(db_uri)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def create_survey(self, user_id, survey_name, question_texts, choice_texts_list):
        session = self.Session()
        survey = Survey(user_id=user_id, survey_name=survey_name, created_at=datetime.now())

        for question_text, choice_texts in zip(question_texts, choice_texts_list):
            question = Question(survey=survey, question_text=question_text)
            for choice_text in choice_texts:
                choice = Choice(question=question, choice_text=choice_text)
                session.add(choice)

        session.add(survey)
        session.commit()
        session.close()

    def update_survey(self, survey_id, survey_name, question_texts, choice_texts_list):
        session = self.Session()
        survey = session.query(Survey).get(survey_id)

        if not survey:
            session.close()
            return

        survey.survey_name = survey_name

        # Редактирование вопросов и вариантов ответов опроса
        existing_question_ids = []
        for question_text, choice_texts in zip(question_texts, choice_texts_list):
            # Поиск существующего вопроса или создание нового
            question = session.query(Question).filter_by(survey_id=survey_id, question_text=question_text).first()
            if question:
                question.choices.clear()
            else:
                question = Question(survey_id=survey_id, question_text=question_text)
                session.add(question)
            
            existing_question_ids.append(question.question_id)

            # Создание или обновление вариантов ответов
            for choice_text in choice_texts:
                choice = Choice(question=question, choice_text=choice_text)
                session.add(choice)
        
        # Удаление вопросов, которых уже нет в обновленном списке
        session.query(Question).filter(Question.survey_id == survey_id, ~Question.question_id.in_(existing_question_ids)).delete(synchronize_session=False)

        session.commit()
        session.close()

    def delete_survey(self, survey_id):
        session = self.Session()
        session.query(Survey).filter_by(survey_id=survey_id).delete()
        session.commit()
        session.close()

    def get_survey(self, survey_id):
        session = self.Session()
        survey = session.query(Survey).get(survey_id)
        session.close()
        return survey

    def get_survey_responses(self, survey_id):
        session = self.Session()
        responses = session.query(SurveyResponse).filter_by(survey_id=survey_id).all()
        session.close()
        return responses
    
    def get_survey_statistics(self, survey_id):
        session = self.Session()

        # Подсчет общего количества ответов на опрос
        total_responses = session.query(func.count(SurveyResponse.respondent_id)) \
                                .filter_by(survey_id=survey_id) \
                                .scalar()

        # Подсчет количества ответов для каждого варианта ответа

