# ---------------------------------------------------------------------------- #
# Module & Libraries Import
# ---------------------------------------------------------------------------- #
import mplfinance as mpf
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------- #
# Drawing function with candlesticks on daily plot
# ---------------------------------------------------------------------------- #
def stock_plot(ticker, name, tik_data, macd_data, sma_data, window):
    # MACD plot + time-series Data
    apds = [
        mpf.make_addplot(
            macd_data['MACD'][-window:], panel='lower', color='black'),
        mpf.make_addplot(
            macd_data['Signal'][-window:], panel='lower', color='red'),
        mpf.make_addplot(
            sma_data['sma_50'][-window:], color='blue'),
        mpf.make_addplot(
            sma_data['sma_150'][-window:], color='red')
    ]

    mpf.plot(
        tik_data[-window:], addplot=apds, type='candle', style='blueskies',
        figscale=3, title=f'\n{ticker}: {name}', volume=True
    )

    # Plots display
    plt.show()
