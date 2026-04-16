import uuid

from fastapi import HTTPException
from sqlmodel import Session
from datetime import datetime, timezone

from app.core.security import create_access_token, hash_password, verify_password
from app.modules.user.infrastructure.UserModel import UserModel
from app.modules.membership.infrastructure.MembershipModel import MembershipModel
from app.modules.usuario.infrastructure.UsuarioModel import UsuarioModel
from app.modules.usuario.interfaces.usuario_schema import UsuarioRead
from app.modules.auth.interfaces.auth_schema import LoginResponse

from app.modules.user.infrastructure.user_repository import UserRepository
from app.modules.membership.infrastructure.membership_repository import MembershipRepository
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository
    
class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.userRepo = UserRepository(db)
        self.membershipRepo = MembershipRepository(db)
        self.usuarioRepo = UsuarioRepository(db)
        
    def login(self, username: str, password: str) -> LoginResponse:
        user = self.userRepo.obtener_por_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
            
        membership = self.membershipRepo.obtener_por_user_id(user.user_id)
        
        if not user or not verify_password(password[:72], membership.password):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        token = create_access_token({
            "sub": str(user.user_id),
            "username": user.username
        })
        
        usuario = self.usuarioRepo.obtener_por_user_id(user.user_id)
        
        login_response = LoginResponse (
            token=token,
            token_type="bearer",
            usuario=UsuarioRead (
                user_id=usuario.user_id,
                nombre=usuario.nombre,
                email=membership.email
            )
        )
        
        return login_response

    # def register(self, payload: UsuarioCreate) -> UsuarioRead:
    #     if self.userRepo.obtener_por_username(payload.username):
    #         raise HTTPException(status_code=400, detail="El nombre de usaurio ya se encuentra registrado.")
        
    #     user = UserModel(
    #         user_id=str(uuid.uuid4()),
    #         username=payload.username
    #     )
        
    #     user = self.userRepo.crear(user)
        
    #     membership = MembershipModel(
    #         user_id=user.user_id,
    #         email=payload.email, 
    #         password=hash_password(payload.password[:72])
    #     )
        
    #     membership = self.membershipRepo.crear(membership)
        
    #     usuario = UsuarioModel(
    #         user_id=user.user_id,
    #         nombre=payload.nombre,
    #         registrado_por=1
    #     )
        
    #     usuario = self.usuarioRepo.crear(usuario)
        
    #     userRead = UsuarioRead(username=user.username, nombre=payload.nombre, email=membership.email)
    #     return userRead

    