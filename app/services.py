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

# In-memory data
SAMPLE_ACCOUNTS = {
    '12345': {'account_number': '12345', 'balance': '1000.00'},
    '67890': {'account_number': '67890', 'balance': '2500.50'},
    '11111': {'account_number': '11111', 'balance': '0.00'},
    '22222': {'account_number': '22222', 'balance': '150.75'},
    '33333': {'account_number': '33333', 'balance': '3200.00'},
    '44444': {'account_number': '44444', 'balance': '500.50'},
    '55555': {'account_number': '55555', 'balance': '750.25'},
    '66666': {'account_number': '66666', 'balance': '1200.00'},
    '77777': {'account_number': '77777', 'balance': '0.00'},
    '88888': {'account_number': '88888', 'balance': '9999.99'}
}


class AccountService:
    """Service class to handle all account utils"""
    
    def __init__(self):
        """Initialize with sample accounts"""        
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
        self.accounts[account_number]['balance'] = new_balance
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
        self.accounts[account_number]['balance'] = new_balance
        log_transaction(account_number, "withdrawal", withdraw_amount, previous_balance, new_balance)
        
        return {
            "transaction_type": "withdrawal",
            "transaction_amount": float(withdraw_amount),
            "previous_balance": float(previous_balance),
            "new_balance": float(new_balance)
        }

# Create instance
account_service = AccountService()