from tables import *
from survey_service import SurveyService
from json import dumps

new_user = {

        'username': 'Matvey',
        'email': 'monggster@yandex.ru',
        'password': 'passwd1'
}

new_survey = {
        'creator_id': 2,
        'survey_name': 'survey1',
        'questions': [
            {
                'question_text': 'quest_text1',
                'question_type': 1,
                'choices': [ 'choice1', 'choice2' ]
            },
            {
                'question_text': 'quest_text2',
                'question_type': 1,
                'choices': [ 'choice1', 'choice2' ]
            },
            {
                'question_text': 'quest_text3',
                'question_type': 2,
                'choices': [ 'choice1', 'choice2' ]
            },
        ]
}

new_responses = {
        'survey_id': 2,
        'user_id': 2,
        'responses': [
            {
                'question_id': 1,
                'response_text': 'choice2',
            },
            {
                'question_id': 2,
                'response_text': 'choice2',
            },
            {
                'question_id': 3,
                'response_text': 'choice2',
            },
        ]
}

def main():
    uri = 'postgresql://localhost/survey_service'
    ss = SurveyService(uri)
    print(dumps(ss.get_user(2), indent=2))


if __name__ == '__main__':
    main()
