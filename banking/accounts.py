"""Bank accounts and the investment accounts that belong to them."""

import itertools

from .exceptions import InsufficientFundsError
from .portfolio import Portfolio

_account_numbers = itertools.count(1000)


class _CashAccount:
    """Shared behaviour for anything that holds a cash balance."""

    def __init__(self, name):
        self.name = name
        self.account_number = next(_account_numbers)
        self.cash = 0.0
        self.transactions = []  # list of (kind, amount, description)

    def _log(self, kind, amount, description=""):
        self.transactions.append((kind, amount, description))

    def _deposit(self, amount, description):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.cash += amount
        self._log("deposit", amount, description)

    def _withdraw(self, amount, description):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.cash:
            raise InsufficientFundsError(
                f"{self.name}: cannot withdraw {amount:.2f}, balance is {self.cash:.2f}"
            )
        self.cash -= amount
        self._log("withdraw", amount, description)


class BankAccount(_CashAccount):
    """A person's bank account. It can own several investment accounts."""

    def __init__(self, owner, name="Checking", initial_deposit=0.0):
        super().__init__(name)
        self.owner = owner
        self.investment_accounts = []
        if initial_deposit:
            self.deposit(initial_deposit)

    @property
    def balance(self):
        return self.cash

    def deposit(self, amount, description="Deposit"):
        self._deposit(amount, description)

    def withdraw(self, amount, description="Withdrawal"):
        self._withdraw(amount, description)

    def transfer_to(self, other, amount):
        """Move cash to another BankAccount."""
        self.withdraw(amount, f"Transfer to {other.account_number}")
        other.deposit(amount, f"Transfer from {self.account_number}")

    def open_investment_account(self, name, initial_funding=0.0):
        account = InvestmentAccount(self, name)
        self.investment_accounts.append(account)
        if initial_funding:
            account.fund(initial_funding)
        return account

    def total_investment_value(self):
        return sum(acc.total_value() for acc in self.investment_accounts)

    def total_value(self):
        """Cash in this account plus everything in its investment accounts."""
        return self.balance + self.total_investment_value()

    def __repr__(self):
        return (f"BankAccount(#{self.account_number} {self.name!r}, "
                f"balance={self.balance:.2f}, "
                f"investment_accounts={len(self.investment_accounts)})")


class InvestmentAccount(_CashAccount):
    """
    An investment account linked to a BankAccount.

    Cash is moved in from (and back out to) the linked bank account, and is
    then used to buy assets that are kept in the account's Portfolio.
    """

    def __init__(self, bank_account, name):
        super().__init__(name)
        self.bank_account = bank_account
        self.portfolio = Portfolio()

    def fund(self, amount):
        """Move cash from the linked bank account into this account."""
        self.bank_account.withdraw(amount, f"To investment account {self.name}")
        self._deposit(amount, "Funding from bank account")

    def withdraw_to_bank(self, amount):
        """Move uninvested cash back to the linked bank account."""
        self._withdraw(amount, "Withdrawal to bank account")
        self.bank_account.deposit(amount, f"From investment account {self.name}")

    def buy(self, asset, quantity):
        cost = asset.price * quantity
        self._withdraw(cost, f"Buy {quantity} {asset.ticker} @ {asset.price:.2f}")
        self.portfolio.add(asset, quantity, asset.price)

    def sell(self, ticker, quantity):
        holding = self.portfolio.get(ticker)
        price = holding.asset.price if holding else 0.0
        self.portfolio.remove(ticker, quantity)
        self._deposit(price * quantity, f"Sell {quantity} {ticker.upper()} @ {price:.2f}")

    def total_value(self):
        return self.cash + self.portfolio.total_value()

    def summary(self):
        lines = [f"Investment account '{self.name}' (#{self.account_number})",
                 f"  Cash:      {self.cash:12.2f}"]
        for h in self.portfolio.holdings:
            lines.append(
                f"  {h.asset.asset_type:<6} {h.asset.ticker:<6} "
                f"{h.quantity:>8g} x {h.asset.price:>9.2f} = {h.market_value:12.2f} "
                f"(gain {h.unrealized_gain:+.2f})"
            )
        lines.append(f"  Total:     {self.total_value():12.2f}")
        return "\n".join(lines)

    def __repr__(self):
        return (f"InvestmentAccount(#{self.account_number} {self.name!r}, "
                f"cash={self.cash:.2f}, {self.portfolio!r})")
