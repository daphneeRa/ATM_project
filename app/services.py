from typing import Dict, List
from decimal import Decimal, ROUND_HALF_UP
from app.models import AccountInfo, AccountNotFoundError, InsufficientFundsError
import logging

logger = logging.getLogger(__name__)

def convert_to_decimal(amount: float) -> Decimal:
    """Convert float to Decimal for precise calculations"""
    return Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def log_transaction(account_number: str, transaction_type: str, amount: Decimal, balance_before: Decimal, balance_after: Decimal):
    """Log transaction for audit purposes"""
    logger.info(
        f"Transaction: {transaction_type} | Account: {account_number} | "
        f"Amount: ${amount} | Balance: ${balance_before} -> ${balance_after}"
    )

class AccountService:
    """Service class to handle all account-related business logic"""
    
    def __init__(self):
        """Initialize with sample accounts"""
        # Import here to avoid circular import
        from main import SAMPLE_ACCOUNTS
        
        self.accounts = {}
        for account_num, account_data in SAMPLE_ACCOUNTS.items():
            self.accounts[account_num] = {
                'account_number': account_data['account_number'],
                'balance': convert_to_decimal(float(account_data['balance']))
            }
        logger.info(f"Initialized {len(self.accounts)} sample accounts")
    
    def account_exists(self, account_number: str) -> bool:
        """Check if an account exists"""
        return account_number in self.accounts
    
    def get_account(self, account_number: str) -> Dict:
        """Get account information"""
        if not self.account_exists(account_number):
            raise AccountNotFoundError(account_number)
        return self.accounts[account_number].copy()
    
    def get_balance(self, account_number: str) -> Decimal:
        """Get account balance"""
        account = self.get_account(account_number)
        return account['balance']
    
    def get_all_accounts(self) -> List[AccountInfo]:
        """Get all accounts information"""
        return [
            AccountInfo(
                account_number=account_data['account_number'],
                balance=float(account_data['balance'])
            )
            for account_data in self.accounts.values()
        ]
    
    def deposit(self, account_number: str, amount: float) -> Dict:
        """Deposit money into an account"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        deposit_amount = convert_to_decimal(amount)
        account = self.get_account(account_number)
        
        previous_balance = account['balance']
        new_balance = previous_balance + deposit_amount
        
        # Update account
        self.accounts[account_number]['balance'] = new_balance
        
        # Log transaction
        log_transaction(account_number, "deposit", deposit_amount, previous_balance, new_balance)
        
        return {
            "transaction_type": "deposit",
            "transaction_amount": float(deposit_amount),
            "previous_balance": float(previous_balance),
            "new_balance": float(new_balance)
        }
    
    def withdraw(self, account_number: str, amount: float) -> Dict:
        """Withdraw money from an account"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        withdraw_amount = convert_to_decimal(amount)
        account = self.get_account(account_number)
        
        previous_balance = account['balance']
        
        # Check sufficient funds
        if previous_balance < withdraw_amount:
            raise InsufficientFundsError(float(previous_balance), float(withdraw_amount))
        
        new_balance = previous_balance - withdraw_amount
        
        # Update account
        self.accounts[account_number]['balance'] = new_balance
        
        # Log transaction
        log_transaction(account_number, "withdrawal", withdraw_amount, previous_balance, new_balance)
        
        return {
            "transaction_type": "withdrawal",
            "transaction_amount": float(withdraw_amount),
            "previous_balance": float(previous_balance),
            "new_balance": float(new_balance)
        }

# Create singleton instance
account_service = AccountService()