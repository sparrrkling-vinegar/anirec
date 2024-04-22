import datetime
import fastapi
import fastapi.security as fastapi_security
import jwt
import os
import passlib.context as passlib_context
import pydantic
import repositories.user_repository as user_repository
import services.user_service as user_service
import typing

class RequiresLoginException(Exception):
    pass

class Token(pydantic.BaseModel):
    access_token: str
    token_type: str

class AuthHandler():
    security = fastapi_security.HTTPBearer()
    pwd_context = passlib_context.CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE_MINUTES = datetime.timedelta(60)
    DEFAULT_TIMEZONE = datetime.UTC
    ALGORITHM = "HS256"
    oauth2_scheme = fastapi_security.OAuth2PasswordBearer(tokenUrl="token")
    user_svc: user_service.UserService

    def __init__(self) -> None:
        # 16 bytes is enough for secure signing
        user_repo = user_repository.UserRepository()
        self.user_svc = user_service.UserService(user_repo)
        self.SECRET_KEY = os.urandom(16)
    
    # For internal (this package) usage only
    # Used to create jwts
    def _create_access_token(self,
        username: str, 
        expires_delta_minutes: datetime.timedelta = ACCESS_TOKEN_EXPIRE_MINUTES
    ) -> str:
        # We call this method if and only if the user is already registered, i.e.
        # we cannot issue the token to the unknown user

        # TODO: probably we do not need this comparison, who knows
        if username != self.user_svc.get(username):
            raise user_service.UserDoesNotExist()
            
        expire = datetime.datetime.now(self.DEFAULT_TIMEZONE) + expires_delta_minutes

        to_encode = {"sub": username, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    # Use this funcion to exchange your token to your username
    def get_current_user(self, token: typing.Annotated[str, fastapi.Depends(oauth2_scheme)]):
        credentials_exception = fastapi.HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithm=self.ALGORITHM)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception
        
        user = self.user_svc.get(username)
        
        if user is None:
            raise credentials_exception

        return user

    # Use this function when you want to get new token and you are already registerd
    def login_for_access_token(
        self,
        form_data: typing.Annotated[fastapi_security.OAuth2PasswordRequestForm, fastapi.Depends()],
    ) -> Token:
        user = self.user_svc.login(form_data.username, form_data.password)
        if not user:
            raise fastapi.HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self._create_access_token(
            username=user.username,
            expires_delta_minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return Token(access_token=access_token, token_type="bearer")
