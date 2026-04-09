from sqlmodel import SQLModel, Field
from datetime import datetime

class PermisoModel(SQLModel, table=True):
    __tablename__ = "permiso"
    
    permiso_id: int | None = Field(default=None, primary_key=True, index=True)
    tracking_id: str = Field(max_length=36, index=True, nullable=False)
    permiso: str = Field(max_length=50, nullable=False, index=True)
    activo: bool = Field(default=True, nullable=False)
    registrado_por: int = Field(nullable=False)
    fecha_creacion: datetime = Field(default=datetime.now(), nullable=False)
    modificado_por: int = Field(nullable=True)
    fecha_modificacion: datetime = Field(nullable=True)