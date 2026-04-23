from sqlmodel import Session

from app.modules.usuario.infrastructure.usuario_model import Usuario
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UsuarioRepository(db)
        
    def crear(self, usuario: Usuario):
        return self.repo.crear(usuario)
        
    def obtener_por_user_id(self, user_id: str):
        return self.repo.obtener_por_user_id(user_id)
    
    def obtener_por_usuario_id(self, usuario_id: str):
        return self.repo.obtener_por_usuario_id(usuario_id)