from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    username: str
    nombre: str = ""
    password: str
    email: str
    
class UsuarioRead(BaseModel):
    user_id: str
    nombre: str
    email: str