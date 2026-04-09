import uuid

from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.pantalla.infrastructure.PantallaModel import PantallaModel
from app.modules.pantalla.interfaces.pantalla_schema import PantallaCreate, PantallaUpdate, PantallaRead
from app.modules.pantalla.infrastructure.pantalla_repository import PantallaRepository
from app.modules.modulo.infrastructure.modulo_repository import ModuloRepository

class PantallaService:
    def __init__(self, db: Session):
        self.db = db
        self.pantalla_repository = PantallaRepository(db)
        self.modulo_repository = ModuloRepository(db)
        
    def crear(self, data: PantallaCreate):
        modulo = self.modulo_repository.obtener_por_tracking_id(data.modulo_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="El módulo no se encuentra registrado.")
        
        if self.pantalla_repository.obtener_por_modulo_id_pantalla(modulo.modulo_id, data.pantalla):
            raise HTTPException(
                    status_code=409, 
                    detail=f"La pantalla {data.pantalla} ya existe para el módulo {modulo.modulo}.")
        
        pantalla = PantallaModel(
            tracking_id=str(uuid.uuid4()),
            pantalla=data.pantalla.strip(),
            descripcion=data.descripcion.strip() if data.descripcion else None,
            modulo_id=modulo.modulo_id,
            registrado_por=1
        )
        
        pantalla = self.pantalla_repository.crear(pantalla)
        return pantalla


    def actualizar(self, data: PantallaUpdate):
        pantalla = self.pantalla_repository.obtener_por_tracking_id(data.tracking_id)
        if not pantalla:
            raise HTTPException(status_code=404, detail="La pantalla no se encuentra registrada")
        
        modulo = self.modulo_repository.obtener_por_tracking_id(data.modulo_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="El módulo no se encuentra registrado.")
        
        pantalla.pantalla = data.pantalla.strip()
        pantalla.descripcion = data.descripcion.strip() if data.descripcion else pantalla.descripcion
        pantalla.modulo_id = modulo.modulo_id
        pantalla.modificado_por = 1
        pantalla.fecha_modificacion = datetime.now()
            
        return self.pantalla_repository.actualizar(pantalla)
    
    def eliminar(self, tracking_id: str) -> None:
        pantalla = self.pantalla_repository.obtener_por_tracking_id(tracking_id)
        if not pantalla:
            raise HTTPException(status_code=404, detail="La pantalla no se encuentra registrada")
        
        pantalla.activo = False if pantalla.activo else True
        pantalla.modificado_por = 1
        pantalla.fecha_modificacion = datetime.now()
        self.pantalla_repository.actualizar(pantalla)
    
    def obtener_por_pantalla_id(self, pantalla_id: int):
        return self.pantalla_repository.obtener_por_pantalla_id(pantalla_id)
    
    def obtener_por_tracking_id(self, tracking_id: str):
        return self.pantalla_repository.obtener_por_tracking_id(tracking_id)
    
    def obtener_por_modulo_id(self, modulo_id: str, activo: bool):
        modulo = self.modulo_repository.obtener_por_tracking_id(modulo_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="El módulo no se encuentra registrado.")
        
        return self.pantalla_repository.obtener_por_modulo_id(modulo.modulo_id, activo)
    
    def obtener_todos(self, activo: bool):
        return self.pantalla_repository.obtener_todos(activo)