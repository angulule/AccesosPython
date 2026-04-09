from fastapi import APIRouter, Depends, status

from app.modules.deps import DBSession
from app.modules.permiso_default.application.permiso_default_service import PermisoDefaultService
from app.modules.permiso_default.interfaces.permiso_default_schema import PermisoDefaultCreate

router = APIRouter(prefix="/permiso_default", tags=["permiso_default"])


@router.post("/crear", response_model=str, status_code=status.HTTP_201_CREATED)
def crear(db: DBSession, payload: PermisoDefaultCreate):
    return PermisoDefaultService(db).crear(payload)

@router.put("/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(db: DBSession, permiso_defaulte_id: str):
    PermisoDefaultService(db).eliminar(permiso_defaulte_id)
    return None
