# NeuraTask Backend

Este es el backend del proyecto NeuraTask, una aplicación de gestión de tareas construida con FastAPI y PostgreSQL.

## Requisitos del Sistema

### Python
- Python 3.12 o superior
- pip (gestor de paquetes de Python)

### Base de Datos
- PostgreSQL 14.0 o superior

### Dependencias del Sistema
Para Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3-dev libpq-dev build-essential
```

Para macOS (usando Homebrew):
```bash
brew install postgresql python
```

## Configuración del Entorno

1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
cd neuratask
```

2. Crear un entorno virtual:
```bash
python -m venv .venv
```

3. Activar el entorno virtual:

Para Linux/macOS:
```bash
source .venv/bin/activate
```

Para Windows:
```bash
.venv\Scripts\activate
```

4. Instalar las dependencias:
```bash
cd backend
pip install -r requirements.txt
```

## Configuración de la Base de Datos

1. Crear una base de datos PostgreSQL
2. Configurar las variables de entorno:

Crear un archivo `.env` en la carpeta `backend` con el siguiente contenido:
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_base_datos
```

3. Ejecutar el script de schema:
```bash
psql -U usuario -d nombre_base_datos -f db/schema.sql
```

## Ejecutar el Backend

1. Asegurarse de estar en el directorio backend:
```bash
cd backend
```

2. Iniciar el servidor:
```bash
python main.py
```

El servidor se iniciará en `http://localhost:8000`

## Documentación API

Una vez que el servidor esté corriendo, puedes acceder a:

- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

## Estructura del Proyecto

El backend sigue una arquitectura hexagonal (ports & adapters):

- `src/adapters/`: Implementaciones concretas de los puertos
  - `driven/`: Repositorios y servicios externos
  - `drivers/`: API y controladores
- `src/domain/`: Lógica de negocio y entidades
- `src/ports/`: Interfaces y contratos
- `tests/`: Tests unitarios y de integración

## Desarrollo

El servidor se ejecuta con recarga automática en modo desarrollo, lo que significa que cualquier cambio en el código fuente provocará un reinicio automático del servidor.

## Versiones de Dependencias

Las principales dependencias y sus versiones son:
- FastAPI: 0.104.1
- Pydantic: 2.4.2
- SQLAlchemy: Incluida en requirements.txt
- Uvicorn: 0.23.2
- PostgreSQL (psycopg2-binary): 2.9.10

Para ver la lista completa de dependencias y sus versiones, consulta el archivo `backend/requirements.txt`.
