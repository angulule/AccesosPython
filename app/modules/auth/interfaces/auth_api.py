from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.deps import DBSession
from app.modules.auth.application.auth_service import AuthService
from app.modules.auth.interfaces.auth_schema import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(payload: LoginRequest, db: DBSession): 
    return AuthService(db).login(payload.username, payload.password)

@router.post("/token")
def token(db: DBSession, form: OAuth2PasswordRequestForm = Depends()):
    email = form.username
    password = form.password
    loginResponse = AuthService(db).login(email, password)
    return {"access_token": loginResponse.token, "token_type": "bearer"}