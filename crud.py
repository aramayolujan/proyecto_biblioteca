from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_usuario_por_nombre(nombre: str, db: Session):
    return db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()

def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session):
    hashed_password = pwd_context.hash(usuario.contrasena)
    usuario_nuevo = models.Usuario(nombre=usuario.nombre, contrasena=hashed_password)
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)
    return usuario_nuevo

def crear_libro(libro: schemas.LibroCreate, db: Session):
    libro_nuevo = models.Libro(**libro.dict())
    db.add(libro_nuevo)
    db.commit()
    db.refresh(libro_nuevo)
    return libro_nuevo

def obtener_libros(db: Session):
    return db.query(models.Libro).all()

def obtener_libro(libro_id: int, db: Session):
    return db.query(models.Libro).filter(models.Libro.id == libro_id).first()

def actualizar_libro(libro_id: int, libro: schemas.LibroCreate, db: Session):
    db_libro = obtener_libro(libro_id, db)
    if not db_libro:
        return None
    for key, value in libro.dict().items():
        setattr(db_libro, key, value)
    db.commit()
    db.refresh(db_libro)
    return db_libro

def eliminar_libro(libro_id: int, db: Session):
    db_libro = obtener_libro(libro_id, db)
    if not db_libro:
        return None
    db.delete(db_libro)
    db.commit()
    return db_libro