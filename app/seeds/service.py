import uuid

from pwdlib import PasswordHash
from contextlib import contextmanager
from sqlmodel import Session, select
from typing import Optional

from app.core.db import engine
# from app.models.user import User
# from app.models.usuario import Usuario
# from app.models.membership import Membership
from app.modules.permiso.infrastructure.PermisoModel import PermisoModel
from app.seeds.data.permisos import PERMISOS


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


# def seed_users(db: Session) -> None:
#     with atomic(db):
#         for data in USERS:
#             user_id = generate_uuid()
            
#             obj_user = get_user_by_username(data["UserName"], db)
#             if obj_user:
#                 changed = False
                
#                 if obj_user.username != data.get("UserName"):
#                     obj_user.username = data.get("UserName")
#                     changed = True
                    
#                 if changed:
#                     db.add(obj_user)
#             else:
#                 db.add(User(
#                     user_id=user_id,
#                     username=data.get("UserName")
#                 ))
#                 db.commit()
                
#                 db.add(Membership(
#                     user_id= user_id,
#                     email=data["Email"],
#                     password=hash_password(data["Password"])
#                 ))
#                 db.commit()
                
#                 db.add(Usuario(
#                     user_id= user_id,
#                     nombre=data["Nombre"],
#                     registrado_por=data["RegistradoPor"]
#                 ))
#                 db.commit()

def seed_permisos(db: Session) -> None:
    with atomic(db):
        for data in PERMISOS:
            permiso = PermisoModel(
                tracking_id=data.get("TrackingId"),
                permiso=data.get("Permiso"),
                registrado_por=data.get("RegistradoPor")
            )
            
            db.add(permiso)
            db.commit()


def run_all() -> None:
    with Session(engine) as db:
        seed_permisos(db)
        