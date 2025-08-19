from fastapi import APIRouter, HTTPException
from app.models import (
    TransactionRequest, BalanceResponse, TransactionResponse, 
    AccountListResponse, ErrorResponse, ATMException
)
from app.services import account_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/accounts", tags=["Account Operations"])

def handle_atm_exception(exc: ATMException) -> HTTPException:
    """Convert ATM exception to HTTP exception"""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details
        }
    )

@router.get("", response_model=AccountListResponse)
async def get_all_accounts():
    """Get all accounts (for debugging purposes)"""
    try:
        accounts = account_service.get_all_accounts()
        return AccountListResponse(
            total_accounts=len(accounts),
            accounts=accounts
        )
    except Exception as e:
        logger.error(f"Error retrieving accounts: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Internal server error", "error_code": "INTERNAL_ERROR"}
        )

@router.get(
    "/{account_number}/balance", 
    response_model=BalanceResponse,
    responses={404: {"model": ErrorResponse}}
)
async def get_balance(account_number: str):
    """Get account balance"""
    try:
        balance = account_service.get_balance(account_number)
        return BalanceResponse(account_number=account_number, balance=float(balance))
    
    except ATMException as e:
        logger.warning(f"ATM error in get_balance: {e.message}")
        raise handle_atm_exception(e)
    
    except Exception as e:
        logger.error(f"Unexpected error in get_balance: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Internal server error", "error_code": "INTERNAL_ERROR"}
        )

@router.post(
    "/{account_number}/deposit",
    response_model=TransactionResponse,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def deposit_money(account_number: str, transaction: TransactionRequest):
    """Deposit money into an account"""
    try:
        result = account_service.deposit(account_number, transaction.amount)
        
        return TransactionResponse(
            message="Deposit successful",
            account_number=account_number,
            **result
        )
        
    except ATMException as e:
        logger.warning(f"ATM error in deposit: {e.message}")
        raise handle_atm_exception(e)
    
    except ValueError as e:
        logger.warning(f"Validation error in deposit: {e}")
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": str(e), "error_code": "VALIDATION_ERROR"}
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in deposit: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Internal server error", "error_code": "INTERNAL_ERROR"}
        )

@router.post(
    "/{account_number}/withdraw",
    response_model=TransactionResponse,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def withdraw_money(account_number: str, transaction: TransactionRequest):
    """Withdraw money from an account"""
    try:
        result = account_service.withdraw(account_number, transaction.amount)
        
        return TransactionResponse(
            message="Withdrawal successful",
            account_number=account_number,
            **result
        )
        
    except ATMException as e:
        logger.warning(f"ATM error in withdraw: {e.message}")
        raise handle_atm_exception(e)
    
    except ValueError as e:
        logger.warning(f"Validation error in withdraw: {e}")
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": str(e), "error_code": "VALIDATION_ERROR"}
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in withdraw: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Internal server error", "error_code": "INTERNAL_ERROR"}
        )