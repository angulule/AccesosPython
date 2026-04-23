from sqlmodel import Session

from app.modules.membership.infrastructure.membership_model import Membership
from app.modules.membership.infrastructure.membership_repository import MembershipRepository

class MembershipService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MembershipRepository(db)
        
    def crear(self, membership: Membership):
        return self.repo.crear(membership)
        
    def obtener_por_user_id(self, user_id: str):
        return self.repo.obtener_por_user_id(user_id)
    
    def obtener_por_email(self, email: str):
        return self.repo.obtener_por_email(email)