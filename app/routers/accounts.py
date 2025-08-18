# app/routers/accounts.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import Account

router = APIRouter()

# In-memory "database" for demonstration purposes
accounts_db = {
    "123456789": {
        "account_id": "123456789",
        "account_name": "John Doe",
        "balance": 1000.00,
        "description": "Primary Checking"
    },
    "987654321": {
        "account_id": "987654321",
        "account_name": "Jane Smith",
        "balance": 500.50,
        "description": "Savings"
    },
    "112233445": {
        "account_id": "112233445",
        "account_name": "Michael Johnson",
        "balance": 250.75,
        "description": "Business Account"
    }
}

@router.post("/", response_model=Account)
async def create_account(account: Account):
    """Creates a new financial account."""
    if account.account_id in accounts_db:
        raise HTTPException(status_code=409, detail="Account ID already exists")
    accounts_db[account.account_id] = account
    return account

@router.get("/{account_id}", response_model=Account)
async def get_account(account_id: str):
    """Retrieves a specific financial account by its ID."""
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts_db[account_id]

@router.get("/", response_model=List[Account])
async def list_accounts():
    """Lists all available financial accounts."""
    return list(accounts_db.values())