from typing import Annotated, List

import jwt
from fastapi import FastAPI, Request, Form, HTTPException, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import fastapi
import schemas
from auth.security import AuthHandler
from services.anime_service import AnimeServiceFactory, AnimeAlreadyExists
from services.enroll_service import EnrollServiceFactory
from services.user_service import UserServiceFactory, UserDoesNotExist, WrongPassword, UserAlreadyExists, WeakPassword
from svc import schemas as svc_schemas
from svc.myanimelist_service import AnimeServiceFactory as AnimeApiServiceFactory
import typing

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
def check_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    def failure_response_factory(text):
        return templates.TemplateResponse(
            'auth/login.html',
            {"request": request, "error": text}
        )

    user_service = UserServiceFactory.make()
    try:
        user = user_service.login(form_data.username, form_data.password)
    except UserDoesNotExist:
        return failure_response_factory("User does not exist.")
    except WrongPassword:
        return failure_response_factory("Incorrect password.")

    token = auth_handler.create_access_token(user.username)
    resp = RedirectResponse(url='/internal', status_code=303)
    resp.set_cookie(key="access_token", value=token)
    return resp


@app.get("/internal", response_class=HTMLResponse)
async def internal(request: Request):
    return templates.TemplateResponse("internal/internal.html", {"request": request})


@app.get("/logout")
async def logout():
    resp = RedirectResponse(url='/', status_code=303)
    resp.delete_cookie("access_token")
    return resp

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
        "internal/account.html", {
            "request": request,
            "username": user.username,
            "photo": user.icon or None,
            "anime": user.anime
        })


@app.post("/update_account", response_class=HTMLResponse)
async def update_account(request: Request, password: str = Form(...), photo: typing.Optional[UploadFile] = File(...)):
    user_service = UserServiceFactory.make()
    token = request.cookies.get("access_token")

    if token is None:
        return HTMLResponse()
    if photo is None:
        return "photo is none"

    user = get_current_user(token)
    
    def error_response_factory(error: str) -> HTMLResponse:
        resp = templates.TemplateResponse(
            # for debugging user.icon should be '/user_photos/rmol.png'
            "internal/account.html", {
                "request": request,
                "username": user.username,
                "photo": user.icon or None,
                "anime": user.anime,
                "error": error
            })
        
        return resp

    try:
        user_service.update(
            user.username,
            schemas.EditUser(
                icon=None,
                password=password
            )
        )


    except WeakPassword:
        return error_response_factory("Weak password")  # return "Weak password"  # TODO: add template rendering or redirect
    except UserDoesNotExist:
        return error_response_factory("User does not exist")  # return "Weak password"  # TODO: add template rendering or redirect

    token = auth_handler.create_access_token(user.username)
    # return RedirectResponse(
    #     url="/account",
    #     status_code=303
    # )


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
    anime_list = AnimeApiServiceFactory.make()
    anime = anime_list.get_random_anime(limit=10)
    anime_service = AnimeServiceFactory.make()
    for anim in anime:
        try:
            anime_service.add(anim)
        except AnimeAlreadyExists:
            pass
    return anime


class AddAnime(BaseModel):
    mal_id: int


class DeleteAnime(BaseModel):
    mal_id: int


class Search(BaseModel):
    search: str


@app.get("/my_anime_list")
async def my_anime_list(request: Request):
    token = request.cookies.get("access_token")
    if token is None:
        return HTMLResponse()
    user = get_current_user(token)
    return user.anime


@app.post("/add_anime")
async def add_anime(request: Request, add: AddAnime):
    token = request.cookies.get("access_token")

    if token is None:
        return HTMLResponse()

    user = get_current_user(token)
    enrollment_service = EnrollServiceFactory.make()
    enrollment_service.connect(user.username, add.mal_id)

    print(f"Add button clicked on anime {add.mal_id}")
    return {"details": f"{add.mal_id}"}


@app.delete("/delete_anime")
async def delete_anime(request: Request, delete: DeleteAnime):
    token = request.cookies.get("access_token")

    if token is None:
        return HTMLResponse()

    user = get_current_user(token)
    enrollment_service = EnrollServiceFactory.make()
    enrollment_service.disconnect(user.username, delete.mal_id)

    print(f"Delete button clicked on anime {delete.mal_id}")
    return {"details": f"{delete.mal_id}"}


@app.get("/search_page", response_class=HTMLResponse)
async def get_search_page(request: Request):
    return templates.TemplateResponse("internal/search.html", {"request": request})


@app.post("/search")
async def search(request_data: Search) -> List[svc_schemas.Anime]:
    anime_list = AnimeApiServiceFactory.make()
    anime = anime_list.get_anime_by_name(request_data.search)
    anime_service = AnimeServiceFactory.make()
    for anim in anime:
        try:
            anime_service.add(anim)
        except AnimeAlreadyExists:
            pass
    return anime
