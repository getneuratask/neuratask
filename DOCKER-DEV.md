# Configuración Docker para Desarrollo - NeuraTask

## Archivos Configurados

### 1. `.env` Principal
- Variables de entorno centralizadas
- Configuración para usar base de datos Neon Tech
- Puertos y configuraciones de desarrollo

### 2. Dockerfiles

#### Backend (`backend/dockerfile`)
- Python 3.12-slim
- Variables de entorno para desarrollo (FLASK_ENV=development, DEBUG=true)
- Hot reload habilitado
- Puerto: 8000

#### Frontend (`frontend/Dockerfile`)
- Node.js 20-alpine
- Servidor de desarrollo Vite con hot reload
- Host configurado para 0.0.0.0 (accesible desde contenedor)
- Puerto: 3000

#### IA Services (`ia-services/Dockerfile`)
- Python 3.12-slim
- Configuración de desarrollo con DEBUG=true
- Puerto: 47337

### 3. `docker-compose.yml`
- Configuración optimizada para desarrollo
- Variables de entorno cargadas desde `.env`
- Volúmenes para hot reload
- Red personalizada para comunicación entre servicios

## Comandos para Desarrollo

### Construir y ejecutar todos los servicios:
```bash
docker-compose up --build
```

### Ejecutar en background:
```bash
docker-compose up --build -d
```

### Ver logs de un servicio específico:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ia-services
```

### Parar todos los servicios:
```bash
docker-compose down
```

### Limpiar y reconstruir:
```bash
docker-compose down --volumes --remove-orphans
docker-compose up --build
```

## Puertos de Desarrollo

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **IA Services**: http://localhost:47337

## Características de Desarrollo

### Hot Reload Habilitado
- **Frontend**: Vite con polling para detectar cambios en archivos
- **Backend**: Flask en modo desarrollo con auto-reload
- **IA Services**: Python con reload automático

### Volúmenes de Desarrollo
- Código fuente montado para cambios en tiempo real
- `node_modules` y `__pycache__` excluidos para evitar conflictos

### Variables de Entorno
- Base de datos: Neon Tech (desarrollo)
- Debug habilitado en todos los servicios
- Configuración de desarrollo por defecto

## Notas Importantes

1. **Base de Datos**: Usando Neon Tech en lugar de PostgreSQL local para desarrollo
2. **Hot Reload**: Todos los servicios se recargan automáticamente al detectar cambios
3. **Debugging**: Variables DEBUG=true habilitadas
4. **Red**: Servicios pueden comunicarse entre sí usando los nombres de servicio
5. **Volúmenes**: Cambios en código se reflejan inmediatamente sin reconstruir

## Solución de Problemas

Si encuentras el error "Network needs to be recreated":
```bash
docker-compose down --volumes --remove-orphans
docker network prune -f
docker-compose up --build
```

## ✅ Estado Actual del Entorno de Desarrollo

### Verificación Completada (Junio 6, 2025)

**Todos los servicios están funcionando correctamente:**

1. **Frontend (React + Vite)**
   - ✅ Contenedor ejecutándose en puerto 3000
   - ✅ Vite dev server activo con hot-reload
   - ✅ Accesible en http://localhost:3000
   - ✅ HMR (Hot Module Replacement) verificado y funcionando

2. **Backend (Python + FastAPI/Flask)**
   - ✅ Contenedor ejecutándose en puerto 8000
   - ✅ API respondiendo correctamente
   - ✅ Auto-reload habilitado para desarrollo
   - ✅ Accesible en http://localhost:8000

3. **IA Services**
   - ✅ Contenedor ejecutándose en puerto 47337
   - ✅ Servicio activo y funcionando

### Flujo de Desarrollo Verificado

- **Hot-reloading**: Cambios en archivos se reflejan automáticamente
- **Container orchestration**: Docker Compose gestiona todos los servicios
- **Network connectivity**: Servicios pueden comunicarse entre sí
- **Volume mounting**: Código fuente sincronizado con contenedores

### Comandos de Uso Diario

```bash
# Iniciar todos los servicios
docker-compose up

# Iniciar en background
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar un servicio específico
docker-compose restart frontend

# Parar todos los servicios
docker-compose down
```

### Configuración Optimizada

- **Vite Config**: Configurado para Docker con host 0.0.0.0 y puerto 5173
- **Docker Compose**: Sintaxis compatible sin características experimentales
- **Environment**: Variables de entorno centralizadas en `.env`
- **Development**: Modo desarrollo habilitado en todos los servicios
