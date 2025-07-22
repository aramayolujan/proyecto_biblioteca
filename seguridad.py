from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 60
SECRET_KEY = "clave_secreta"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contrasena(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hashear_contrasena(password):
    return pwd_context.hash(password)

def crear_token(payload: dict):
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])