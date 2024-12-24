# Volatility Surface Plotter

## Overview

This project creates a volatility surface for a stock’s options using the Black-Scholes model and real-time market data from the Yahoo Finance API. The tool focuses on short-term options (up to 30 days to expiration) and provides an interpolated 3D visualization of implied volatility.

## Features
- Options Data Fetching:
  - Retrieves options chains for a given stock ticker.
  - Filters data for short-term options (expirations within 30 days).
- Implied Volatility Calculation:
  - Implements the Black-Scholes model to compute implied volatility for each option.
  - Supports both calls and puts (currently visualizes calls).
- 3D Volatility Surface Visualization:
  - Interpolates between points for a smooth surface.
  - Plots strike price, time to maturity (in days), and implied volatility.
 
## Example

## How It Works
- 1.	Data Collection:
	- Fetches historical market data and options chains from Yahoo Finance.
  - Filters options for expirations within the next 30 days.
- 2.	Implied Volatility Calculation:
	- Uses the Black-Scholes formula to compute implied volatility for each option.
  - Filters out invalid data points (e.g., missing or zero prices).
- 3.	Surface Construction:
	- Interpolates implied volatility values across a grid of strike prices and time-to-maturity values.
  - Plots a smooth 3D surface.
- 4.	Visualization:
	- Displays the interpolated volatility surface with:
	- X-axis: Strike Prices.
	- Y-axis: Time to Maturity (Days).
	- Z-axis: Implied Volatility.
