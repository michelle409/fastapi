"""Small arithmetic and account examples retained from the course project."""


def add(num1: int, num2: int = 2) -> int:
    return num1 + num2


def subtract(num1: int, num2: int) -> int:
    return num1 - num2


def multiply(num1: int, num2: int) -> int:
    return num1 * num2


def divide(num1: float, num2: float) -> float:
    if num2 == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return num1 / num2


class InsufficientFunds(Exception):
    pass


class BankAccount:
    def __init__(self, starting_balance: float = 0):
        self.balance = starting_balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")
        self.balance -= amount

    def collect_interest(self) -> None:
        self.balance *= 1.1
