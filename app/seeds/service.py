import uuid

from pwdlib import PasswordHash
from contextlib import contextmanager
from sqlmodel import Session, select
from typing import Optional

from app.core.db import engine
from app.modules.user.infrastructure.UserModel import UserModel
from app.modules.usuario.infrastructure.UsuarioModel import UsuarioModel
from app.modules.membership.infrastructure.MembershipModel import MembershipModel
from app.modules.permiso.infrastructure.PermisoModel import PermisoModel
from app.seeds.data.permisos import PERMISOS
from app.seeds.data.usuarios import USERS


def hash_password(password: str) -> str:
    return PasswordHash.recommended().hash(password)

@contextmanager
def atomic(db: Session):
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise
   
   
# def get_user_by_username(username: str, db: Session) -> Optional[User]:
#     return db.exec(select(User).where(User.username == username)).first()

def generate_uuid():
    return str(uuid.uuid4())


def seed_usuarios(db: Session) -> None:
    with atomic(db):
        for data in USERS:
            user_id = generate_uuid()
            
            db.add(UserModel(
                user_id=user_id,
                username=data["UserName"]
            ))
            db.commit()
            
            membership = MembershipModel(
                user_id= user_id,
                email=data["Email"],
                password=hash_password(data["Password"])
            )            
            
            usuario = UsuarioModel(
                user_id= user_id,
                nombre=data["Nombre"],
                registrado_por=data["RegistradoPor"]
            )
            
            db.add_all([membership, usuario])
                

def seed_permisos(db: Session) -> None:
    with atomic(db):
        for data in PERMISOS:
            permiso = PermisoModel(
                tracking_id=data["TrackingId"],
                permiso=data["Permiso"],
                registrado_por=data["RegistradoPor"]
            )
            
            db.add(permiso)
            db.commit()


def run_all() -> None:
    with Session(engine) as db:
        seed_usuarios(db)
        print("✅ Usuarios creados")
        seed_permisos(db)
        print("✅ Permisos creados")
        
def run_users() -> None:
    with Session(engine) as db:
        seed_usuarios(db)
        