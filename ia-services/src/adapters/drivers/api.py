from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.adapters.drivers.chatbot_router import router as chatbot_router

app = FastAPI(
    title="NeuraTask AI Services",
    description="AI Services for NeuraTask",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir el router del chatbot
app.include_router(chatbot_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-services", "version": "1.0.0"}