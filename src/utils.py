import pandas as pd
from pandas_datareader import data

__all__ = ['get_data']

def get_data(params: dict) -> pd.DataFrame:
    stock_codes = params
