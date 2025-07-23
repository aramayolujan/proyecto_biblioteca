# 📚 Proyecto Biblioteca - API REST con FastAPI

Este proyecto es una API para la gestión de usuarios, libros y préstamos en una biblioteca. Está construida con **FastAPI**, **SQLAlchemy** y **JWT** para autenticación, y permite realizar operaciones CRUD seguras.

---

## 🚀 Funcionalidades

- Registro de usuarios
- Login con generación de token JWT
- Gestión de libros (crear, consultar, modificar, eliminar)
- Gestión de préstamos (crear y devolver préstamo)
- Protección de endpoints con autenticación

---

## 📦 Tecnologías utilizadas

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite (modo local, reemplazable por otro motor)
- Passlib (hash de contraseñas)
- JWT (OAuth2PasswordBearer)

---

## ⚙️ Instalación y ejecución

1. **Cloná el repositorio**:
   ```bash
   git clone https://github.com/aramayolujan/proyecto_biblioteca.git
   cd proyecto_biblioteca
