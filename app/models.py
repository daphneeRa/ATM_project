from pydantic import BaseModel, field_validator, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

#################### REQUEST MODELS ####################

class TransactionRequest(BaseModel):
    """Request model for deposit and withdraw operations"""
    amount: float = Field(
        ..., 
        gt=0, 
        description="Amount must be greater than 0",
        example=100.50
    )
    
    @field_validator('amount')
    def validate_amount_precision(cls, v):
        """Ensure amount has at most 2 decimal places"""
        if round(v, 2) != v:
            raise ValueError('Amount can have at most 2 decimal places')
        return v
    
    @field_validator('amount')
    def validate_reasonable_amount(cls, v):
        """Ensure amount is reasonable (not too large)"""
        if v > 1_000_000:  
            raise ValueError('Amount cannot exceed $1,000,000 per transaction')
        return v

#################### RESPONSE MODELS ####################

class BaseResponse(BaseModel):
    """Base response model with common fields"""
    success: bool = Field(default=True, description="Indicates if the operation was successful")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

class ErrorResponse(BaseResponse):
    """Standard error response model"""
    success: bool = Field(default=False)
    message: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code for programmatic handling")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")

class HealthResponse(BaseResponse):
    """Health check response model"""
    message: str = Field(..., example="ATM System API is running")
    version: str = Field(..., example="1.0.0")
    endpoints: Dict[str, str] = Field(..., description="Available API endpoints")
    sample_accounts: List[str] = Field(..., description="Sample account numbers for testing")

class AccountInfo(BaseModel):
    """Account information model"""
    account_number: str = Field(..., description="Account number")
    balance: float = Field(..., description="Current account balance")

class BalanceResponse(BaseResponse):
    """Balance inquiry response model"""
    account_number: str = Field(..., description="Account number")
    balance: float = Field(..., description="Current account balance", example=1000.00)

class TransactionResponse(BaseResponse):
    """Transaction response model for deposits and withdrawals"""
    message: str = Field(..., description="Transaction result message")
    account_number: str = Field(..., description="Account number")
    transaction_type: str = Field(..., description="Type of transaction (deposit/withdrawal)")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    previous_balance: float = Field(..., description="Balance before transaction")
    new_balance: float = Field(..., description="Balance after transaction")

class AccountListResponse(BaseResponse):
    """Response model for listing all accounts"""
    total_accounts: int = Field(..., description="Total number of accounts")
    accounts: List[AccountInfo] = Field(..., description="List of account information")

#################### EXCEPTION CLASSES ####################

class ATMException(Exception):
    """Base exception for ATM operations"""
    def __init__(self, message: str, error_code: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class AccountNotFoundError(ATMException):
    """Raised when an account is not found"""
    def __init__(self, account_number: str):
        super().__init__(
            message=f"Account {account_number} not found",
            error_code="ACCOUNT_NOT_FOUND",
            status_code=404,
            details={"account_number": account_number}
        )

class InsufficientFundsError(ATMException):
    """Raised when account has insufficient funds for withdrawal"""
    def __init__(self, current_balance: float, requested_amount: float):
        shortfall = requested_amount - current_balance
        super().__init__(
            message=f"Insufficient funds. Available: ${current_balance:.2f}, Requested: ${requested_amount:.2f}",
            error_code="INSUFFICIENT_FUNDS",
            status_code=400,
            details={
                "current_balance": current_balance,
                "requested_amount": requested_amount,
                "shortfall": shortfall
            }
        )