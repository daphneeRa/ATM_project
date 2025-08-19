from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, accounts
import uvicorn
import os
import logging

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

# Sample accounts data
SAMPLE_ACCOUNTS = {
    '12345': {'account_number': '12345', 'balance': '1000.00'},
    '67890': {'account_number': '67890', 'balance': '2500.50'},
    '11111': {'account_number': '11111', 'balance': '0.00'}
}

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
    for acc_num, acc_data in SAMPLE_ACCOUNTS.items():
        logger.info(f"   - Account: {acc_num} (Balance: ${acc_data['balance']})")

# Run the app
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )