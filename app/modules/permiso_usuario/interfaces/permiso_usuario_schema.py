from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PermisoUsuarioCreate(BaseModel):
    usuario_id: str
    pantalla_id: str
    permiso_id: str
    
class PermisoUsuarioUpdate(BaseModel):
    tracking_id: str
    usuario_id: str
    pantalla_id: str
    permiso_id: str
    
class PermisoUsuarioRead(BaseModel):
    tracking_id: str
    usuario_id: str
    usuario: str
    pantalla_id: str
    pantalla: str
    permiso_id: str
    permiso: str