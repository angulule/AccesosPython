import uuid

from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.modulo.infrastructure.ModuloModel import ModuloModel
from app.modules.modulo.interfaces.modulo_schema import ModuloRead
from app.modules.modulo.infrastructure.modulo_repository import ModuloRepository

class ModuloService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ModuloRepository(db)
        
    def crear(self, nombre: str):
        if self.repo.obtener_por_modulo(nombre.strip()):
            raise HTTPException(status_code=409, detail="El módulo ya se encuentra registrado.")
        
        modulo = ModuloModel(
            tracking_id=str(uuid.uuid4()),
            modulo=nombre.strip(),
            registrado_por=1
        )
        
        modulo = self.repo.crear(modulo)
        return modulo

    def actualizar(self, tracking_id: str, nombre: str):
        modulo = self.repo.obtener_por_tracking_id(tracking_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")
        
        modulo.modulo = nombre.strip()
        modulo.modificado_por = 1
        modulo.fecha_modificacion = datetime.now()
        return self.repo.actualizar(modulo)
    
    def eliminar(self, tracking_id: str) -> None:
        modulo = self.repo.obtener_por_tracking_id(tracking_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")
        
        modulo.activo = False if modulo.activo else True
        modulo.modificado_por = 1
        modulo.fecha_modificacion = datetime.now()
        self.repo.actualizar(modulo)
    
    def obtener_todos(self, activo: bool):
        return self.repo.obtener_todos(activo)
    
    def obtener_por_tracking_id(self, tracking_id: str):
        return self.repo.obtener_por_tracking_id(tracking_id)