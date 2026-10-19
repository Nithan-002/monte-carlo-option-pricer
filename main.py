
import numpy as np
import matplotlib.pyplot as plt
from math import erf, exp, log, sqrt

# Option pricing parameters
S0 = 100.0
K = 100.0
T = 1.0
r = 0.05
sigma = 0.20
N = 10_000


def simulate_stock_prices(S0, T, r, sigma, N):
    """Simulate stock prices at expiry using risk-neutral GBM."""
    Z = np.random.standard_normal(N)
    return S0 * np.exp(
        (r - 0.5 * sigma**2) * T
        + sigma * np.sqrt(T) * Z
    )


def price_options(ST, K, r, T):
    """Calculate discounted Monte Carlo call and put prices."""
    call_payoffs = np.maximum(ST - K, 0)
    put_payoffs = np.maximum(K - ST, 0)
    discount = np.exp(-r * T)

    return (
        discount * np.mean(call_payoffs),
        discount * np.mean(put_payoffs),
    )


def normal_cdf(x):
    """Standard normal cumulative distribution function."""
    return 0.5 * (1 + erf(x / sqrt(2)))


def black_scholes_prices(S0, K, T, r, sigma):
    """Calculate European call and put prices."""
    d1 = (
        log(S0 / K) + (r + 0.5 * sigma**2) * T
    ) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    call = S0 * normal_cdf(d1) - K * exp(-r * T) * normal_cdf(d2)
    put = K * exp(-r * T) * normal_cdf(-d2) - S0 * normal_cdf(-d1)

    return call, put


def convergence_experiment(sample_sizes, S0, K, T, r, sigma, bs_call):
    """Measure call-price estimation error at different sample sizes."""
    estimates = []
    errors = []

    print("\n--- Monte Carlo Convergence ---")

    for n in sample_sizes:
        np.random.seed(42)
        Z = np.random.standard_normal(n)

        ST = S0 * np.exp(
            (r - 0.5 * sigma**2) * T
            + sigma * np.sqrt(T) * Z
        )

        estimate = np.exp(-r * T) * np.mean(np.maximum(ST - K, 0))
        error = abs(estimate - bs_call)

        estimates.append(estimate)
        errors.append(error)

        print(
            f"Simulations: {n:>6} | "
            f"Estimate: ₹{estimate:.4f} | "
            f"Absolute error: ₹{error:.4f}"
        )

    return estimates, errors


def plot_option_payoffs(K):
    """Plot European call and put payoffs at expiration."""
    stock_prices = np.linspace(0, 200, 500)

    call_payoffs = np.maximum(stock_prices - K, 0)
    put_payoffs = np.maximum(K - stock_prices, 0)

    plt.figure(figsize=(9, 5))
    plt.plot(stock_prices, call_payoffs, label="European Call Payoff")
    plt.plot(stock_prices, put_payoffs, label="European Put Payoff")
    plt.axvline(K, linestyle="--", label=f"Strike Price = ₹{K:.2f}")
    plt.xlabel("Stock Price at Expiration (₹)")
    plt.ylabel("Option Payoff (₹)")
    plt.title("European Call and Put Payoffs at Expiration")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("option_payoffs.png", dpi=300)
    plt.close()

    print("Saved payoff graph to option_payoffs.png")


def main():
    np.random.seed(42)

    ST = simulate_stock_prices(S0, T, r, sigma, N)
    call_price, put_price = price_options(ST, K, r, T)
    bs_call, bs_put = black_scholes_prices(S0, K, T, r, sigma)

    print("First 10 simulated stock prices:")
    print(ST[:10])

    print(f"\nEstimated call option price: ₹{call_price:.2f}")
    print(f"Estimated put option price: ₹{put_price:.2f}")

    print("\n--- Black-Scholes Comparison ---")
    print(f"Monte Carlo call: ₹{call_price:.2f}")
    print(f"Black-Scholes call: ₹{bs_call:.2f}")
    print(f"Monte Carlo put: ₹{put_price:.2f}")
    print(f"Black-Scholes put: ₹{bs_put:.2f}")
    print(f"Call pricing error: ₹{abs(call_price - bs_call):.4f}")
    print(f"Put pricing error: ₹{abs(put_price - bs_put):.4f}")

    sample_sizes = [100, 1_000, 10_000, 100_000]
    estimates, errors = convergence_experiment(
        sample_sizes, S0, K, T, r, sigma, bs_call
    )

    # Graph 1: estimated price versus simulation count
    plt.figure(figsize=(9, 5))
    plt.plot(sample_sizes, estimates, marker="o", label="Monte Carlo estimate")
    plt.axhline(
        y=bs_call,
        linestyle="--",
        label=f"Black-Scholes price = ₹{bs_call:.2f}",
    )
    plt.xscale("log")
    plt.xlabel("Number of simulations")
    plt.ylabel("Estimated call option price (₹)")
    plt.title("Monte Carlo Option Pricing Convergence")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("convergence.png", dpi=300)
    print("\nSaved convergence graph to convergence.png")
    plt.close()

    # Graph 2: absolute pricing error
    plt.figure(figsize=(9, 5))
    plt.plot(sample_sizes, errors, marker="o")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of simulations")
    plt.ylabel("Absolute pricing error (₹)")
    plt.title("Monte Carlo Pricing Error")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("convergence_error.png", dpi=300)
    plt.close()
    print("Saved error graph to convergence_error.png")

    # Graph 3: European call and put payoffs
    plot_option_payoffs(K)


if __name__ == "__main__":
    main()
