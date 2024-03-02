from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from survey_service import SurveyService
import jwt

app = FastAPI()

# Инициализируем SurveyService
survey_service = SurveyService('your-db-uri')  # Укажите вашу строку подключения к БД

# Secret key для подписи JWT
SECRET_KEY = "YourSecretKey"
ALGORITHM = "HS256"


class UserRegistrationRequest(BaseModel):
    username: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: str

class Token(BaseModel):
    access_token: str
    token_type: str



def create_token(self, user_id: int):
   expires_in = timedelta(minutes=30)
   expire = datetime.utcnow() + expires_in
   to_encode = {"sub": user_id, "exp": expire}
   token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return token




# Эндпоинт для регистрации пользователя
@app.post("/register/", response_model=UserResponse)
async def register_user(user_data: UserRegistrationRequest):
    user_id = survey_service.register_user(user_data.username, user_data.email, user_data.password)
    return UserResponse(user_id=user_id, username=user_data.username, email=user_data.email, created_at="")

# Эндпоинт для аутентификации и получения токена
@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: UserLoginRequest):
    user = survey_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = survey_service.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

# Эндпоинты для работы с опросами
@app.post("/surveys/", response_model=int)
async def create_survey(survey_data: dict, current_user: User = Depends(survey_service.get_current_user)):
    survey_data['creator_id'] = current_user.user_id
    survey_id = survey_service.create_survey(survey_data)
    return survey_id

@app.delete("/surveys/{survey_id}/")
async def delete_survey(survey_id: int, current_user: User = Depends(survey_service.get_current_user)):
    survey = survey_service.get_survey(survey_id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey not found")
    if survey.creator_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this survey")
    survey_service.delete_survey(survey_id)
    return {"message": "Survey deleted successfully"}

@app.get("/surveys/{survey_id}/", response_model=dict)
async def get_survey(survey_id: int):
    survey_data = survey_service.get_survey(survey_id)
    if not survey_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey not found")
    return survey_data

@app.get("/surveys/", response_model=list)
async def get_surveys_list():
    return survey_service.get_surveys_list()
