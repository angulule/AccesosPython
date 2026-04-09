from sqlmodel import SQLModel, Field
from datetime import datetime

class PermisoDefaultModel(SQLModel, table=True):
    __tablename__ = "permiso_default"
    
    permiso_default_id: int | None = Field(default=None, primary_key=True, index=True)
    tracking_id: str = Field(max_length=36, index=True, nullable=False)
    role_id: str = Field(foreign_key="rol.role_id", max_length=36, nullable=False, index=True,)
    pantalla_id: int = Field(foreign_key="pantalla.pantalla_id", nullable=False, index=True)
    permiso_id: int = Field(foreign_key="permiso.permiso_id", nullable=False, index=True)
    permiso: bool = Field(default=True, nullable=False)
    activo: bool = Field(default=True, nullable=False)