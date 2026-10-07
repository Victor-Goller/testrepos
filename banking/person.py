"""A Person owns one or more bank accounts."""

from .accounts import BankAccount


class Person:
    def __init__(self, name):
        self.name = name
        self.bank_accounts = []

    def open_bank_account(self, name="Checking", initial_deposit=0.0):
        account = BankAccount(self, name, initial_deposit)
        self.bank_accounts.append(account)
        return account

    def net_worth(self):
        return sum(acc.total_value() for acc in self.bank_accounts)

    def summary(self):
        lines = [f"{self.name} — net worth {self.net_worth():.2f}"]
        for bank in self.bank_accounts:
            lines.append(f"Bank account '{bank.name}' (#{bank.account_number}): "
                         f"balance {bank.balance:.2f}")
            for inv in bank.investment_accounts:
                lines.append("    " + inv.summary().replace("\n", "\n    "))
        return "\n".join(lines)

    def __repr__(self):
        return f"Person({self.name!r}, bank_accounts={len(self.bank_accounts)})"
