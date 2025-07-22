from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuarioEntrada(BaseModel):
    nombre_usuario: str
    contrasena: str

class UsuarioSalida(BaseModel):
    id: int
    nombre_usuario: str
    class Config:
        orm_mode = True

class LoginEntrada(BaseModel):
    username: str
    password: str

class TokenSalida(BaseModel):
    access_token: str
    token_type: str

class LibroEntrada(BaseModel):
    titulo: str
    autor: str

class LibroSalida(LibroEntrada):
    id: int
    disponible: str
    class Config:
        orm_mode = True

class PrestamoEntrada(BaseModel):
    usuario_id: int
    libro_id: int

class PrestamoSalida(BaseModel):
    id: int
    usuario_id: int
    libro_id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime]
    class Config:
        orm_mode = True