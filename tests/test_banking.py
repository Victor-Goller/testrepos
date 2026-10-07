import unittest

from banking import (Bond, IndexFund, InsufficientFundsError,
                     InsufficientHoldingsError, Person, Stock)


class BankingTest(unittest.TestCase):
    def setUp(self):
        self.person = Person("Ada")
        self.bank = self.person.open_bank_account("Main", initial_deposit=10_000)
        self.stock = Stock("abc", "ABC Corp", 100.0, dividend_yield=0.02)
        self.bond = Bond("GOV", "Gov Bond", 950.0, face_value=1000, coupon_rate=0.04)
        self.index = IndexFund("IDX", "World Index", 50.0, "MSCI World",
                               expense_ratio=0.001, dividend_yield=0.02)

    def test_bank_deposit_withdraw_transfer(self):
        self.bank.withdraw(1_000)
        other = self.person.open_bank_account("Savings")
        self.bank.transfer_to(other, 2_000)
        self.assertEqual(self.bank.balance, 7_000)
        self.assertEqual(other.balance, 2_000)
        with self.assertRaises(InsufficientFundsError):
            self.bank.withdraw(100_000)

    def test_open_investment_account_moves_cash(self):
        inv = self.bank.open_investment_account("Stocks", initial_funding=3_000)
        self.assertEqual(self.bank.balance, 7_000)
        self.assertEqual(inv.cash, 3_000)
        self.assertIn(inv, self.bank.investment_accounts)

    def test_buy_and_sell(self):
        inv = self.bank.open_investment_account("Mix", initial_funding=5_000)
        inv.buy(self.stock, 10)
        inv.buy(self.bond, 2)
        inv.buy(self.index, 20)
        self.assertAlmostEqual(inv.cash, 5_000 - 1_000 - 1_900 - 1_000)
        self.assertEqual(len(inv.portfolio), 3)

        self.stock.update_price(120.0)
        self.assertAlmostEqual(inv.portfolio.get("ABC").unrealized_gain, 200)

        inv.sell("ABC", 10)
        self.assertIsNone(inv.portfolio.get("ABC"))
        self.assertAlmostEqual(inv.cash, 1_100 + 1_200)
        with self.assertRaises(InsufficientHoldingsError):
            inv.sell("GOV", 5)
        with self.assertRaises(InsufficientFundsError):
            inv.buy(self.bond, 100)

    def test_average_cost(self):
        inv = self.bank.open_investment_account("Avg", initial_funding=5_000)
        inv.buy(self.stock, 10)
        self.stock.update_price(200.0)
        inv.buy(self.stock, 10)
        self.assertAlmostEqual(inv.portfolio.get("ABC").average_cost, 150.0)

    def test_allocation_and_income(self):
        inv = self.bank.open_investment_account("Alloc", initial_funding=5_000)
        inv.buy(self.stock, 10)   # 1000
        inv.buy(self.index, 20)   # 1000
        alloc = inv.portfolio.allocation()
        self.assertAlmostEqual(alloc["Stock"], 0.5)
        self.assertAlmostEqual(alloc["Index"], 0.5)
        inv.buy(self.bond, 1)
        # 1000*0.02 + 1000*(0.02-0.001) + 1000*0.04
        self.assertAlmostEqual(inv.portfolio.expected_annual_income(), 79.0)

    def test_net_worth(self):
        inv = self.bank.open_investment_account("NW", initial_funding=2_000)
        inv.buy(self.stock, 10)
        self.stock.update_price(150.0)
        self.assertAlmostEqual(self.person.net_worth(), 10_000 + 500)
        inv.withdraw_to_bank(1_000)
        self.assertAlmostEqual(self.bank.balance, 9_000)
        self.assertAlmostEqual(self.person.net_worth(), 10_500)


if __name__ == "__main__":
    unittest.main()
