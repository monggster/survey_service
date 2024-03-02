Пользователь может создавать и проходить опросы.
Смотреть статистику ответов и удалять свои опросы.

Чтобы пройти или создать опрос, нужно зарегестрироваться.
Статистика видна всем, но она анонимна. То есть не содержит данных о том какой пользователь что ответил. Только варианты ответов и число, означающее сколько раз был выбран данный вариант.
Изменить опрос, вопрос, вариант ответа или сам ответ нельзя.
В будущем это можно будет изменить.

Опрос состоит из множества вопросов. Каждый вопрос может быть 3-х типов: 
- С одним вариантом ответа.
- С множеством вариантов ответа.
- Текст ответа вводит респондент.

На главной странице будет предложена регистрация/вход + список существующих опросов.
Если пользователь авторизирован, он может создать или удалить свой опрос, а так же к любому опросу можно посмотреть статистику.


Создание базы данных:
`CREATE DATABASE survey_service;`

Даем права на управление базой данных:
`ALTER DATABASE "survey_service" OWNER TO user;`


Python зависимости



Подробное описание методов класса SurveyService:

-----------------
- `create_survey`
Принимает:
```
# структура словаря, содержащего все необходимые данные, чтобы создать новый опрос
survey_data = {
    'creator_id': creator_id,
    'survey_name': survey_name,
    'questions': [
        {
            'question_text': question_text,
            'question_type': question_type,
            'choices': [choice1, choice2, ...]
        },
        ...
    ]
}
```
Возвращает: `survey_id`

-----------------
- `delete_survey`
Принимает: `survey_id`
Возвращает: `None` 

-----------------
- `get_survey`
Принимает: `survey_id`
Возвращает:
```
# структура словаря, содержащего данные о существующем опросе
survey_data = {
    'survey_id': survey_id,
    'creator_id': user_id,
    'survey_name': survey_name,
    'created_at': created_at,
    'questions': [
        {
            'question_text': question_text,
            'question_type': question_type,
            'choices': [choice1, choice2, ...]
        },
        ...
    ]
}
```

-----------------
- `get_survey_statistics`
Принимает: `survey_id`
Возвращает:
```
# структура словаря, содержащего статистику опроса
survey_statistics = {
    'survey_id': survey_id,
    'creator_id': user_id,
    'survey_name': survey_name,
    'created_at': created_at,
    'questions': [
        {
            'question_text': question_text,
            'question_type': question_type,
            'choices': [
                {
                    'response_text1': num1,
                    'response_text2': num2,
                    ...
                }
            ]
        },
        ...
    ]
```

-----------------
- `get_surveys_list` (с количеством вопросов в каждом опросе)
Принимает: `None`
Возвращает:
```
# структура списка, содержащего общие данные о каждом опросе
surveys_list = [
    {
        'survey_id': survey_id,
        'creator_id': user_id,
        'survey_name': survey_name,
        'created_at': created_at,
        'question_count': question_count
    },
    ...
]
```

-----------------
- `create_user`
Принимает:
```
# структура словаря, содержащего все необходимые данные, чтобы создать нового пользователя
user_data = {
    'username': username,
    'email': email,
    'password': password,
}
```
Возвращает: `user_id`

-----------------
- `delete_user`
Принимает: `user_id`
Возвращает: `None` 

-----------------
- `get_user`
Принимает: `user_id`
Возвращает:
```
# структура словаря, содержащего все данные о пользователе
user_data = {
    'user_id': user_id,
    'username': username,
    'email': email,
    'password': password,
    'created_at': created_at,
}
```

-----------------
- `validate_user`

-----------------
- `upload_responses`
Принимает: 
```
responses_data = {
    'survey_id': survey_id,
    'user_id': user_id,
    'responses': [
        {
            'question_id': question_id,
            'response_text': response_text,
        }
        ...
    ]
}
```
Возвращает: `None` 

-----------------
- `get_surveys_by_creator`

-----------------
- `get_creator_by_survey`

-----------------




