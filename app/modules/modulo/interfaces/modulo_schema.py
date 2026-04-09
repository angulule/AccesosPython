from datetime import datetime
from pydantic import BaseModel
    
    
class ModuloRead(BaseModel):
    tracking_id: str
    modulo: str
    activo: bool