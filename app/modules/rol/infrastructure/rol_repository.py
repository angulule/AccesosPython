from sqlmodel import Session, select
from app.modules.rol.infrastructure.RolModel import RolModel

class RolRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, rol: RolModel) -> RolModel:
        self.session.add(rol)
        self.session.commit()
        self.session.refresh(rol)
        return rol
    
    def actualizar(self, rol: RolModel):
        self.session.add(rol)
        self.session.commit()
        self.session.refresh(rol)
        return rol
    
    def eliminar(self, rol: RolModel):
        self.session.delete(rol)
        self.session.commit()
    
    def obtener_todos(self, activo: bool) -> list[RolModel]:
        return self.session.exec(select(RolModel).where(RolModel.activo == activo)).all()

    def obtener_por_rol_id(self, rol_id: int) -> RolModel:
        return self.session.exec(select(RolModel).where(RolModel.rol_id == rol_id)).first()
    
    def obtener_por_role_id(self, role_id: str) -> RolModel:
        return self.session.exec(select(RolModel).where(RolModel.role_id == role_id)).first()
    
    def obtener_por_rol(self, rol: str) -> RolModel:
        return self.session.exec(select(RolModel).where(RolModel.rol == rol)).first()
    
    