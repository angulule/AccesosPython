from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PermisoDefaultCreate(BaseModel):
    role_id: str
    pantalla_id: str
    permiso_id: str    
    