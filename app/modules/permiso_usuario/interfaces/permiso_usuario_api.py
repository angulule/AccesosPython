from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.modules.deps import CurrentUser, DBSession
from app.modules.permiso_usuario.application.permiso_usuario_service import PermisoUsuarioService
from app.modules.permiso_usuario.interfaces.permiso_usuario_schema import PermisoUsuarioRead, PermisoUsuarioCreate, PermisoUsuarioUpdate

router = APIRouter(prefix="/permiso_usuario", tags=["permiso_usuario"])


@router.post("/crear", response_model=PermisoUsuarioRead, status_code=status.HTTP_201_CREATED)
def crear(db: DBSession, payload: PermisoUsuarioCreate, user: CurrentUser):
    return PermisoUsuarioService(db).crear(payload, user.user_id)


@router.put("/actualizar", response_model=PermisoUsuarioRead)
def actualizar(db: DBSession, payload: PermisoUsuarioUpdate, user: CurrentUser):
    return PermisoUsuarioService(db).actualizar(payload, user.user_id)

@router.delete("/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(db: DBSession, tracking_id: str, user: CurrentUser):
    PermisoUsuarioService(db).eliminar(tracking_id, user.user_id)
    return None

@router.get("/obtener_todos", response_model=list[PermisoUsuarioRead])
def obtener_todos(db: DBSession, activo: bool, user: CurrentUser):
    return PermisoUsuarioService(db).obtener_todos(activo)