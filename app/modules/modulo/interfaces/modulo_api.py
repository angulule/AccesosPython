from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.modules.deps import DBSession, get_current_user, CurrentUser
from app.modules.modulo.application.modulo_service import ModuloService
from app.modules.modulo.interfaces.modulo_schema import ModuloRead

router = APIRouter(prefix="/modulo", tags=["modulo"])


@router.post("/crear", response_model=ModuloRead, status_code=status.HTTP_201_CREATED)
def crear(nombre: str, db: DBSession, user: CurrentUser):
    return ModuloService(db).crear(nombre, user.user_id)

@router.put("/actualizar", response_model=ModuloRead)
def actualizar(tracking_id: str, nombre: str, db: DBSession, user: CurrentUser):
    print(user)
    return ModuloService(db).actualizar(tracking_id, nombre, user.user_id)

@router.put("/eliminar")
def eliminar(tracking_id: str, db: DBSession, user: CurrentUser):
    ModuloService(db).eliminar(tracking_id, user.user_id)
    return None

@router.get("/obtener_todos", response_model=list[ModuloRead])
def obtener_todos(activo: bool, db: DBSession, user: CurrentUser):
    return ModuloService(db).obtener_todos(activo)


@router.get("/obtener_por_tracking_id", response_model=ModuloRead)
def obtener_por_tracking_id(tracking_id: str, db: DBSession, user: CurrentUser):
    return ModuloService(db).obtener_por_tracking_id(tracking_id)
