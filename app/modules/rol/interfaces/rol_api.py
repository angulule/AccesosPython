from fastapi import APIRouter, Depends, status

from app.modules.deps import DBSession
from app.modules.rol.application.rol_service import RolService
from app.modules.rol.interfaces.rol_schema import RolRead, RolCreate, RolUpdate

router = APIRouter(prefix="/rol", tags=["rol"])


@router.post("/crear", response_model=RolRead, status_code=status.HTTP_201_CREATED)
def crear(db: DBSession, payload: RolCreate):
    return RolService(db).crear(payload)

@router.put("/actualizar", response_model=RolRead, status_code=status.HTTP_200_OK)
def actualizar(db: DBSession, payload: RolUpdate):
    return RolService(db).actualizar(payload)

@router.put("/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(db: DBSession, role_id: str):
    RolService(db).eliminar(role_id)
    return None

@router.get("/obtener_todos", response_model=list[RolRead])
def obtener_todos(db: DBSession, activo: bool):
    return RolService(db).obtener_todos(activo)

@router.get("/obtener_por_role_id", response_model=RolRead)
def obtener_por_role_id(db: DBSession, role_id: str):
    return RolService(db).obtener_por_role_id(role_id)
