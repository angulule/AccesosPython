from sqlmodel import Session, select
from app.modules.permiso.infrastructure.PermisoModel import PermisoModel

class PermisoRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, permiso: PermisoModel) -> PermisoModel:
        self.session.add(permiso)
        self.session.commit()
        self.session.refresh(permiso)
        return permiso
    
    def actualizar(self, permiso: PermisoModel):
        self.session.add(permiso)
        self.session.commit()
        self.session.refresh(permiso)
        return permiso
    
    def obtener_todos(self, activo: bool) -> list[PermisoModel]:
        return self.session.exec(select(PermisoModel).where(PermisoModel.activo == activo)).all()

    def obtener_por_permiso_id(self, permiso_id: int) -> PermisoModel:
        return self.session.exec(select(PermisoModel).where(PermisoModel.permiso_id == permiso_id)).first()
    
    def obtener_por_tracking_id(self, tracking_id: str) -> PermisoModel:
        return self.session.exec(select(PermisoModel).where(PermisoModel.tracking_id == tracking_id)).first()
    
    def obtener_por_permiso(self, permiso: str) -> PermisoModel:
        return self.session.exec(select(PermisoModel).where(PermisoModel.permiso == permiso)).first()
    
    