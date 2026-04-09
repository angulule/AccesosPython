from sqlmodel import Session, select
from app.modules.modulo.infrastructure.ModuloModel import ModuloModel

class ModuloRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, modulo: ModuloModel) -> ModuloModel:
        self.session.add(modulo)
        self.session.commit()
        self.session.refresh(modulo)
        return modulo
    
    def actualizar(self, modulo: ModuloModel):
        self.session.add(modulo)
        self.session.commit()
        self.session.refresh(modulo)
        return modulo
    
    def obtener_todos(self, activo: bool) -> list[ModuloModel]:
        return self.session.exec(select(ModuloModel).where(ModuloModel.activo == activo)).all()

    def obtener_por_modulo_id(self, modulo_id: int) -> ModuloModel:
        return self.session.exec(select(ModuloModel).where(ModuloModel.modulo_id == modulo_id)).first()
    
    def obtener_por_tracking_id(self, tracking_id: str) -> ModuloModel:
        return self.session.exec(select(ModuloModel).where(ModuloModel.tracking_id == tracking_id)).first()
    
    def obtener_por_modulo(self, modulo: str) -> ModuloModel:
        return self.session.exec(select(ModuloModel).where(ModuloModel.modulo == modulo)).first()
    
    