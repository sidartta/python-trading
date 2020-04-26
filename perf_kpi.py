# ---------------------------------------------------------------------------- #
# Module & Libraries Import
# ---------------------------------------------------------------------------- #
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------- #
# Function to calculate Cumulative Annual Growth Rate
# ---------------------------------------------------------------------------- #
def cagr(ser):
    calc_df = pd.DataFrame()
    calc_df["daily_ret"] = ser.pct_change()
    calc_df["cum_return"] = (1 + calc_df["daily_ret"]).cumprod()
    n = len(calc_df) / 252
    CAGR = (calc_df["cum_return"][-1]) ** (1 / n) - 1
    return CAGR


# ---------------------------------------------------------------------------- #
# Function to calculate annualized volatility
# ---------------------------------------------------------------------------- #
def volatility(ser):
    calc_df = ser.pct_change()
    vol = calc_df.std() * np.sqrt(252)
    return vol


# ---------------------------------------------------------------------------- #
# Function to calculate Sharpe Ratio; rf is the risk free rate
# ---------------------------------------------------------------------------- #
def sharpe(ser, rf):
    sr = (cagr(ser) - rf) / volatility(ser)
    return sr


# ---------------------------------------------------------------------------- #
# Function to calculate Sortino Ratio; rf is the risk free rate
# ---------------------------------------------------------------------------- #
def sortino(ser, rf):
    chg = ser.pct_change()
    neg_vol = chg.where(chg < 0).std() * np.sqrt(252)
    sr = (cagr(ser) - rf) / neg_vol
    return sr


'''def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd


def calmar(DF):
    "function to calculate calmar ratio"
    df = DF.copy()
    clmr = CAGR(df) / max_dd(df)
    return clmr'''
