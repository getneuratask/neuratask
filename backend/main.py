"""
NeuralTask Backend - Main entry point for the modular API
"""
import uvicorn
from src.adapters.drivers.api import create_app
app = create_app()

if __name__ == "__main__":
    # Run the modular API application
    uvicorn.run(
        "src.adapters.drivers.api.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )