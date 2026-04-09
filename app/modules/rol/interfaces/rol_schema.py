from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class RolCreate(BaseModel):
    rol: str
    descripcion: Optional[str] = None
    
class RolUpdate(BaseModel):
    role_id: str
    rol: str
    descripcion: Optional[str] = None
    
class RolRead(BaseModel):
    role_id: str
    rol: str
    descripcion: Optional[str] = None