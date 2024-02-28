from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tables import Base, User, Survey, Question, Choice, SurveyResponse
from collections import defaultdict

class SurveyService:
    def __init__(self, db_uri):
        engine = create_engine(db_uri)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def create_survey(self, survey_data):
        session = self.Session()
        creator_id = survey_data['creator_id']
        survey_name = survey_data['survey_name']
        survey = Survey(user_id=creator_id, survey_name=survey_name, created_at=datetime.now())
        
        # Итерируемся по вопросам словаря и добавляем их в таблицу
        questions_data = survey_data.get('questions', [])
        for question_data in questions_data:
            question_text = question_data.get('question_text')
            question_type = question_data.get('question_type')
            choices_data = question_data.get('choices', [])
            
            question = Question(question_text=question_text, question_type=question_type, survey=survey)
            survey.questions.append(question)
            
            # Итерируемся по вариантам ответов для вопроса и добавляем их в
            # таблицу
            for choice_text in choices_data:
                choice = Choice(choice_text=choice_text, question=question)
                question.choices.append(choice)
        
        session.add(survey)
        session.commit()
        survey_id = survey.survey_id
        session.close()
        return survey_id

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

        if not survey:
            return None

        # Создаем словарь для хранения данных опроса
        survey_data = {
            'survey_id': survey.survey_id,
            'creator_id': survey.user_id,
            'survey_name': survey.survey_name,
            'created_at': survey.created_at,
            'questions': []
        }

        # Итерируемся по вопросам опроса и добавляем их в словарь
        for question in survey.questions:
            question_data = {
                'question_text': question.question_text,
                'question_type': question.question_type,
                'choices': []
            }

            # Итерируемся по вариантам ответов вопроса и добавляем их в словарь
            for choice in question.choices:
                question_data['choices'].append(choice.choice_text)

            survey_data['questions'].append(question_data)

        return survey_data

    def get_survey_statistics(self, survey_id):
        session = self.Session()
        survey = session.query(Survey).get(survey_id)
        session.close()

        if not survey:
            return None

        # Создаем словарь для хранения статистики опроса
        survey_statistics = {
            'survey_id': survey.survey_id,
            'creator_id': survey.user_id,
            'survey_name': survey.survey_name,
            'created_at': survey.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'questions': []
        }

        # Итерируемся по вопросам опроса и добавляем статистику для каждого вопроса
        for question in survey.questions:
            question_statistics = {
                'question_text': question.question_text,
                'question_type': question.question_type,

                # Используем defaultdict(int) для автоматической
                # инициализации счетчиков вариантов ответов
                'choices': defaultdict(int)  
            }

            # Получаем статистику ответов пользователей для данного вопроса
            question_responses = session.query(SurveyResponse.response_text).join(Question).filter(Question.question_id == question.question_id).all()

            # Обновляем статистику для каждого варианта
            # ответа или текстового ответа пользователей
            for response in question_responses:
                question_statistics['choices'][response.response_text] += 1

            survey_statistics['questions'].append(question_statistics)

        return survey_statistics

