import numpy as np
import pandas as pd

from src.utils import *


__all__ = [
    "get_covariance_tbl",
    "get_correlation_tbl",
    "get_portfolio_variance",
    "get_returns",
]


def get_returns(data: pd.DataFrame, variable: str = "Adj Close") -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    returns_yearly = df.resample("Y").last().pct_change().mean()
    df = pd.DataFrame({'yearly_returns': returns_yearly})
    df.index = [multi_idx[1] for multi_idx in df.index]
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={'index':'stock_name'}, inplace=True)
    return df


def get_portfolio_variance(data: pd.DataFrame, params: dict, w: dict = None) -> tuple:
    """
    :param covariance_tbl:
    :param params:
    :param w: weight dictionary with key as stock name and value as portfolio share for the given stock
    :return:
    """
    if not w:
        chosen_stocks = params.get("chosen_stocks")
        w = {stock_name: 1 / len(chosen_stocks) for stock_name in chosen_stocks}
    covariance_tbl = get_covariance_tbl(data, insert_stock_name=False)
    portfolio_share= pd.DataFrame.from_dict(w, orient='index', columns=['portfolio_share'])
    portfolio_share.reset_index(drop=False, inplace=True)
    portfolio_share.rename(columns={'index':'stock_name'}, inplace=True)
    return covariance_tbl.mul(w, axis=0).mul(w, axis=1).sum().sum(), portfolio_share


def get_correlation_tbl(
    data: pd.DataFrame, variable: str = "Adj Close", insert_stock_name: bool = True
) -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    df = df.pct_change().apply(lambda x: np.log(1 + x)).corr()
    df = remove_multi_index(df)
    if insert_stock_name:
        df.insert(0, "stock_name", list(df.index))
    return df


def get_covariance_tbl(
    data: pd.DataFrame, variable: str = "Adj Close", insert_stock_name: bool = True
) -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    df = df.pct_change().apply(lambda x: np.log(1 + x)).cov()
    df = remove_multi_index(df)
    if insert_stock_name:
        df.insert(0, "stock_name", list(df.index))
    return df
