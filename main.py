from auth.security import AuthHandler
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi import UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from services.user_service import UserServiceFactory, UserDoesNotExist, WrongPassword, UserAlreadyExists, WeakPassword
from svc import schemas as svc_schemas
from svc.anime import get_anime_by_name, get_random_anime
from typing import Annotated
from typing import List
import jwt
import schemas


app = FastAPI()
app.mount("/user_photos", StaticFiles(directory="user_photos"), name="user_photos")

templates = Jinja2Templates(directory="templates/")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

secret_key = b"111111111111111111111111"
auth_handler = AuthHandler(secret_key)

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})


@app.post("/signup")
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    user_service = UserServiceFactory.make()

    def failure_response_factory(text: str, status_code: int) -> templates.TemplateResponse:
        return templates.TemplateResponse(
            'auth/signup.html',
            {"request": request, "error": text},
            status_code=status_code
        )

    try:
        user_service.register(
            schemas.CreateUser(
                username=username,
                password=password,
                icon=None  # TODO: add icon
            )
        )
    except UserAlreadyExists:
        return failure_response_factory(f"Username already exists.", 400)
    except WeakPassword:
        return failure_response_factory(
            "Weak password. Password "
            "should be at least 8 "
            "characters, "
            "include uppercase, "
            "lowercase, numbers, "
            "and a special character.",
            400
        )

    token = auth_handler.create_access_token(username)
    resp = RedirectResponse(url='/internal', status_code=303)
    resp.set_cookie(key="access_token", value=token)
    return resp


@app.get("/signin", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


# Use this funcion to exchange your token to your username
def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth_handler.decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user_service = UserServiceFactory.make()
    user = user_service.get(username)
    
    if user is None:
        raise credentials_exception

    return user

# Use this function when you want to get new token and you are already registerd
@app.post("/signin")
def check_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_service = UserServiceFactory.make()
    try:
        print(form_data.username, form_data.password)

        user = user_service.login(form_data.username, form_data.password)
    except UserDoesNotExist or WrongPassword:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = auth_handler.create_access_token(user.username)
    resp = RedirectResponse(url='/internal', status_code=303)
    resp.set_cookie(key="access_token", value=token)
    return resp


@app.get("/internal", response_class=HTMLResponse)
async def internal(request: Request):
    return templates.TemplateResponse("internal/internal.html", {"request": request})


@app.get("/logout")
async def logout():
    return RedirectResponse(url='/', status_code=303)


@app.get("/account", response_class=HTMLResponse)
async def account(request: Request):
    user_service = UserServiceFactory.make()

    token = request.cookies.get("access_token")

    if token is None:
        return HTMLResponse()

    user = get_current_user(token)

    try:
        user = user_service.get(username=user.username)
    except UserDoesNotExist:
        return "User does not exist."

    return templates.TemplateResponse(
        # for debugging user.icon should be '/user_photos/rmol.png'
        "internal/account.html", {"request": request, "username": user.username, "photo": user.icon or None})


@app.post("/update_account")
async def update_account(request: Request, username: str = Form(...), photo: UploadFile = File(...)):
    user_service = UserServiceFactory.make()

    token = request.cookies.get("access_token")

    if token is None:
        return HTMLResponse()

    user = get_current_user(token)

    try:
        user_service.update(
            user.username,
            schemas.EditUser(
                username=username,
                icon=None,
                password=None  # TODO: implement front for password change
            )
        )
    except WeakPassword:
        return "Weak password"  # TODO: add template rendering or redirect
    except UserDoesNotExist:
        return "User does not"  # TODO: add template rendering or redirect
    return {
        "status": True,
        "detail": "User account has been updated"
    }


@app.get("/recommendation", response_class=HTMLResponse)
async def get_recommendation(request: Request):
    user_service = UserServiceFactory.make()

    token = request.cookies.get("access_token")

    if token is None:
        return HTMLResponse()

    user = get_current_user(token)
    return templates.TemplateResponse("internal/recommendation.html", {"request": request})


@app.post("/generate_recommendation")
async def generate_recommendation() -> List[svc_schemas.Anime]:
    return get_random_anime(limit=10)


class Nice(BaseModel):
    index: int


class Search(BaseModel):
    search: str


@app.post("/nice_anime")
async def post_nice(nice: Nice):
    print(f"Nice button clicked on anime {nice.index}")
    return {}


texts = [f"Text {i}" for i in range(10)]


@app.get("/search_page", response_class=HTMLResponse)
async def get_search_page(request: Request):
    return templates.TemplateResponse("internal/search.html", {"request": request})


@app.post("/search")
async def search(request_data: Search) -> List[svc_schemas.Anime]:
    return get_anime_by_name(request_data.search)


