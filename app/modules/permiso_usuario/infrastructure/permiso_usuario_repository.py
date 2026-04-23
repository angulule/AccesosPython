from sqlmodel import Session, select
from app.modules.permiso_usuario.infrastructure.permiso_usuario_model import PermisoUsuarioModel
from app.modules.pantalla.infrastructure.pantalla_model import PantallaModel

class PermisoUsuarioRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def crear(self, permiso: PermisoUsuarioModel):
        self.session.add(permiso)
        self.session.commit()
        self.session.refresh(permiso)
        return permiso
    
    def actualizar(self, permiso: PermisoUsuarioModel):
        self.session.add(permiso)
        self.session.commit()
        self.session.refresh(permiso)
        return permiso
    
    def eliminar(self, permiso: PermisoUsuarioModel):
        self.session.delete(permiso)
        self.session.commit()

    def obtener_por_permiso_usuario_id(self, permiso_usuario_id: int) -> PermisoUsuarioModel:
        return self.session.exec(select(PermisoUsuarioModel)
                                 .where(PermisoUsuarioModel.permiso_usuario_id == permiso_usuario_id)).first()
    
    def obtener_por_tracking_id(self, tracking_id: str) -> PermisoUsuarioModel:
        return self.session.exec(select(PermisoUsuarioModel).where(PermisoUsuarioModel.tracking_id == tracking_id)).first()
    
    def obtener_por_usuario_pantalla(self, usuario_id: int, pantalla_id: int) -> PermisoUsuarioModel:
        return self.session.exec(select(PermisoUsuarioModel)
                                    .where(PermisoUsuarioModel.usuario_id == usuario_id)
                                    .where(PermisoUsuarioModel.pantalla_id == pantalla_id)).first()
        
    def obtener_por_usuario_pantalla_permiso(self, usuario_id: int, pantalla_id: int, permiso_id: int) -> PermisoUsuarioModel:
        return self.session.exec(select(PermisoUsuarioModel)
                                    .where(PermisoUsuarioModel.usuario_id == usuario_id)
                                    .where(PermisoUsuarioModel.pantalla_id == pantalla_id)
                                    .where(PermisoUsuarioModel.permiso_id == permiso_id)).first()
    
    def obtener_por_usuario_modulo(self, usuario_id: int, modulo_id: int) -> list[PermisoUsuarioModel]:
        return self.session.exec(select(PermisoUsuarioModel)
                                    .join(PantallaModel, PermisoUsuarioModel.pantalla_id == PantallaModel.pantalla_id)
                                    .where(PantallaModel.modulo_id == modulo_id)
                                    .where(PermisoUsuarioModel.usuario_id == usuario_id)).all()
        
    def obtener_todos(self, activo: bool) -> list[PermisoUsuarioModel]:
        return self.session.exec(select(PermisoUsuarioModel).where(PermisoUsuarioModel.activo == activo)).all()