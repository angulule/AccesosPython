from sqlmodel import select, Session
from fastapi import HTTPException

from app.modules.usuario.infrastructure.usuario_model import UsuarioModel

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def obtener_por_user_id(self, user_id: str) -> UsuarioModel | None:
        return self.db.exec(select(UsuarioModel).where(UsuarioModel.user_id == user_id)).first()
    
    
    def obtener_por_usuario_id(self, usuario_id: str) -> UsuarioModel | None:
        return self.db.exec(select(UsuarioModel).where(UsuarioModel.usuario_id == usuario_id)).first()
    
    def validar_usuario(self, user_id: str):
        usuario = self.obtener_por_user_id(user_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return usuario
    
    
    def crear(self, usuario: UsuarioModel | None) -> UsuarioModel:        
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
