from sqlmodel import SQLModel, Field
from datetime import datetime

class PantallaModel(SQLModel, table=True):
    __tablename__ = "pantalla"
     
    pantalla_id: int = Field(default=None, primary_key=True)
    tracking_id: str = Field(max_length=36, index=True, nullable=False)
    pantalla: str = Field(max_length=256, nullable=False, index=True)
    descripcion: str = Field(max_length=256, nullable=True)
    modulo_id: int = Field(foreign_key="modulo.modulo_id", nullable=False, index=True)
    activo: bool = True
    registrado_por: int = Field(nullable=False)
    fecha_registro: datetime = Field(default=datetime.now(), nullable=False)
    modificado_por: int = Field(nullable=True)
    fecha_modificacion: datetime = Field(nullable=True)