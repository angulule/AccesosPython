from datetime import datetime
from pydantic import BaseModel
from typing import Optional
    
class ModuloRead(BaseModel):
    tracking_id: str
    modulo: str
    activo: bool
    registrado_por: str
    fecha_creacion: datetime
    modificado_por: Optional[str] = None
    fecha_modificacion: Optional[datetime] = None