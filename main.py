from fastapi import FastAPI, Request, Form
from fastapi import UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import aiofiles
from typing import List
import re
from fastapi.staticfiles import StaticFiles
import auth.schemas as schemas
from pydantic import BaseModel

from svc.anime import get_anime_by_name
from svc import schemas

app = FastAPI()
app.mount("/user_photos", StaticFiles(directory="user_photos"), name="user_photos")

templates = Jinja2Templates(directory="templates/")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def check_password(password: str):
    # Password should at least be 8 characters long, have a number, an uppercase and a lowercase letter,
    # and a special character
    # TODO: for debugging only!
    return True
    return len(password) >= 8 and re.search(r'\d', password) is not None and re.search(r'[A-Z]',
                                                                                       password) is not None and re.search(
        r'[a-z]', password) is not None and re.search(r'\W', password) is not None


@app.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})


@app.post("/signup")
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    # TODO: use this User
    user = schemas.User(username=username, password=password)
    _ = user

    async with aiofiles.open('users.txt', mode='r') as file:
        users = [line.split(":")[0] for line in await file.readlines()]
    if username in users:
        return templates.TemplateResponse('auth/signup.html', {"request": request, "error": "Username already exists."})
    elif not check_password(password):
        return templates.TemplateResponse('auth/signup.html', {"request": request, "error": "Weak password. Password "
                                                                                            "should be at least 8 "
                                                                                            "characters, "
                                                                                            "include uppercase, "
                                                                                            "lowercase, numbers, "
                                                                                            "and a special character."})
    else:
        async with aiofiles.open('users.txt', mode='a') as file:
            await file.write(f'{username}:{password}\n')
        return RedirectResponse(url='/internal', status_code=303)


@app.get("/signin", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/signin")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # TODO: use this User
    user = schemas.User(username=username, password=password)
    _ = user

    async with aiofiles.open('users.txt', mode='r') as file:
        users = [line.strip().split(":") for line in await file.readlines()]
        for user in users:
            if user[0] == username and user[1] == password:
                return RedirectResponse(url='/internal', status_code=303)
    return templates.TemplateResponse('auth/login.html',
                                      {"request": request, "error": "Incorrect username or password."})


@app.get("/internal", response_class=HTMLResponse)
async def internal(request: Request):
    return templates.TemplateResponse("internal/internal.html", {"request": request})


@app.get("/logout")
async def logout():
    return RedirectResponse(url='/', status_code=303)


def get_user_data():
    return "rmol", "/user_photos/rmol.png"


@app.get("/account", response_class=HTMLResponse)
async def account(request: Request):
    username, user_photo_path = get_user_data()
    return templates.TemplateResponse(
        "internal/account.html", {"request": request, "username": username, "photo": user_photo_path or None})


@app.post("/update_account")
async def update_account(username: str = Form(...), photo: UploadFile = File(...)):
    return {
        "status": True,
        "detail": "User account has been updated"
    }


@app.get("/recommendation", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse("internal/recommendation.html", {"request": request})


@app.post("/generate_recommendation")
async def generate_recommendation() -> List[str]:
    recommendations = [f"Recommendation {i}" for i in range(1, 11)]
    return recommendations


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
async def search(request_data: Search) -> List[schemas.Anime]:
    return get_anime_by_name(request_data.search)
