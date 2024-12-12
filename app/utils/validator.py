import re
from decimal import Decimal

from fastapi import HTTPException

from app.config.settings import get_settings
from app.interfaces.dock_account import DockAccountInterface
from app.repositories.transaction_history_repository import TransactionHistoryRepository


def validate_cpf(cpf: str) -> bool | str:
    """
    Validates if a CPF is valid or not.

    :param cpf: CPF in string format (with or without punctuation)
    :return: True if the CPF is valid, False otherwise
    """
    # Remove non-numeric characters
    cpf = re.sub("[^0-9]","", cpf)

    # Check if the CPF has 11 digits or is a repeated sequence
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Calculate the CPF digits
    calc = [i for i in range(1, 10)]
    d1 = (sum([int(a) * b for a, b in zip(cpf[:-2], calc)]) % 11) % 10
    d2 = (sum([int(a) * b for a, b in zip(reversed(cpf[:-2]), calc)]) % 11) % 10

    # Check if the calculated digits match the given ones
    if str(d1) == cpf[-2] and str(d2) == cpf[-1]:
        return cpf
    return False

def withdrawal_validation(dock_account: DockAccountInterface, amount: Decimal):
    """
    Validates if a withdrawal can be done to a particular account.

    :param dock_account: Dock digital account info
    :param amount: amount to withdraw from the account
    """
    def validate_amount():
        """
        Validates if the withdrawal amount is not negative.
        """
        return amount > 0

    def validate_balance():
        """
        Validates if the account has sufficient balance to withdraw.
        """
        return dock_account.balance >= amount

    def validate_daily_limit():
        """
        Validates if the daily withdrawal limit has been exceeded.
        """
        _settings = get_settings()
        _repository = TransactionHistoryRepository()
        daily_withdrawal_amount = _repository.daily_withdrawal_amount(dock_account_id=dock_account.id)
        return _settings.maximum_daily_limit >= (daily_withdrawal_amount + amount)

    if not validate_amount():
        raise HTTPException(status_code=422, detail="Invalid withdrawal amount")

    if not validate_balance():
        raise HTTPException(status_code=422, detail="DockAccount has no sufficient balance")

    if not validate_daily_limit():
        raise HTTPException(status_code=422, detail="Daily withdrawal limit exceeded")
