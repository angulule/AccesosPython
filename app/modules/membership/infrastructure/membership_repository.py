from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.membership.infrastructure.MembershipModel import MembershipModel


class MembershipRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def obtener_por_user_id(self, user_id: str) -> MembershipModel | None:
        return self.db.get(MembershipModel, user_id)
    
    def obtener_por_email(self, email: str) -> MembershipModel | None:
       return self.db.execute(select(MembershipModel).where(MembershipModel.email == email)).first()
    
    def crear(self, membership: MembershipModel | None) -> MembershipModel:
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(membership)
        
        return membership
    