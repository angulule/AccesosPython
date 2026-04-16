from sqlmodel import select, Session

from app.modules.user.infrastructure.UserModel import UserModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def obtener_por_user_id(self, user_id: str) -> UserModel | None:
        return self.db.exec(select(UserModel).where(UserModel.user_id == user_id)).first()
    
    def obtener_por_username(self, username: str) -> UserModel | None:
        return self.db.exec(select(UserModel).where(UserModel.username == username)).first()
    
    def crear(self, user: UserModel | None) -> UserModel:        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
