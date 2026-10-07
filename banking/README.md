# banking

A small object-oriented model of a person's bank and investment accounts.

```
Person
 └── BankAccount            (a person can have many)
      └── InvestmentAccount (a bank account can have many)
           └── Portfolio
                └── Holding (one per asset, tracks quantity & average cost)
                     └── Asset (abstract) -> Stock | Bond | IndexFund
```

## Usage

```python
from banking import Person, Stock, Bond, IndexFund

apple = Stock("AAPL", "Apple Inc.", 190.0, sector="Tech", dividend_yield=0.005)
bond = Bond("NOR10Y", "Norway 10Y", 980.0, face_value=1000, coupon_rate=0.035)
sp500 = IndexFund("VOO", "S&P 500 ETF", 480.0, tracked_index="S&P 500")

victor = Person("Victor")
checking = victor.open_bank_account("Checking", initial_deposit=50_000)
growth = checking.open_investment_account("Growth", initial_funding=20_000)

growth.buy(apple, 30)
growth.buy(sp500, 10)
growth.sell("AAPL", 5)

print(victor.summary())
print(growth.portfolio.allocation())
```

Run the full demo with `python banking_demo.py` and the tests with
`python -m unittest discover tests`.

## Adding a new asset type

Subclass `Asset` and implement `asset_type` and `expected_annual_income`:

```python
class Crypto(Asset):
    @property
    def asset_type(self):
        return "Crypto"

    def expected_annual_income(self, quantity):
        return 0.0
```
