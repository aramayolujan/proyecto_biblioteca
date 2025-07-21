from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        orm_mode = True