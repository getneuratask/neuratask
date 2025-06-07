# NeuralTask API Documentation

## Descripción General

Esta API REST completa proporciona todos los endpoints necesarios para gestionar el sistema de tareas NeuralTask. Incluye gestión de usuarios, espacios de trabajo, proyectos, tareas, etiquetas, comentarios, recordatorios y logs de actividad.

## Configuración y Despliegue

### Desarrollo Local

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar base de datos:**
   - PostgreSQL debe estar ejecutándose
   - Configurar parámetros de conexión en `DB_PARAMS` en `api.py`

3. **Ejecutar la aplicación:**
   ```bash
   # Desde el directorio backend
   python main.py
   ```

4. **Acceder a la documentación:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Despliegue con Docker

```bash
# Desde el directorio raíz del proyecto
docker-compose up --build
```

## Arquitectura de la API

La API sigue una arquitectura hexagonal (ports & adapters) con las siguientes capas:

- **API Layer**: FastAPI endpoints y DTOs
- **Service Layer**: Lógica de negocio
- **Repository Layer**: Acceso a datos
- **Domain Layer**: Entidades y modelos

## Endpoints por Servicio

### 🏥 Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Verificar estado de la API |
| GET | `/` | Información general de la API |

### 👥 Usuarios (Users)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users` | Obtener todos los usuarios |
| GET | `/users/{user_id}` | Obtener usuario por ID |
| GET | `/users/auth0/{auth0_sub}` | Obtener usuario por Auth0 subject |
| GET | `/users/email/{email}` | Obtener usuario por email |
| POST | `/users` | Crear nuevo usuario |
| PUT | `/users/{user_id}` | Actualizar usuario |
| DELETE | `/users/{user_id}` | Eliminar usuario |

### 🏢 Espacios de Trabajo (Workspaces)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/workspaces` | Obtener todos los espacios de trabajo |
| GET | `/workspaces/{workspace_id}` | Obtener espacio por ID |
| GET | `/users/{owner_id}/workspaces` | Obtener espacios por propietario |
| POST | `/workspaces` | Crear nuevo espacio de trabajo |
| PUT | `/workspaces/{workspace_id}` | Actualizar espacio de trabajo |
| DELETE | `/workspaces/{workspace_id}` | Eliminar espacio de trabajo |

### 📁 Proyectos (Projects)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/projects` | Obtener todos los proyectos |
| GET | `/projects/{project_id}` | Obtener proyecto por ID |
| GET | `/workspaces/{workspace_id}/projects` | Obtener proyectos por espacio |
| GET | `/workspaces/{workspace_id}/projects/active` | Obtener proyectos activos |
| POST | `/projects` | Crear nuevo proyecto |
| PUT | `/projects/{project_id}` | Actualizar proyecto |
| DELETE | `/projects/{project_id}` | Eliminar proyecto |

### ✅ Tareas (Tasks)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tasks` | Obtener todas las tareas |
| GET | `/tasks/{task_id}` | Obtener tarea por ID |
| GET | `/projects/{project_id}/tasks` | Obtener tareas por proyecto |
| GET | `/users/{user_id}/tasks` | Obtener tareas asignadas a usuario |
| GET | `/tasks/{parent_task_id}/subtasks` | Obtener subtareas |
| POST | `/tasks` | Crear nueva tarea |
| PUT | `/tasks/{task_id}` | Actualizar tarea |
| DELETE | `/tasks/{task_id}` | Eliminar tarea |

### 🏷️ Etiquetas (Labels)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/labels` | Obtener todas las etiquetas |
| GET | `/labels/{label_id}` | Obtener etiqueta por ID |
| GET | `/workspaces/{workspace_id}/labels` | Obtener etiquetas por espacio |
| GET | `/tasks/{task_id}/labels` | Obtener etiquetas por tarea |
| POST | `/labels` | Crear nueva etiqueta |
| PUT | `/labels/{label_id}` | Actualizar etiqueta |
| DELETE | `/labels/{label_id}` | Eliminar etiqueta |

### 💬 Comentarios (Comments)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/comments` | Obtener todos los comentarios |
| GET | `/comments/{comment_id}` | Obtener comentario por ID |
| GET | `/tasks/{task_id}/comments` | Obtener comentarios por tarea |
| GET | `/users/{author_id}/comments` | Obtener comentarios por autor |
| POST | `/comments` | Crear nuevo comentario |
| PUT | `/comments/{comment_id}` | Actualizar comentario |
| DELETE | `/comments/{comment_id}` | Eliminar comentario |

### ⏰ Recordatorios (Reminders)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/reminders` | Obtener todos los recordatorios |
| GET | `/reminders/{reminder_id}` | Obtener recordatorio por ID |
| GET | `/tasks/{task_id}/reminders` | Obtener recordatorios por tarea |
| GET | `/users/{user_id}/reminders` | Obtener recordatorios por usuario |
| GET | `/reminders/pending` | Obtener recordatorios pendientes |
| POST | `/reminders` | Crear nuevo recordatorio |
| PUT | `/reminders/{reminder_id}` | Actualizar recordatorio |
| DELETE | `/reminders/{reminder_id}` | Eliminar recordatorio |

### 📊 Logs de Actividad (Activity Logs)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/activity-logs` | Obtener todos los logs |
| GET | `/activity-logs/{activity_id}` | Obtener log por ID |
| GET | `/activity-logs/entity/{entity_type}/{entity_id}` | Obtener logs por entidad |
| GET | `/users/{actor_id}/activity-logs` | Obtener logs por actor |
| POST | `/activity-logs` | Crear nuevo log |
| DELETE | `/activity-logs/{activity_id}` | Eliminar log |

## Modelos de Datos

### DTOs de Entrada

Cada endpoint POST/PUT utiliza DTOs específicos que contienen solo los campos necesarios:

- `TaskCreateDTO`: Para crear tareas
- `TaskUpdateDTO`: Para actualizar tareas
- `UserCreateDTO`: Para crear usuarios
- `UserUpdateDTO`: Para actualizar usuarios
- Y así para cada entidad...

### Entidades de Respuesta

Las respuestas utilizan las entidades del dominio:

- `Task`: Entidad completa de tarea
- `User`: Entidad completa de usuario
- `Workspace`: Entidad completa de espacio de trabajo
- `Project`: Entidad completa de proyecto
- `Label`: Entidad completa de etiqueta
- `Comment`: Entidad completa de comentario
- `Reminder`: Entidad completa de recordatorio
- `ActivityLog`: Entidad completa de log de actividad

## Características Principales

### ✅ Funcionalidades Implementadas

- **Documentación automática** con Swagger UI y ReDoc
- **Validación de datos** con Pydantic
- **Manejo de errores** con códigos HTTP apropiados
- **CORS** configurado para desarrollo
- **Arquitectura limpia** con separación de responsabilidades
- **Inyección de dependencias** para servicios
- **DTOs específicos** para operaciones de creación/actualización
- **Endpoints RESTful** bien estructurados
- **Logging de actividad** para auditoría

### 🔧 Configuración

La configuración de la base de datos se encuentra en la variable `DB_PARAMS`:

```python
DB_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "database": "neuratask",
    "user": "postgres",
    "password": "postgres"
}
```

### 🚀 Despliegue en Producción

Para producción, considera:

1. **Variables de entorno** para configuración sensible
2. **HTTPS** obligatorio
3. **Rate limiting** para prevenir abuso
4. **Autenticación/Autorización** (Auth0 integration)
5. **Monitoring** y logging
6. **Health checks** avanzados

## Ejemplos de Uso

### Crear una nueva tarea

```bash
curl -X POST "http://localhost:8000/tasks?created_by=uuid-here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nueva tarea",
    "description": "Descripción de la tarea",
    "project_id": "project-uuid-here",
    "priority": 3,
    "due_date": "2025-12-31"
  }'
```

### Obtener tareas de un proyecto

```bash
curl -X GET "http://localhost:8000/projects/{project_id}/tasks"
```

### Actualizar estado de una tarea

```bash
curl -X PUT "http://localhost:8000/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "DONE"
  }'
```

## Contribución

1. La API sigue principios REST
2. Todos los endpoints están documentados
3. Se utilizan códigos de estado HTTP apropiados
4. Los errores devuelven mensajes descriptivos
5. La validación de datos es automática con Pydantic

## Notas de Desarrollo

- Usar UUIDs para todos los identificadores
- Los timestamps se manejan automáticamente
- Las relaciones se manejan por IDs de referencia
- Todos los endpoints están agrupados por tags para mejor organización en la documentación
