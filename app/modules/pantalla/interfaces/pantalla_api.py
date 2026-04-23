from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.modules.deps import CurrentUser, DBSession
from app.modules.pantalla.application.pantalla_service import PantallaService
from app.modules.pantalla.interfaces.pantalla_schema import PantallaCreate, PantallaUpdate, PantallaRead

router = APIRouter(prefix="/pantalla", tags=["pantalla"])


@router.post("/crear", response_model=PantallaRead, status_code=status.HTTP_201_CREATED)
def crear(db: DBSession, data: PantallaCreate, user: CurrentUser):
    return PantallaService(db).crear(data, user.user_id)


@router.put("/actualizar", response_model=PantallaRead)
def actualizar(db: DBSession, data: PantallaUpdate, user: CurrentUser):
    return PantallaService(db).actualizar(data, user.user_id)

@router.put("/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(db: DBSession, tracking_id: str, user: CurrentUser):
    PantallaService(db).eliminar(tracking_id, user.user_id)
    return None

@router.get("/obtener_por_modulo_id", response_model=list[PantallaRead])
def obtener_por_modulo_id(db: DBSession, modulo_id: str, activo: bool, user: CurrentUser):
    return PantallaService(db).obtener_por_modulo_id(modulo_id, activo)


@router.get("/obtener_por_tracking_id", response_model=PantallaRead)
def obtener_por_tracking_id(db: DBSession, tracking_id: str, user: CurrentUser):
    return PantallaService(db).obtener_por_tracking_id(tracking_id)

@router.get("/obtener_todos", response_model=list[PantallaRead])
def obtener_todos(db: DBSession, activo: bool, user: CurrentUser):
    return PantallaService(db).obtener_todos(activo)