import numpy as np
import pandas as pd

__all__ = ['get_covariance_tbl', 'get_correlation_tbl']


def get_correlation_tbl(data:pd.DataFrame, variable:str='Adj Close') -> pd.DataFrame:
    df = data[[variable, 'stock_name', 'Date']]
    df.reset_index(drop=True, inplace=True)
    df.set_index(['Date', 'stock_name'], inplace=True)
    df = df.unstack(level=1)
    df = df.pct_change().apply(lambda x: np.log(1 + x)).corr()
    # remove multi index
    df.index = [idx_multi[1] for idx_multi in df.index]
    df.columns = [idx_multi[1] for idx_multi in df.columns]
    df.insert(0, 'stock_name', list(df.index))
    return df


def get_covariance_tbl(data:pd.DataFrame, variable:str='Adj Close') -> pd.DataFrame:
    df = data[[variable, 'stock_name', 'Date']]
    df.reset_index(drop=True, inplace=True)
    df.set_index(['Date', 'stock_name'], inplace=True)
    df = df.unstack(level=1)
    df = df.pct_change().apply(lambda x: np.log(1 + x)).cov()
    # remove multi index
    df.index = [idx_multi[1] for idx_multi in df.index]
    df.columns = [idx_multi[1] for idx_multi in df.columns]
    df.insert(0, 'stock_name', list(df.index))
    return df

