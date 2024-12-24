import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.interpolate import griddata
from datetime import datetime


def black_scholes_iv(option_price, S, K, T, r, option_type="call"):
    precision = 1e-5
    max_iterations = 100
    sigma = 0.2

    for _ in range(max_iterations):
        try:
            d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)

            if option_type == "call":
                price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            else:
                price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

            vega = S * norm.pdf(d1) * np.sqrt(T)
            diff = option_price - price

            if abs(diff) < precision:
                return sigma

            sigma += diff / vega if vega > precision else 0.01
        except (FloatingPointError, ValueError, OverflowError):
            break

    return None


def fetch_options(ticker, max_days=30):
    stock = yf.Ticker(ticker)
    expirations = stock.options
    options_data = {}
    today = datetime.today()

    for exp in expirations:
        exp_date = datetime.strptime(exp, "%Y-%m-%d")
        days_to_exp = (exp_date - today).days
        if days_to_exp > 0 and days_to_exp <= max_days:
            opt_chain = stock.option_chain(exp)
            options_data[exp] = {
                "calls": opt_chain.calls,
                "puts": opt_chain.puts
            }

    return options_data


def build_volatility_surface(ticker, r=0.05):
    options_data = fetch_options(ticker)
    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d")["Close"].iloc[-1]

    strikes = []
    maturities_days = []
    implied_vols = []

    for exp, data in options_data.items():
        days_to_exp = (datetime.strptime(exp, "%Y-%m-%d") - datetime.today()).days
        T = days_to_exp / 365.0
        for _, row in data["calls"].iterrows():
            K = row["strike"]
            market_price = row["lastPrice"]

            if market_price <= 0 or T <= 0:
                continue

            iv = black_scholes_iv(market_price, current_price, K, T, r, option_type="call")
            if iv is not None:
                strikes.append(K)
                maturities_days.append(days_to_exp)
                implied_vols.append(iv)

    strikes = np.array(strikes)
    maturities_days = np.array(maturities_days)
    implied_vols = np.array(implied_vols)

    grid_strikes = np.linspace(min(strikes), max(strikes), 50)
    grid_maturities = np.linspace(min(maturities_days), max(maturities_days), 50)
    grid_x, grid_y = np.meshgrid(grid_strikes, grid_maturities)

    grid_z = griddata(
        points=(strikes, maturities_days),
        values=implied_vols,
        xi=(grid_x, grid_y),
        method="cubic"
    )

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap="viridis", edgecolor="k", alpha=0.8)

    ax.set_title(f"Interpolated Short-Term Volatility Surface for {ticker.upper()}", fontsize=14)
    ax.set_xlabel("Strike Price", fontsize=12)
    ax.set_ylabel("Time to Maturity (Days)", fontsize=12)
    ax.set_zlabel("Implied Volatility", fontsize=12)
    fig.colorbar(surf, shrink=0.5, aspect=10, label="Implied Volatility")
    plt.show()


if __name__ == "__main__":
    build_volatility_surface("AAPL")