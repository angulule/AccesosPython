import uuid

from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.permiso_default.infrastructure.permiso_default_model import PermisoDefaultModel
from app.modules.permiso_default.interfaces.permiso_default_schema import PermisoDefaultCreate, PermisoDefaultUpdate
from app.modules.permiso_default.infrastructure.permiso_default_repository import PermisoDefaultRepository

class PermisoDefaultService:
    def __init__(self, db: Session):
        self.db = db
        self.permiso_default_repository = PermisoDefaultRepository(db)
        
    def crear(self, payload: PermisoDefaultCreate):
        if self.repo.obtener_por_permiso_default(payload.permiso_default.strip()):
            raise HTTPException(status_code=409, detail="El permiso_default ya se encuentra registrado.")
        
        permiso_default = PermisoDefaultModel(
            tracking_id=str(uuid.uuid4()),
            role_id=payload.role_id.strip(),
            pantalla_id=payload.pantalla_id,
            permiso_id=payload.permiso_id
        )
        
        permiso_default = self.permiso_default_repository.crear(permiso_default)
        return permiso_default.tracking_id
    
    def eliminar(self, tracking_id: str) -> None:
        permiso_default = self.permiso_default_repository.obtener_por_tracking_id(tracking_id)
        if not permiso_default:
            raise HTTPException(status_code=404, detail="El permiso no fue encontrado")
        
        self.repo.eliminar(permiso_default)
    
    def obtener_por_role_id(self, role_id: str):
        return self.permiso_default_repository.obtener_por_role_id(role_id)
    
    def obtener_por_permiso_default_id(self, permiso_default_id: str):
        return self.permiso_default_repository.obtener_por_permiso_default_id(permiso_default_id)
    
    def obtener_por_tracking_id(self, tracking_id: str):
        return self.permiso_default_repository.obtener_por_tracking_id(tracking_id)