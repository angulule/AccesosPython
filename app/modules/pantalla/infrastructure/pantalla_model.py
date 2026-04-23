from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime

class PantallaModel(SQLModel, table=True):
    __tablename__ = "pantalla"
     
    pantalla_id: int = Field(default=None, primary_key=True)
    tracking_id: str = Field(max_length=36, index=True, nullable=False)
    pantalla: str = Field(max_length=256, nullable=False, index=True)
    descripcion: str = Field(max_length=256, nullable=True)
    modulo_id: int = Field(foreign_key="modulo.modulo_id", nullable=False, index=True)
    activo: bool = True
    registrado_por: int = Field(nullable=False)
    
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    
    modificado_por: int = Field(nullable=True)
    
    fecha_modificacion: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )