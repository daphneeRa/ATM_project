# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, accounts
import uvicorn
import os
import logging
from app.services import account_service  # Import service with sample accounts

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    APP_NAME = "ATM System API"
    VERSION = "1.0.0"
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 8000))
    DEBUG = os.environ.get("ENVIRONMENT", "development") == "development"

# Create FastAPI app
app = FastAPI(
    title=Config.APP_NAME,
    version=Config.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(accounts.router)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"{Config.APP_NAME} is starting up!")
    logger.info(f"API Documentation: http://localhost:{Config.PORT}/docs")
    logger.info(f"ReDoc Documentation: http://localhost:{Config.PORT}/redoc")
    logger.info("\nSample accounts available:")
    for acc_num, acc_data in account_service.accounts.items():
        logger.info(f"   - Account: {acc_num} (Balance: ${acc_data['balance']})")

# Run the app
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # <-- note the module path
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )
