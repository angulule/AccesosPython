from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime

class ModuloModel(SQLModel, table=True):
    __tablename__ = "modulo"
    
    modulo_id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    tracking_id: str = Field(max_length=36, index=True, nullable=False)
    modulo: str = Field(max_length=50, nullable=False, index=True)
    activo: bool = Field(default=True, nullable=False)
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