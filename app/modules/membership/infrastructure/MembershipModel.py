from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class MembershipModel(SQLModel, table=True):
    __tablename__ = "membership"
     
    user_id: str = Field(foreign_key="user.user_id", primary_key=True, unique=True, index=True, max_length=36)    
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    password: str = Field(nullable=False, max_length=255)
    esta_bloqueado: bool = Field(default=False)
    
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

