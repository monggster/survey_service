import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from survey_service import SurveyService

app = FastAPI()
templates = Jinja2Templates(directory="templates")
uri = 'postgresql://localhost/survey_service'
ss = SurveyService(uri)

@app.get("/register", response_class=HTMLResponse)  # Указываем, что возвращается HTML-страница
async def read_root():
    return templates.TemplateResponse("register.html", {})

@app.post("/register", response_class=HTMLResponse)  # Указываем, что возвращается HTML-страница
async def read_root():
    return templates.TemplateResponse("register.html", {"name": "World"})

if __name__ == '__main__':
    uvicorn.run("n:app", host="0.0.0.0", port=8000, reload=True)
