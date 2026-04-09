from sqlmodel import Session, select
from app.modules.pantalla.infrastructure.PantallaModel import PantallaModel

class PantallaRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def crear(self, pantalla: PantallaModel):
        self.session.add(pantalla)
        self.session.commit()
        self.session.refresh(pantalla)
        return pantalla
    
    def actualizar(self, pantalla: PantallaModel):
        self.session.add(pantalla)
        self.session.commit()
        self.session.refresh(pantalla)
        return pantalla

    def obtener_por_pantalla_id(self, pantalla_id: int) -> PantallaModel:
        return self.session.exec(select(PantallaModel).where(PantallaModel.pantalla_id == pantalla_id)).first()
    
    def obtener_por_tracking_id(self, tracking_id: str) -> PantallaModel:
        return self.session.exec(select(PantallaModel).where(PantallaModel.tracking_id == tracking_id)).first()
    
    def obtener_por_modulo_id(self, modulo_id: int, activo: bool) -> list[PantallaModel]:
        return self.session.exec(select(PantallaModel)
                                    .where(PantallaModel.modulo_id == modulo_id)
                                    .where(PantallaModel.activo == activo)).all()
    
    def obtener_por_modulo_id_pantalla(self, modulo_id: int, pantalla: str) -> PantallaModel:
        return self.session.exec(select(PantallaModel)
                                    .where(PantallaModel.modulo_id == modulo_id)
                                    .where(PantallaModel.pantalla == pantalla)).first()
        
    def obtener_todos(self, activo: bool) -> list[PantallaModel]:
        return self.session.exec(select(PantallaModel).where(PantallaModel.activo == activo)).all()