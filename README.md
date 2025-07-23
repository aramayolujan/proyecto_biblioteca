# 📚 Proyecto Final - Sistema de Gestión de Biblioteca

Este proyecto es el resultado integrador del curso, y tiene como objetivo construir una API REST para la gestión de usuarios, libros y préstamos en una biblioteca. Se utilizaron tecnologías modernas como **FastAPI**, **SQLAlchemy** y **JWT**.

## 🚀 Tecnologías Utilizadas

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **JWT (JSON Web Tokens)**
- **Git y GitHub**
- **Swagger (para documentación y pruebas)**

---

## 🎯 Objetivo

Desarrollar una API funcional para:

- Registrar y autenticar usuarios con contraseña encriptada.
- Administrar libros con operaciones CRUD.
- Gestionar préstamos y devoluciones de libros.
- Proteger los endpoints sensibles con autenticación JWT.
- Validar que no se pueda prestar un libro ya prestado.


## 🔐 Autenticación

Se implementó autenticación **JWT**:

- `/registro`: Crea un nuevo usuario con contraseña hasheada.
- `/token`: Devuelve un token JWT tras login exitoso.

Los endpoints protegidos (como `/libros` y `/prestamos`) requieren autenticación vía token.

---

## 🔄 Endpoints

### 📌 Usuarios

- `POST /registro` → Crea usuario.
- `POST /token` → Login y obtención del token JWT.

### 📌 Libros (protegidos con JWT)

- `GET /libros` → Listar libros.
- `POST /libros` → Crear libro.
- `PUT /libros/{id}` → Actualizar libro.
- `DELETE /libros/{id}` → Eliminar libro.

### 📌 Préstamos (protegidos con JWT)

- `POST /prestamos` → Registrar un préstamo.
- `POST /devolver/{id}` → Devolver un libro.
- `GET /prestamos` → Listar todos los préstamos.
- `GET /mis-prestamos` → Listar préstamos activos del usuario autenticado.

---

## 🛡️ Validaciones Clave

- Un libro no puede prestarse si ya está en préstamo.
- Solo el usuario que realizó el préstamo puede devolverlo.
- Las contraseñas se almacenan en forma segura usando `bcrypt`.

---

⚙️ Instalación y Ejecución
Seguí estos pasos para levantar la API localmente:

Clonar el repositorio:
git clone https://github.com/aramayolujan/proyecto_biblioteca.git
cd proyecto_biblioteca

Crear un entorno virtual:
En Linux/macOS:
python -m venv venv
source venv/bin/activate
En Windows:
python -m venv venv
venv\Scripts\activate

Instalar las dependencias:
pip install -r requirements.txt

Ejecutar la aplicación:
uvicorn main:app --reload

Acceder a la documentación interactiva (Swagger UI):
Abrí tu navegador y visitá:
http://127.0.0.1:8000/docs

🧪 Pruebas
Usá la interfaz de Swagger para:

Registrar un nuevo usuario.

Autenticarse y obtener el token.

Clic en el botón “Authorize” e ingresar:
Bearer <tu_token_aquí>

Probar los endpoints.

📂 Se utilizó Git y GitHub durante todo el desarrollo.

Se excluyó la carpeta venv/ con .gitignore.

✅ Estado del Proyecto
✔ Registro y login
✔ JWT funcionando correctamente
✔ CRUD de libros
✔ Préstamos y devoluciones
✔ Validaciones implementadas
✔ Documentado en Swagger
✔ Proyecto subido a GitHub

🙋‍♀️ Autor
María Luján Aramayo
GitHub

