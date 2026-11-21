from app.calculations import BankAccount, InsufficientFunds, add, subtract, multiply, divide
import pytest


def test_basic_math():
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(3, 4) == 12
    assert divide(8, 2) == 4


def test_bank_account():
    account = BankAccount(100)
    account.deposit(50)
    account.withdraw(25)
    assert account.balance == 125
    account.collect_interest()
    assert account.balance == pytest.approx(137.5)
    with pytest.raises(InsufficientFunds):
        account.withdraw(1000)
