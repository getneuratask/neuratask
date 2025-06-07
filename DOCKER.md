# NeuraTask Docker Setup

This document explains how to run the NeuraTask application using Docker and Docker Compose.

## Prerequisites

- Docker
- Docker Compose
- Git

## Services

The application consists of 4 services:

1. **postgres**: PostgreSQL database
2. **backend**: FastAPI backend service (Python)
3. **ia-services**: AI services (Python FastAPI)
4. **frontend**: React frontend (Node.js/Vite)

## Quick Start

1. Clone the repository and navigate to the project directory:
```bash
cd /home/kuaik/Documents/projects/neuratask
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Edit the `.env` file and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
```

4. Build and start all services:
```bash
docker-compose up --build
```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - AI Services API: http://localhost:47337
   - PostgreSQL: localhost:5432

## Development Mode

For development with hot reload:

```bash
docker-compose up --build
```

The volumes are mounted so changes to your code will be reflected in the containers.

## Useful Commands

- **Start services in background**: `docker-compose up -d`
- **Stop services**: `docker-compose down`
- **View logs**: `docker-compose logs [service_name]`
- **Rebuild specific service**: `docker-compose build [service_name]`
- **Execute command in container**: `docker-compose exec [service_name] [command]`

## Database

The PostgreSQL database is automatically initialized with the schema from `backend/db/schema.sql` when the container starts for the first time.

## Environment Variables

Key environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key for AI services
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database configuration
- Backend runs on port 8000
- Frontend runs on port 3000 (served via nginx)
- AI Services run on port 47337

## Troubleshooting

1. **Port conflicts**: Make sure ports 3000, 8000, 47337, and 5432 are available
2. **Database connection issues**: Wait for PostgreSQL to be fully initialized
3. **Build issues**: Try `docker-compose down` and `docker-compose up --build --force-recreate`
