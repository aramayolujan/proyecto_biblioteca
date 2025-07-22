from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

import models, schemas, crud, auth
from database import engine, SessionLocal
from dependencies import get_db

# Crear la base de datos
models.Base.metadata.create_all(bind=engine)

# Configurar OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Crear app FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI para que aparezca "Authorize" en Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Biblioteca",
        version="1.0.0",
        description="API con autenticación JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Endpoints

@app.post("/registro", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.obtener_usuario_por_nombre(usuario.nombre, db)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El nombre ya está registrado.")
    return crud.registrar_usuario(usuario, db)

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = auth.autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.crear_token(data={"sub": usuario.nombre})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/libros", response_model=schemas.LibroOut)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.crear_libro(libro, db)

@app.get("/libros", response_model=list[schemas.LibroOut])
def listar_libros(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.obtener_libros(db)

@app.get("/libros/{libro_id}", response_model=schemas.LibroOut)
def obtener_libro(libro_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    libro = crud.obtener_libro(libro_id, db)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.put("/libros/{libro_id}", response_model=schemas.LibroOut)
def actualizar_libro(libro_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    libro_actualizado = crud.actualizar_libro(libro_id, libro, db)
    if not libro_actualizado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro_actualizado

@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    libro = crud.eliminar_libro(libro_id, db)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"mensaje": "Libro eliminado correctamente"}
