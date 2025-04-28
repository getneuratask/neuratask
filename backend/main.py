import uvicorn
from src.adapters.drivers.api import app

if __name__ == "__main__":
    uvicorn.run("src.adapters.drivers.api:app", host="0.0.0.0", port=8000, reload=True)