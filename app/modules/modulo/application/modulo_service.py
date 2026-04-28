import uuid

from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.modulo.infrastructure.modulo_model import ModuloModel
from app.modules.modulo.interfaces.modulo_schema import ModuloRead
from app.modules.modulo.infrastructure.modulo_repository import ModuloRepository
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository

class ModuloService:
    def __init__(self, db: Session):
        self.db = db
        self.modulo_repository = ModuloRepository(db)
        self.usuario_repository = UsuarioRepository(db)
        
    def crear(self, nombre: str, user_id: str) -> ModuloRead:
        usuario = self.usuario_repository.validar_usuario(user_id)
        
        modulo = ModuloModel(
            tracking_id=str(uuid.uuid4()),
            modulo=nombre.strip(),
            registrado_por=usuario.usuario_id
        )
        
        self._validar_modulo(modulo)
        modulo = self.modulo_repository.crear(modulo)
        return self._map_to_read(modulo)

    def actualizar(self, tracking_id: str, nombre: str, user_id: str) -> ModuloRead:
        usuario = self.usuario_repository.validar_usuario(user_id)
        
        modulo = self.modulo_repository.obtener_por_tracking_id(tracking_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")
        
        modulo.modulo = nombre.strip()
        modulo.modificado_por = usuario.usuario_id
        modulo.fecha_modificacion = datetime.now(timezone.utc)
        
        self._validar_modulo(modulo)
        self.modulo_repository.actualizar(modulo)
        
        return self._map_to_read(modulo)
    
    def eliminar(self, tracking_id: str, user_id: str) -> None:
        usuario = self.usuario_repository.validar_usuario(user_id)
        
        modulo = self.modulo_repository.obtener_por_tracking_id(tracking_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")
        
        modulo.activo = False if modulo.activo else True
        modulo.modificado_por = usuario.usuario_id
        modulo.fecha_modificacion = datetime.now()
        self.modulo_repository.actualizar(modulo)
    
    def obtener_todos(self, activo: bool) -> list[ModuloRead]:
        modulos = self.modulo_repository.obtener_todos(activo)
        return [self._map_to_read(modulo) for modulo in modulos]
    
    def obtener_por_tracking_id(self, tracking_id: str):
        modulo = self.modulo_repository.obtener_por_tracking_id(tracking_id)
        return self._map_to_read(modulo)
    
    def _map_to_read(self, modulo: ModuloModel) -> ModuloRead:
        registrado_por = self.usuario_repository.obtener_por_usuario_id(modulo.registrado_por)
        modificado_por = self.usuario_repository.obtener_por_usuario_id(modulo.registrado_por)
        
        return ModuloRead(
            tracking_id=modulo.tracking_id,
            modulo=modulo.modulo,
            activo=modulo.activo,
            registrado_por=registrado_por.nombre if registrado_por else "",
            modificado_por=modificado_por.nombre if modificado_por else None,
            fecha_creacion=modulo.fecha_creacion,
            fecha_modificacion=modulo.fecha_modificacion
        )
        
    def _validar_modulo(self, modulo: ModuloModel):
        modulo_aux = self.modulo_repository.obtener_por_modulo(modulo.modulo.strip())
        
        if modulo_aux and modulo.tracking_id != modulo_aux.tracking_id:
            raise HTTPException(status_code=409, detail=f"El módulo {modulo.modulo} ya se encuentra registrado.")