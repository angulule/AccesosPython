from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime

class UserModel(SQLModel, table=True):
    __tablename__ = "user"
    
    user_id: str = Field(primary_key=True, max_length=36, index=True)
    username: str = Field(unique=True, index=True, nullable=False, max_length=255)
    
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
