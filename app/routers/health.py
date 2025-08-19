from fastapi import APIRouter
from app.models import HealthResponse
from app.services import account_service

router = APIRouter(tags=["Health Check"])

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with API information"""
    from main import Config  # Import here to avoid circular import
    
    return HealthResponse(
        message=f"{Config.APP_NAME} is running",
        version=Config.VERSION,
        endpoints={
            "health": "GET /",
            "get_balance": "GET /accounts/{account_number}/balance",
            "withdraw": "POST /accounts/{account_number}/withdraw", 
            "deposit": "POST /accounts/{account_number}/deposit",
            "get_all_accounts": "GET /accounts",
            "api_docs": "GET /docs",
            "redoc_docs": "GET /redoc"
        },
        sample_accounts=[account.account_number for account in account_service.get_all_accounts()]
    )