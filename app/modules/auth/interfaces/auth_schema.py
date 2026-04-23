from pydantic import BaseModel

from app.modules.usuario.interfaces.usuario_schema import UsuarioRead

class LoginRequest(BaseModel):
    username: str
    password: str
    
class LoginResponse(BaseModel):
    token: str
    token_type: str
    usuario: UsuarioRead
    
class TokenValidationResponse(BaseModel):
    valid: bool
    usuario: dict
    