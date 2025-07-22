from pydantic import BaseModel

# Usuario
class UsuarioCreate(BaseModel):
    nombre: str
    contrasena: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

# Libro
class LibroCreate(BaseModel):
    titulo: str
    autor: str

class LibroOut(LibroCreate):
    id: int
    disponible: bool = True

    class Config:
        from_attributes = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str