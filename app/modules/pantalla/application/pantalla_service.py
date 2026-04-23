import uuid

from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.pantalla.infrastructure.pantalla_model import PantallaModel
from app.modules.pantalla.interfaces.pantalla_schema import PantallaCreate, PantallaUpdate, PantallaRead
from app.modules.pantalla.infrastructure.pantalla_repository import PantallaRepository
from app.modules.modulo.infrastructure.modulo_repository import ModuloRepository
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository

class PantallaService:
    def __init__(self, db: Session):
        self.db = db
        self.pantalla_repository = PantallaRepository(db)
        self.modulo_repository = ModuloRepository(db)
        self.usuario_repository = UsuarioRepository(db)
        
    def crear(self, data: PantallaCreate, user_id: str) -> PantallaRead:
        usuario = self.usuario_repository.validar_usuario(user_id)
         
        modulo = self.modulo_repository.obtener_por_tracking_id(data.modulo_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="El módulo no se encuentra registrado.")
        
        if self.pantalla_repository.obtener_por_pantalla(data.pantalla):
            raise HTTPException(status_code=404, detail="La pantalla ya existe.")
        
        if self.pantalla_repository.obtener_por_modulo_id_pantalla(modulo.modulo_id, data.pantalla):
            raise HTTPException(status_code=409, detail=f"La pantalla {data.pantalla} ya existe para el módulo {modulo.modulo}.")
        
        pantalla = PantallaModel(
            tracking_id=str(uuid.uuid4()),
            pantalla=data.pantalla.strip(),
            descripcion=data.descripcion.strip() if data.descripcion else None,
            modulo_id=modulo.modulo_id,
            registrado_por=usuario.usuario_id
        )
        
        pantalla = self.pantalla_repository.crear(pantalla)
        return self._map_to_read(pantalla)


    def actualizar(self, data: PantallaUpdate, user_id: str)-> PantallaRead:
        usuario = self.usuario_repository.validar_usuario(user_id)
        
        pantalla = self.pantalla_repository.obtener_por_tracking_id(data.tracking_id)
        if not pantalla:
            raise HTTPException(status_code=404, detail="La pantalla no se encuentra registrada")
        
        modulo = self.modulo_repository.obtener_por_tracking_id(data.modulo_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="El módulo no se encuentra registrado.")
        
        pantalla.pantalla = data.pantalla.strip()
        pantalla.descripcion = data.descripcion.strip()
        pantalla.modulo_id = modulo.modulo_id
        pantalla.modificado_por = usuario.usuario_id
        pantalla.fecha_modificacion = datetime.now()
        pantalla = self.pantalla_repository.actualizar(pantalla)
        
        return self._map_to_read(pantalla)
    
    def eliminar(self, tracking_id: str, user_id: str) -> None:
        usuario = self.usuario_repository.validar_usuario(user_id)
        
        pantalla = self.pantalla_repository.obtener_por_tracking_id(tracking_id)
        if not pantalla:
            raise HTTPException(status_code=404, detail="La pantalla no se encuentra registrada")
        
        pantalla.activo = False if pantalla.activo else True
        pantalla.modificado_por = usuario.usuario_id
        pantalla.fecha_modificacion = datetime.now()
        self.pantalla_repository.actualizar(pantalla)
    
    def obtener_por_pantalla_id(self, pantalla_id: int)-> PantallaRead:
        pantalla = self.pantalla_repository.obtener_por_pantalla_id(pantalla_id)
        return self._map_to_read(pantalla)
    
    def obtener_por_tracking_id(self, tracking_id: str)-> PantallaRead:
        pantalla = self.pantalla_repository.obtener_por_tracking_id(tracking_id)
        return self._map_to_read(pantalla)
    
    def obtener_por_modulo_id(self, modulo_id: str, activo: bool)-> list[PantallaRead]:
        modulo = self.modulo_repository.obtener_por_tracking_id(modulo_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="El módulo no se encuentra registrado.")
        
        pantallas = self.pantalla_repository.obtener_por_modulo_id(modulo.modulo_id, activo)
        return [self._map_to_read(pantalla) for pantalla in pantallas]
    
    def obtener_todos(self, activo: bool) -> list[PantallaRead]:
        pantallas = self.pantalla_repository.obtener_todos(activo)
        return [self._map_to_read(pantalla) for pantalla in pantallas]
    
    def _map_to_read(self, pantalla: PantallaModel) -> PantallaRead:
        modulo = self.modulo_repository.obtener_por_modulo_id(pantalla.modulo_id)
        registrado_por = self.usuario_repository.obtener_por_usuario_id(pantalla.registrado_por)
        modificado_por = self.usuario_repository.obtener_por_usuario_id(pantalla.modificado_por)
        
        return PantallaRead(                
            tracking_id=pantalla.tracking_id,
            pantalla=pantalla.pantalla,
            descripcion=pantalla.descripcion,
            modulo_id=modulo.tracking_id if modulo else "",
            modulo=modulo.modulo if modulo else "",
            activo=pantalla.activo,
            registrado_por=registrado_por.nombre if registrado_por else "",
            modificado_por=modificado_por.nombre if modificado_por else None,
            fecha_creacion=pantalla.fecha_creacion,
            fecha_modificacion=pantalla.fecha_modificacion
        )