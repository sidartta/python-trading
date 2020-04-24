# ---------------------------------------------------------------------------- #
# Module & Libraries Import
# ---------------------------------------------------------------------------- #
import mplfinance as mpf
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------- #
# Drawing function with candlesticks on daily plot
# ---------------------------------------------------------------------------- #
def stock_plot(ticker, name, tik_data, macd_data, window):
    # MACD plot + time-series Data
    apds = [
        mpf.make_addplot(
            macd_data['MACD'][-window:], panel='lower', color='black'),
        mpf.make_addplot(
            macd_data['Signal'][-window:], panel='lower', color='red')
    ]

    mpf.plot(
        tik_data[-window:], addplot=apds, type='candlestick', mav=(20, 50),
        figscale=3, title=f'\n{ticker}: {name}', volume=True, legend=True
    )

    # Plots display
    plt.show()
