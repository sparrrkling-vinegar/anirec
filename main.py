from fastapi import FastAPI, Request, Form
from fastapi import UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
import re
from fastapi.staticfiles import StaticFiles
import auth.schemas as auth_schemas
from pydantic import BaseModel

from services.user_service import UserServiceFactory, UserDoesNotExist, WrongPassword, UserAlreadyExists, WeakPassword
from svc.anime import get_anime_by_name, get_random_anime
from svc import schemas as svc_schemas
import schemas

app = FastAPI()
app.mount("/user_photos", StaticFiles(directory="user_photos"), name="user_photos")

templates = Jinja2Templates(directory="templates/")


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
    return RedirectResponse(url='/internal', status_code=303)


@app.get("/signin", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/signin")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user_service = UserServiceFactory.make()

    def failure_response_factory(text: str, status_code: int):
        return templates.TemplateResponse(
            'auth/login.html',
            {"request": request, "error": text},
            status_code=status_code
        )

    try:
        user_service.login(username=username, password=password)
    except UserDoesNotExist:
        return failure_response_factory("User does not exist.", 404)
    except WrongPassword:
        return failure_response_factory("Incorrect password.", 403)
    return RedirectResponse(url='/internal', status_code=303)


@app.get("/internal", response_class=HTMLResponse)
async def internal(request: Request):
    return templates.TemplateResponse("internal/internal.html", {"request": request})


@app.get("/logout")
async def logout():
    return RedirectResponse(url='/', status_code=303)


# TODO: switch to token, do not use path
@app.get("/account/{username}", response_class=HTMLResponse)
async def account(request: Request, username: str):
    user_service = UserServiceFactory.make()

    try:
        user = user_service.get(username=username)
    except UserDoesNotExist:
        return "User does not exist."

    return templates.TemplateResponse(
        # for debugging user.icon should be '/user_photos/rmol.png'
        "internal/account.html", {"request": request, "username": user.username, "photo": user.icon or None})


# TODO: switch to token, do not use path
@app.post("/update_account/{user}")
async def update_account(user: str, username: str = Form(...), photo: UploadFile = File(...)):
    user_service = UserServiceFactory.make()

    try:
        user_service.update(
            user,
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
async def get_page(request: Request):
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
async def get_page(request: Request):
    return templates.TemplateResponse("internal/search.html", {"request": request})


@app.post("/search")
async def search(request_data: Search) -> List[svc_schemas.Anime]:
    return get_anime_by_name(request_data.search)
