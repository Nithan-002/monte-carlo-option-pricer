import unittest

from main import (
    simulate_stock_prices,
    price_options,
    black_scholes_prices,
    S0, K, T, r, sigma, N
)


class TestOptionPricer(unittest.TestCase):

    def test_option_prices_are_positive(self):
        ST = simulate_stock_prices(S0, r, sigma, T, N)
        call, put = price_options(ST, K, r, T)

        self.assertGreater(call, 0)
        self.assertGreater(put, 0)

    def test_monte_carlo_matches_black_scholes(self):
        import numpy as np
        np.random.seed(42)
        ST = simulate_stock_prices(S0, T, r, sigma, 100000)
        mc_call, mc_put = price_options(ST, K, r, T)
        bs_call, bs_put = black_scholes_prices(S0, K, T, r, sigma)

        self.assertAlmostEqual(mc_call, bs_call, delta=0.20)
        self.assertAlmostEqual(mc_put, bs_put, delta=0.20)


if __name__ == "__main__":
    unittest.main()