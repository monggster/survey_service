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

Методы класса SurveyService:
- `create_survey`
- `delete_survey`
- `get_survey`
- `get_survey_statistics`

- `get_surveys_list` (с количеством вопросов в каждом опросе)

- `create_user`
- `delete_user`
- `validate_user`

- `upload_survey_response`

- `get_surveys_by_creator`
- `get_creator_by_survey`


`create_survey`(id опроса(авто), id создателя, имя опроса, время создания(авто), [набор вопросов, набор ответов к каждому вопросу])


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


```
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


`create_question`(id вопроса(авто), id опроса, текст вопроса, набор ответов)

`create_choice`(id варианта(авто), id вопроса, текст варианта)

`delete_survey`(id опроса)

















