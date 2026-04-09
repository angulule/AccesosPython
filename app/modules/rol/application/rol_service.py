import uuid

from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.rol.infrastructure.RolModel import RolModel
from app.modules.rol.interfaces.rol_schema import RolCreate, RolUpdate
from app.modules.rol.infrastructure.rol_repository import RolRepository

class RolService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = RolRepository(db)
        
    def crear(self, payload: RolCreate):
        if self.repo.obtener_por_rol(payload.rol.strip()):
            raise HTTPException(status_code=409, detail="El rol ya se encuentra registrado.")
        
        rol = RolModel(
            role_id=str(uuid.uuid4()),
            rol=payload.rol.strip(),
            descripcion=payload.descripcion.strip() if payload.descripcion else None,
            registrado_por=1
        )
        
        rol = self.repo.crear(rol)
        return rol

    def actualizar(self, payload: RolUpdate):
        rol = self.repo.obtener_por_role_id(payload.role_id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        rol.rol = payload.rol.strip()
        rol.descripcion = payload.descripcion.strip() if payload.descripcion else rol.descripcion
        rol.modificado_por = 1
        rol.fecha_modificacion = datetime.now()
        
        # if payload.descripcion:
        #     rol.descripcion = payload.descripcion.strip()
        
        return self.repo.actualizar(rol)
    
    def eliminar(self, role_id: str) -> None:
        rol = self.repo.obtener_por_role_id(role_id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        self.repo.eliminar(rol)
    
    def obtener_todos(self, activo: bool):
        return self.repo.obtener_todos(activo)
    
    def obtener_por_role_id(self, tracking_id: str):
        return self.repo.obtener_por_role_id(tracking_id)
    
    def obtener_por_rol_id(self, rol_id: int):
        return self.repo.obtener_por_rol_id(rol_id)