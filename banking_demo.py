"""
Demo of the `banking` package.

Run with:  python banking_demo.py
"""

from banking import Person, Stock, Bond, IndexFund


def main():
    # Define some assets that can be traded
    apple = Stock("AAPL", "Apple Inc.", 190.0, sector="Tech", dividend_yield=0.005)
    equinor = Stock("EQNR", "Equinor ASA", 28.0, sector="Energy", dividend_yield=0.05)
    gov_bond = Bond("NOR10Y", "Norway 10Y Government Bond", 980.0,
                    face_value=1000, coupon_rate=0.035, maturity_years=10)
    sp500 = IndexFund("VOO", "Vanguard S&P 500 ETF", 480.0,
                      tracked_index="S&P 500", expense_ratio=0.0003, dividend_yield=0.013)

    # A person opens a bank account
    victor = Person("Victor")
    checking = victor.open_bank_account("Checking", initial_deposit=50_000)

    # The bank account gets two investment accounts
    growth = checking.open_investment_account("Growth", initial_funding=20_000)
    safe = checking.open_investment_account("Safe", initial_funding=10_000)

    growth.buy(apple, 30)
    growth.buy(equinor, 100)
    growth.buy(sp500, 20)

    safe.buy(gov_bond, 8)
    safe.buy(sp500, 4)

    # Prices move
    apple.update_price(210.0)
    sp500.update_price(500.0)
    gov_bond.update_price(990.0)

    print(victor.summary())
    print()
    print("Growth allocation:",
          {k: f"{v:.0%}" for k, v in growth.portfolio.allocation().items()})
    print(f"Safe expected yearly income: {safe.portfolio.expected_annual_income():.2f}")


if __name__ == "__main__":
    main()
