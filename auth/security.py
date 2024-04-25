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

    def __init__(self, secret_key: bytes) -> None:
        # 16 bytes is enough for secure signing
        user_repo = user_repository.UserRepository()
        self.user_svc = user_service.UserService(user_repo)
        self.SECRET_KEY = secret_key
    
    # For internal (this package) usage only
    # Used to create jwts
    def create_access_token(self,
        username: str, 
        expires_delta_minutes: datetime.timedelta = ACCESS_TOKEN_EXPIRE_MINUTES
    ) -> str:
        # We call this method if and only if the user is already registered, i.e.
        # we cannot issue the token to the unknown user

        expire = datetime.datetime.now(self.DEFAULT_TIMEZONE) + expires_delta_minutes

        to_encode = {"sub": username, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

