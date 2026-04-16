from sqlmodel import Session

from app.modules.user.infrastructure.UserModel import User
from app.modules.user.infrastructure.user_repository import UserRepository

class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)
        
    def crear(self, user: User):
        return self.repo.crear(user)
        
    def obtener_por_user_id(self, user_id: str):
        return self.repo.obtener_por_user_id(user_id)
    
    def obtener_por_username(self, username: str):
        return self.repo.obtener_por_username(username)