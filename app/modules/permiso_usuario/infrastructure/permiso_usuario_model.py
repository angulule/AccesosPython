from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime

class PermisoUsuarioModel(SQLModel, table=True):
    __tablename__ = "permiso_usuario"
     
    permiso_usuario_id: int = Field(default=None, primary_key=True, nullable=False)
    tracking_id: str = Field(max_length=36, index=True, nullable=False)
    usuario_id: int = Field(foreign_key="usuario.usuario_id", nullable=False, index=True)
    pantalla_id: int = Field(foreign_key="pantalla.pantalla_id", nullable=False, index=True)
    permiso_id: int = Field(foreign_key="permiso.permiso_id", nullable=False, index=True)
    permiso: bool = True
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