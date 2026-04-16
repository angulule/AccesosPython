from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint, Column, DateTime

class UsuarioModel(SQLModel, table=True):
    __tablename__ = "usuario"
    __table_args__ = (UniqueConstraint("user_id", name="uq_usuario_user"),)
    
    usuario_id: int = Field(primary_key=True, index=True, default=None, nullable=False)
    user_id: str = Field(foreign_key="user.user_id", nullable=False, index=True, unique=True)
    nombre: str = Field(nullable=False, max_length=255)
    nombres: str = Field(nullable=True, max_length=255)
    apellido_paterno: str = Field(nullable=True, max_length=255)
    apellido_materno: str = Field(nullable=True, max_length=255)
    domicilio: str = Field( nullable=True, max_length=255)
    telefono: str = Field( nullable=True, max_length=20)
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