"""A Portfolio is a collection of Holdings, one per asset."""


from .exceptions import InsufficientHoldingsError


class Holding:
    """How many units of one asset are owned, and what they cost on average."""

    def __init__(self, asset):
        self.asset = asset
        self.quantity = 0.0
        self.average_cost = 0.0

    @property
    def cost_basis(self):
        return self.quantity * self.average_cost

    @property
    def market_value(self):
        return self.quantity * self.asset.price

    @property
    def unrealized_gain(self):
        return self.market_value - self.cost_basis

    def add(self, quantity, price):
        total_cost = self.cost_basis + quantity * price
        self.quantity += quantity
        self.average_cost = total_cost / self.quantity

    def remove(self, quantity):
        if quantity > self.quantity:
            raise InsufficientHoldingsError(
                f"Cannot sell {quantity} {self.asset.ticker}; only {self.quantity} owned"
            )
        self.quantity -= quantity

    def __repr__(self):
        return (f"Holding({self.asset.ticker}, qty={self.quantity}, "
                f"value={self.market_value:.2f})")


class Portfolio:
    """All the assets held in one investment account."""

    def __init__(self):
        self._holdings = {}  # ticker -> Holding

    @property
    def holdings(self):
        return list(self._holdings.values())

    def get(self, ticker):
        return self._holdings.get(ticker.upper())

    def add(self, asset, quantity, price=None):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        price = asset.price if price is None else price
        holding = self._holdings.setdefault(asset.ticker, Holding(asset))
        holding.add(quantity, price)

    def remove(self, ticker, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        holding = self.get(ticker)
        if holding is None:
            raise InsufficientHoldingsError(f"No holding for {ticker}")
        holding.remove(quantity)
        if holding.quantity == 0:
            del self._holdings[holding.asset.ticker]

    def total_value(self):
        return sum(h.market_value for h in self.holdings)

    def total_cost(self):
        return sum(h.cost_basis for h in self.holdings)

    def unrealized_gain(self):
        return self.total_value() - self.total_cost()

    def expected_annual_income(self):
        return sum(h.asset.expected_annual_income(h.quantity) for h in self.holdings)

    def holdings_by_type(self, asset_type):
        """Return holdings of one kind, e.g. 'Stock', 'Bond' or 'Index'."""
        return [h for h in self.holdings if h.asset.asset_type == asset_type]

    def allocation(self):
        """Share of total value per asset type, e.g. {'Stock': 0.6, 'Bond': 0.4}."""
        total = self.total_value()
        if total == 0:
            return {}
        result = {}
        for h in self.holdings:
            result[h.asset.asset_type] = result.get(h.asset.asset_type, 0) + h.market_value
        return {kind: value / total for kind, value in result.items()}

    def __len__(self):
        return len(self._holdings)

    def __repr__(self):
        return f"Portfolio({len(self)} holdings, value={self.total_value():.2f})"
