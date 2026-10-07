"""
Tradable assets.

`Asset` is an abstract base class. Each concrete subclass (Stock, Bond,
IndexFund) adds its own attributes and behaviour, but they all share a
name, a ticker symbol and a current price, so a Portfolio can treat them
the same way (polymorphism).
"""

from abc import ABC, abstractmethod


class Asset(ABC):
    """Something that can be bought and held in a portfolio."""

    def __init__(self, ticker, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.ticker = ticker.upper()
        self.name = name
        self.price = float(price)

    @property
    @abstractmethod
    def asset_type(self):
        """A short label such as 'Stock', 'Bond' or 'Index'."""

    @abstractmethod
    def expected_annual_income(self, quantity):
        """Expected yearly cash income (dividends, coupons) for `quantity` units."""

    def update_price(self, new_price):
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = float(new_price)

    def __repr__(self):
        return f"{self.asset_type}({self.ticker!r}, price={self.price:.2f})"


class Stock(Asset):
    """A share in a single company."""

    def __init__(self, ticker, name, price, sector="Unknown", dividend_yield=0.0):
        super().__init__(ticker, name, price)
        self.sector = sector
        self.dividend_yield = dividend_yield  # e.g. 0.03 for 3 %

    @property
    def asset_type(self):
        return "Stock"

    def expected_annual_income(self, quantity):
        return self.price * self.dividend_yield * quantity


class Bond(Asset):
    """A fixed-income security that pays a yearly coupon on its face value."""

    def __init__(self, ticker, name, price, face_value=1000.0, coupon_rate=0.0,
                 maturity_years=10):
        super().__init__(ticker, name, price)
        self.face_value = float(face_value)
        self.coupon_rate = coupon_rate  # e.g. 0.04 for 4 %
        self.maturity_years = maturity_years

    @property
    def asset_type(self):
        return "Bond"

    def annual_coupon(self):
        return self.face_value * self.coupon_rate

    def expected_annual_income(self, quantity):
        return self.annual_coupon() * quantity


class IndexFund(Asset):
    """A fund that tracks a market index, e.g. the S&P 500."""

    def __init__(self, ticker, name, price, tracked_index, expense_ratio=0.0,
                 dividend_yield=0.0):
        super().__init__(ticker, name, price)
        self.tracked_index = tracked_index
        self.expense_ratio = expense_ratio  # yearly fee, e.g. 0.0003 for 0.03 %
        self.dividend_yield = dividend_yield

    @property
    def asset_type(self):
        return "Index"

    def annual_fee(self, quantity):
        return self.price * self.expense_ratio * quantity

    def expected_annual_income(self, quantity):
        return self.price * (self.dividend_yield - self.expense_ratio) * quantity
