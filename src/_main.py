from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from survey_service import SurveyService

database_uri = "postgresql://localhost/survey_service"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
survey_service = SurveyService(db_uri=database_uri)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    surveys = survey_service.get_surveys()
    return templates.TemplateResponse("index.html", {"request": request, "surveys": surveys})

@app.get("/surveys/create", response_class=HTMLResponse)
def create_survey(request: Request):
    return templates.TemplateResponse("create_survey.html", {"request": request})

@app.post("/surveys")
async def create_survey(request: Request):
    # Валидация формы необходима здесь

    form = await request.form()
    question_texts = form.getlist("question_text")
    choice_texts_list = [form.getlist(f"choice_texts_{i}") for i in range(len(question_texts))]
    survey_service.create_survey(user_id=1, survey_name=form["survey_name"], question_texts=question_texts, choice_texts_list=choice_texts_list)
    return {"message": "Survey created successfully!"}

@app.put("/surveys/{survey_id}")
async def update_survey(request: Request, survey_id: int):
    form = await request.form()
    question_texts = form.getlist("question_text")
    choice_texts_list = [form.getlist(f"choice_texts_{i}") for i in range(len(question_texts))]
    survey_service.update_survey(survey_id=survey_id, survey_name=form["survey_name"], question_texts=question_texts, choice_texts_list=choice_texts_list)
    return {"message": "Survey updated successfully!"}

@app.get("/surveys/{survey_id}", response_class=HTMLResponse)
def get_survey(request: Request, survey_id: int):
    survey = survey_service.get_survey(survey_id=survey_id)
    return templates.TemplateResponse("survey.html", {"request": request, "survey": survey})

@app.get("/surveys/{survey_id}/responses", response_class=HTMLResponse)
def get_survey_responses(request: Request, survey_id: int):
    responses = survey_service.get_survey_responses(survey_id=survey_id)
    return templates.TemplateResponse("responses.html", {"request": request, "responses": responses})

