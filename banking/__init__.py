"""
A small object-oriented model of personal banking and investing.

Hierarchy:

    Person
     └── BankAccount (one or more)
          └── InvestmentAccount (one or more per bank account)
               └── Portfolio
                    └── Holding (one per asset)
                         └── Asset  ->  Stock | Bond | IndexFund
"""

from .exceptions import BankingError, InsufficientFundsError, InsufficientHoldingsError
from .assets import Asset, Stock, Bond, IndexFund
from .portfolio import Holding, Portfolio
from .accounts import BankAccount, InvestmentAccount
from .person import Person

__all__ = [
    "BankingError",
    "InsufficientFundsError",
    "InsufficientHoldingsError",
    "Asset",
    "Stock",
    "Bond",
    "IndexFund",
    "Holding",
    "Portfolio",
    "BankAccount",
    "InvestmentAccount",
    "Person",
]
