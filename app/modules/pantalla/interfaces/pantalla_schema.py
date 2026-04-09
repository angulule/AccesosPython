from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PantallaCreate(BaseModel):
    pantalla: str
    descripcion: Optional[str] = None
    modulo_id: str
    
class PantallaUpdate(BaseModel):
    tracking_id: str
    pantalla: str
    descripcion: Optional[str] = None
    modulo_id: str
    
class PantallaRead(BaseModel):
    tracking_id: str
    pantalla: str
    descripcion: Optional[str] = None
    modulo_id: int
    activo: bool