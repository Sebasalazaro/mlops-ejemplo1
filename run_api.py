"""
API Server Startup Script

Runs the FastAPI application using uvicorn.
"""
import uvicorn
from config.settings import API_HOST, API_PORT, API_DEBUG, API_RELOAD


if __name__ == "__main__":
    uvicorn.run(
        "api.api:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD
    )
