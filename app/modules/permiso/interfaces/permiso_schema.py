from datetime import datetime
from pydantic import BaseModel
    
    
class PermisoRead(BaseModel):
    tracking_id: str
    permiso: str
    activo: bool