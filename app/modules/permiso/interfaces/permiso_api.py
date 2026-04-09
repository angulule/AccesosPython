from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.modules.deps import DBSession
from app.modules.permiso.application.permiso_service import PermisoService
from app.modules.permiso.interfaces.permiso_schema import PermisoRead

router = APIRouter(prefix="/permiso", tags=["permiso"])


@router.post("/crear", response_model=PermisoRead, status_code=status.HTTP_201_CREATED)
def crear(db: DBSession, nombre: str):
    return PermisoService(db).crear(nombre)

@router.put("/actualizar", response_model=PermisoRead)
def actualizar(db: DBSession, tracking_id: str, nombre: str):
    return PermisoService(db).actualizar(tracking_id, nombre)

@router.put("/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(db: DBSession, tracking_id: str):
    PermisoService(db).eliminar(tracking_id)
    return None

@router.get("/obtener_todos", response_model=list[PermisoRead])
def obtener_todos(db: DBSession, activo: bool):
    return PermisoService(db).obtener_todos(activo)

@router.get("/obtener_por_tracking_id", response_model=PermisoRead)
def obtener_por_tracking_id(db: DBSession, tracking_id: str):
    return PermisoService(db).obtener_por_tracking_id(tracking_id)
