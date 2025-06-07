"""
Main API application assembly - combines all modular routers
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routers
from src.adapters.drivers.api.users import router as users_router
from src.adapters.drivers.api.workspaces import router as workspaces_router
from src.adapters.drivers.api.projects import router as projects_router
from src.adapters.drivers.api.tasks import router as tasks_router
from src.adapters.drivers.api.labels import router as labels_router
from src.adapters.drivers.api.comments import router as comments_router
from src.adapters.drivers.api.reminders import router as reminders_router
from src.adapters.drivers.api.activity_logs import router as activity_logs_router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title="NeuralTask API",
        description="Complete task management system API with modular architecture",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register all routers
    app.include_router(users_router, prefix="/api/v1", tags=["Users"])
    app.include_router(workspaces_router, prefix="/api/v1", tags=["Workspaces"])
    app.include_router(projects_router, prefix="/api/v1", tags=["Projects"])
    app.include_router(tasks_router, prefix="/api/v1", tags=["Tasks"])
    app.include_router(labels_router, prefix="/api/v1", tags=["Labels"])
    app.include_router(comments_router, prefix="/api/v1", tags=["Comments"])
    app.include_router(reminders_router, prefix="/api/v1", tags=["Reminders"])
    app.include_router(activity_logs_router, prefix="/api/v1", tags=["Activity Logs"])

    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint - API health check"""
        return {
            "message": "NeuralTask API is running",
            "version": "1.0.0",
            "status": "healthy",
            "documentation": "/docs"
        }

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "timestamp": "2025-06-07T00:00:00Z",
            "services": [
                "users", "workspaces", "projects", "tasks", 
                "labels", "comments", "reminders", "activity_logs"
            ]
        }

    return app

# Create the app instance
app = create_app()
