from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from base_datos import SessionLocal, engine
import modelos, esquemas, seguridad
from seguridad import verificar_contrasena, hashear_contrasena, crear_token, decodificar_token
from datetime import datetime

modelos.Base.metadata.create_all(bind=engine)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = decodificar_token(token)
        return payload.get("sub")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

@router.post("/registro", response_model=esquemas.UsuarioSalida)
def registro(usuario: esquemas.UsuarioEntrada, db: Session = Depends(get_db)):
    db_usuario = modelos.Usuario(nombre_usuario=usuario.nombre_usuario, contrasena=hashear_contrasena(usuario.contrasena))
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.post("/token", response_model=esquemas.TokenSalida)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(modelos.Usuario).filter(modelos.Usuario.nombre_usuario == form_data.username).first()
    if not usuario or not verificar_contrasena(form_data.password, usuario.contrasena):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    token = crear_token({"sub": usuario.nombre_usuario})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/libros", response_model=esquemas.LibroSalida)
def crear_libro(libro: esquemas.LibroEntrada, db: Session = Depends(get_db), usuario: str = Depends(obtener_usuario_actual)):
    db_libro = modelos.Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

@router.get("/libros", response_model=list[esquemas.LibroSalida])
def listar_libros(db: Session = Depends(get_db), usuario: str = Depends(obtener_usuario_actual)):
    return db.query(modelos.Libro).all()

@router.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db), usuario: str = Depends(obtener_usuario_actual)):
    libro = db.query(modelos.Libro).get(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(libro)
    db.commit()
    return {"mensaje": "Libro eliminado"}

@router.post("/prestamos", response_model=esquemas.PrestamoSalida)
def crear_prestamo(p: esquemas.PrestamoEntrada, db: Session = Depends(get_db), usuario: str = Depends(obtener_usuario_actual)):
    prestamo = modelos.Prestamo(**p.dict())
    libro = db.query(modelos.Libro).get(p.libro_id)
    if libro:
        libro.disponible = "no"
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo

@router.post("/prestamos/{prestamo_id}/devolver")
def devolver_prestamo(prestamo_id: int, db: Session = Depends(get_db), usuario: str = Depends(obtener_usuario_actual)):
    prestamo = db.query(modelos.Prestamo).get(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    prestamo.fecha_devolucion = datetime.utcnow()
    libro = db.query(modelos.Libro).get(prestamo.libro_id)
    if libro:
        libro.disponible = "si"
    db.commit()
    return {"mensaje": "Libro devuelto correctamente"}