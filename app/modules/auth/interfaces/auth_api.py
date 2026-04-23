from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.deps import CurrentUser, DBSession
from app.modules.auth.application.auth_service import AuthService
from app.modules.auth.interfaces.auth_schema import LoginRequest, TokenValidationResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(payload: LoginRequest, db: DBSession): 
    return AuthService(db).login(payload.username, payload.password)

@router.get("/token")
def validate_token(current_user: CurrentUser):
    return TokenValidationResponse(
        valid=True,
        usuario={
            "user_id": current_user.user_id,
            "nombre": current_user.nombre,
        }
    )

@router.post("/token")
def token(db: DBSession, form: OAuth2PasswordRequestForm = Depends()):
    username = form.username
    password = form.password
    login_repsonse = AuthService(db).login(username, password)
    return {"access_token": login_repsonse.token, "usuario": login_repsonse.usuario}