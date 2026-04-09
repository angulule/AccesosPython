from sqlmodel import Session, select
from app.modules.permiso_default.infrastructure.PermisoDefaultModel import PermisoDefaultModel

class PermisoDefaultRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, permiso_default: PermisoDefaultModel) -> PermisoDefaultModel:
        self.session.add(permiso_default)
        self.session.commit()
        self.session.refresh(permiso_default)
        return permiso_default
    
    def actualizar(self, permiso_default: PermisoDefaultModel):
        self.session.add(permiso_default)
        self.session.commit()
        self.session.refresh(permiso_default)
        return permiso_default
    
    def eliminar(self, permiso_default: PermisoDefaultModel):
        self.session.delete(permiso_default)
        self.session.commit()

    def obtener_por_role_id(self, role_id: int) -> PermisoDefaultModel:
        return self.session.exec(select(PermisoDefaultModel).where(PermisoDefaultModel.role_id == role_id)).first()
    
    def obtener_por_permiso_default_id(self, permiso_default_id: int) -> PermisoDefaultModel:
        return self.session.exec(select(PermisoDefaultModel)
                                 .where(PermisoDefaultModel.permiso_default_id == permiso_default_id)).first()
    
    def obtener_por_tracking_id(self, tracking_id: str) -> PermisoDefaultModel:
        return self.session.exec(select(PermisoDefaultModel).where(PermisoDefaultModel.tracking_id == tracking_id)).first()
    
    