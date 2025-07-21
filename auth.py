from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

import models
import schemas
from database import SessionLocal

# Secret key para firmar el JWT
SECRET_KEY = "mi_clave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Para login vía /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Otras funciones 

def verificar_contraseña(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hashear_contraseña(password):
    return pwd_context.hash(password)

def crear_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def obtener_usuario(db: Session, nombre: str):
    return db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()

# Registro de usuarios

def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session):
    usuario_existente = obtener_usuario(db, usuario.nombre)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Nombre ya registrado")
    
    hashed_password = hashear_contraseña(usuario.contraseña)
    nuevo_usuario = models.Usuario(nombre=usuario.nombre, contraseña=hashed_password)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Login

def autenticar_usuario(nombre: str, contraseña: str, db: Session):
    usuario = obtener_usuario(db, nombre)
    if not usuario or not verificar_contraseña(contraseña, usuario.contraseña):
        return False
    return usuario

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nombre: str = payload.get("sub")
        if nombre is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = obtener_usuario(db, nombre)
    if usuario is None:
        raise credentials_exception
    return usuario

