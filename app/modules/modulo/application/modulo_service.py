import uuid

from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.modulo.infrastructure.ModuloModel import ModuloModel
from app.modules.modulo.interfaces.modulo_schema import ModuloRead
from app.modules.modulo.infrastructure.modulo_repository import ModuloRepository
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository

class ModuloService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ModuloRepository(db)
        self.usuarioRepo = UsuarioRepository(db)
        
    def crear(self, nombre: str, user_id: str) -> ModuloRead:
        usuario = self.usuarioRepo.validar_usuario(user_id)
        
        if self.repo.obtener_por_modulo(nombre.strip()):
            raise HTTPException(status_code=409, detail="El módulo ya se encuentra registrado.")
        
        modulo = ModuloModel(
            tracking_id=str(uuid.uuid4()),
            modulo=nombre.strip(),
            registrado_por=usuario.usuario_id
        )
        
        modulo = self.repo.crear(modulo)
        
        modulo_read = ModuloRead(
            tracking_id=modulo.tracking_id,
            modulo=modulo.modulo,
            activo=modulo.activo,
            registrado_por=usuario.nombre,
            fecha_creacion=modulo.fecha_creacion
        )
        
        return modulo_read

    def actualizar(self, tracking_id: str, nombre: str, user_id: str) -> ModuloRead:
        usuario = self.usuarioRepo.validar_usuario(user_id)
        
        modulo = self.repo.obtener_por_tracking_id(tracking_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")
        
        modulo.modulo = nombre.strip()
        modulo.modificado_por = usuario.usuario_id
        modulo.fecha_modificacion = datetime.now(timezone.utc)
        self.repo.actualizar(modulo)
        
        registrado_por = self.usuarioRepo.obtener_por_usuario_id(modulo.registrado_por)
        
        modulo_read = ModuloRead(
            tracking_id=modulo.tracking_id,
            modulo=modulo.modulo,
            activo=modulo.activo,
            registrado_por=registrado_por.nombre if registrado_por else "",
            fecha_creacion=modulo.fecha_creacion,
            modificado_por=usuario.nombre if usuario else None,
            fecha_modificacion=modulo.fecha_modificacion if modulo.fecha_modificacion else None
        )
        
        return modulo_read
    
    def eliminar(self, tracking_id: str, user_id: str) -> None:
        usuario = self.usuarioRepo.validar_usuario(user_id)
        
        modulo = self.repo.obtener_por_tracking_id(tracking_id)
        if not modulo:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")
        
        modulo.activo = False if modulo.activo else True
        modulo.modificado_por = usuario.usuario_id
        modulo.fecha_modificacion = datetime.now()
        self.repo.actualizar(modulo)
    
    def obtener_todos(self, activo: bool) -> list[ModuloRead]:
        modulos = self.repo.obtener_todos(activo)
        data: list[ModuloRead] = []
        
        for modulo in modulos:
            registrado_por = self.usuarioRepo.obtener_por_usuario_id(modulo.registrado_por)
            modificado_por = self.usuarioRepo.obtener_por_usuario_id(modulo.modificado_por)
            
            modulo_read = ModuloRead(
                tracking_id=modulo.tracking_id,
                modulo=modulo.modulo,
                activo=modulo.activo,
                registrado_por=registrado_por.nombre if registrado_por else "",
                modificado_por=modificado_por.nombre if modificado_por else None,
                fecha_creacion=modulo.fecha_creacion,
                fecha_modificacion=modulo.fecha_modificacion
            )
            data.append(modulo_read)
        
        return data
    
    def obtener_por_tracking_id(self, tracking_id: str):
        modulo = self.repo.obtener_por_tracking_id(tracking_id)
        
        registrado_por = self.usuarioRepo.obtener_por_usuario_id(modulo.registrado_por)
        modificado_por = self.usuarioRepo.obtener_por_usuario_id(modulo.registrado_por)
        
        modulo_read = ModuloRead(
            tracking_id=modulo.tracking_id,
            modulo=modulo.modulo,
            activo=modulo.activo,
            registrado_por=registrado_por.nombre if registrado_por else "",
            modificado_por=modificado_por.nombre if modificado_por else None,
            fecha_creacion=modulo.fecha_creacion,
            fecha_modificacion=modulo.fecha_modificacion
        )
        
        return modulo_read