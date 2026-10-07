"""Custom exceptions for the banking package."""


class BankingError(Exception):
    """Base class for all errors raised by this package."""


class InsufficientFundsError(BankingError):
    """Raised when an account does not have enough cash for an operation."""


class InsufficientHoldingsError(BankingError):
    """Raised when trying to sell more units of an asset than are owned."""
