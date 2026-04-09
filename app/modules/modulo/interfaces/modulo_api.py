from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.modules.deps import DBSession
from app.modules.modulo.application.modulo_service import ModuloService
from app.modules.modulo.interfaces.modulo_schema import ModuloRead

router = APIRouter(prefix="/modulo", tags=["modulo"])


@router.post("/crear", response_model=ModuloRead, status_code=status.HTTP_201_CREATED)
def crear(db: DBSession, nombre: str):
    return ModuloService(db).crear(nombre)


@router.put("/actualizar", response_model=ModuloRead)
def actualizar(db: DBSession, tracking_id: str, nombre: str):
    return ModuloService(db).actualizar(tracking_id, nombre)

@router.put("/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(db: DBSession, tracking_id: str):
    ModuloService(db).eliminar(tracking_id)
    return None

@router.get("/obtener_todos", response_model=list[ModuloRead])
def obtener_todos(db: DBSession, activo: bool):
    return ModuloService(db).obtener_todos(activo)


@router.get("/obtener_por_tracking_id", response_model=ModuloRead)
def obtener_por_tracking_id(db: DBSession, tracking_id: str):
    return ModuloService(db).obtener_por_tracking_id(tracking_id)
