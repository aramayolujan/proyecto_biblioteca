from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import models

SECRET_KEY = "tu_clave_secreta_supersegura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contrasena(contrasena_plana, contrasena_hash):
    return pwd_context.verify(contrasena_plana, contrasena_hash)

def autenticar_usuario(db, nombre: str, contrasena: str):
    usuario = db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()
    if not usuario or not verificar_contrasena(contrasena, usuario.contrasena):
        return None
    return usuario

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt