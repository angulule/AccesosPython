import uuid

from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.permiso.infrastructure.PermisoModel import PermisoModel
from app.modules.permiso.interfaces.permiso_schema import PermisoRead
from app.modules.permiso.infrastructure.permiso_repository import PermisoRepository

class PermisoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PermisoRepository(db)
        
    def crear(self, nombre: str):
        if self.repo.obtener_por_permiso(nombre.strip()):
            raise HTTPException(status_code=409, detail="El permiso ya se encuentra registrado.")
        
        permiso = PermisoModel(
            tracking_id=str(uuid.uuid4()),
            permiso=nombre.strip(),
            registrado_por=1
        )
        
        permiso = self.repo.crear(permiso)
        return permiso

    def actualizar(self, tracking_id: str, nombre: str):
        permiso = self.repo.obtener_por_tracking_id(tracking_id)
        if not permiso:
            raise HTTPException(status_code=404, detail="Permiso no encontrado")
        
        permiso.permiso = nombre.strip()
        permiso.modificado_por = 1
        permiso.fecha_modificacion = datetime.now()
        return self.repo.actualizar(permiso)
    
    def eliminar(self, tracking_id: str) -> None:
        permiso = self.repo.obtener_por_tracking_id(tracking_id)
        if not permiso:
            raise HTTPException(status_code=404, detail="Permiso no encontrado")
        
        permiso.activo = False if permiso.activo else True
        permiso.modificado_por = 1
        permiso.fecha_modificacion = datetime.now()
        self.repo.actualizar(permiso)
    
    def obtener_todos(self, activo: bool):
        return self.repo.obtener_todos(activo)
    
    def obtener_por_tracking_id(self, tracking_id: str):
        return self.repo.obtener_por_tracking_id(tracking_id)
    
    def obtener_por_permiso_id(self, permiso_id: int):
        return self.repo.obtener_por_permiso_id(permiso_id)