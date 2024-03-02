from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tables import Base, User, Survey, Question, Choice, SurveyResponse
from collections import defaultdict
from passlib.context import CryptContext

class SurveyService:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def authenticate_user(self, username: str, password: str):
        session = self.Session()
        user = session.query(User).filter(User.username == username).first()
        session.close()
        if not user:
            return False
        if not self.__verify_password(password, user.password):
            return False
        return user

    def register_user(self, user_data):
        session = self.Session()
        username = user_data['username']
        email = user_data['email']
        hashed_password = self.__get_password_hash(user_data['password'])
        user = User(
                    username=username,
                    email=email,
                    password=hashed_password,
                    created_at=datetime.now()
                    )
        session.add(user)
        user_id = user.user_id
        session.commit()
        session.close()
        return user_id


    def __verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def __get_password_hash(self, password):
        return self.pwd_context.hash(password)

    
    def create_survey(self, survey_data):
        session = self.Session()
        creator_id = survey_data['creator_id']
        survey_name = survey_data['survey_name']
        survey = Survey(
                        user_id=creator_id,
                        survey_name=survey_name,
                        created_at=datetime.now()
                        )
        
        # Итерируемся по вопросам словаря и добавляем их в таблицу
        questions_data = survey_data.get('questions', [])
        for question_data in questions_data:
            question_text = question_data.get('question_text')
            question_type = question_data.get('question_type')
            choices_data = question_data.get('choices', [])
            
            question = Question(
                            question_text=question_text,
                            question_type=question_type,
                            survey=survey
                            )

            survey.questions.append(question)
            
            # Итерируемся по вариантам ответов для вопроса и добавляем их в
            # таблицу
            for choice_text in choices_data:
                choice = Choice(
                                choice_text=choice_text,
                                question=question
                                )
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

        if not survey:
            session.close()
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

            # Итерируемся по вариантам ответов вопроса
            # и добавляем их в словарь
            for choice in question.choices:
                question_data['choices'].append(choice.choice_text)

            survey_data['questions'].append(question_data)

        session.close()
        return survey_data

    def get_survey_statistics(self, survey_id):
        session = self.Session()
        survey = session.query(Survey).get(survey_id)

        if not survey:
            session.close()
            return None

        # Создаем словарь для хранения статистики опроса
        survey_statistics = {
            'survey_id': survey.survey_id,
            'creator_id': survey.user_id,
            'survey_name': survey.survey_name,
            'created_at': survey.created_at.strftime('%H:%M %d/%m/%Y'),
            'questions': []
        }

        # Итерируемся по вопросам опроса и добавляем
        # статистику для каждого вопроса
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

        session.close()
        return survey_statistics


    def get_surveys_list(self):
        session = self.Session()
        surveys = session.query(Survey).all()

        surveys_list = []

        for survey in surveys:
            survey_data = {
                'survey_id': survey.survey_id,
                'creator_id': survey.user_id,
                'survey_name': survey.survey_name,
                'created_at': survey.created_at.strftime('%H:%M %d/%m/%Y')
            }
            # Получаем количество вопросов в опросе
            survey_data['question_count'] = len(survey.questions)
            surveys_list.append(survey_data)

        session.close()
        return surveys_list


    def delete_user(self, user_id):
        session = self.Session()
        user = session.query(User).get(user_id)
        if user:
            session.delete(user)
            session.commit()
        session.close()

    def get_user(self, user_id):
        session = self.Session()
        user = session.query(User).get(user_id)
        if not user:
            session.close()
            return None

        user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'created_at': user.created_at.strftime('%H:%M %d/%m/%Y'),
        }

        session.close()
        return user_data


    def upload_responses(self, responses_data):
        session = self.Session()
        responses = responses_data['responses']
        survey_id = responses_data['survey_id']
        user_id = responses_data['user_id']
        responded_at = datetime.now()


        for response in responses:
            question_id = response['question_id']
            response_text = response['response_text']
            
            survey_response = SurveyResponse(
                            survey_id=survey_id,
                            question_id=question_id,
                            user_id=user_id,
                            response_text=response_text,
                            responded_at=responded_at
                            )

            session.add(survey_response);
            
        session.commit()
        session.close()






