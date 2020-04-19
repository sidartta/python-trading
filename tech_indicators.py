# ------------------------------------------------------ #
# Module & Libraries Import
# ------------------------------------------------------ #
import numpy as np
import pandas as pd


# ------------------------------------------------------ #
# MACD calculation for a unique stock
# ------------------------------------------------------ #
def macd(df=pd.DataFrame(), short_p=12, long_p=20, mean_p=9):
    macd_df = pd.DataFrame(index=df.index)
    macd_df['MA Fast'] = df.ewm(span=short_p, min_periods=short_p).mean()
    macd_df['MA Slow'] = df.ewm(span=long_p, min_periods=long_p).mean()
    macd_df['MACD'] = macd_df['MA Fast'] - macd_df['MA Slow']
    macd_df['Signal'] = macd_df['MACD'].ewm(span=mean_p, min_periods=mean_p).mean()
    return macd_df
