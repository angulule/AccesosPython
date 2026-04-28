from sqlmodel import Session

from app.modules.user.infrastructure.user_model import User
from app.modules.user.infrastructure.user_repository import UserRepository

class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        
    def crear(self, user: User):
        return self.user_repository.crear(user)
        
    def obtener_por_user_id(self, user_id: str):
        return self.user_repository.obtener_por_user_id(user_id)
    
    def obtener_por_username(self, username: str):
        return self.user_repository.obtener_por_username(username)