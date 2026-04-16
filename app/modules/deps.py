

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlmodel import Session

from app.core.db import get_session
from app.core.security import decode_token

from app.modules.user.infrastructure.UserModel import UserModel
from app.modules.user.infrastructure.user_repository import UserRepository

security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

DBSession = Annotated[Session, Depends(get_session)]

credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No autorizado",
    headers={"WWW-Authenticate": "Bearer"}
)

# def get_current_user(
#     credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
#     db: Annotated[Session, Depends(get_session)]) -> UserModel:
    
#     token = credentials.credentials

#     try:
#         payload = decode_token(token)
#         user_id = payload.get("sub")
        
#         if not user_id:
#             raise credentials_exc
#     except Exception:
#         raise credentials_exc

#     user = UserRepository(db).obtener_por_user_id(user_id)
#     if not user:
#         raise credentials_exc

#     return user

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Annotated[Session, Depends(get_session)]) -> UserModel:
    
    #token = credentials.credentials

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        
        print(user_id)
        
        if not user_id:
            raise credentials_exc
    except Exception:
        raise credentials_exc

    user = UserRepository(db).obtener_por_user_id(user_id)
    if not user:
        raise credentials_exc

    return user

CurrentUser = Annotated[UserModel, Depends(get_current_user)]