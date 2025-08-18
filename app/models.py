# app/models.py
from pydantic import BaseModel
from typing import Optional, List

# Pydantic model for an Account
class Account(BaseModel):
    account_id: str
    account_name: str
    balance: float
    description: Optional[str] = None