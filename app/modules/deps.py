from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlmodel import Session

from app.core.db import get_session
from app.core.security import decode_token

from app.modules.auth.interfaces.auth_schema import LoginResponse
from app.modules.usuario.infrastructure.usuario_model import UsuarioModel
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository

security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

DBSession = Annotated[Session, Depends(get_session)]

credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No autorizado",
    headers={"WWW-Authenticate": "Bearer"}
)

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Annotated[Session, Depends(get_session)]) -> UsuarioModel:
    
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise credentials_exc
        
        usuario = UsuarioRepository(db).obtener_por_user_id(user_id)        
        if usuario is None:
            raise credentials_exc

        return usuario
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise credentials_exc

CurrentUser = Annotated[UsuarioModel, Depends(get_current_user)]