import numpy as np
import pandas as pd
from collections import namedtuple

from src.utils import *


__all__ = [
    "get_covariance_tbl",
    "get_correlation_tbl",
    "get_portfolio_properties",
    "get_returns",
    'get_portfolio_variance',
    'get_shares_allocation_df',
    'get_expected_portfolio_return',
    'PortfolioReturnsProperties',
    'get_volatility_yearly'
]

PortfolioReturnsProperties = namedtuple('PortfolioReturnsProperties', 'variance_portfolio_return share_allocation_df '
                                                                'expected_portfolio_return')


def get_volatility_yearly(data:pd.DataFrame, variable:str='Adj Close') -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    volatility_yearly= df.pct_change().apply(lambda x: np.log(1 + x)).std().apply(lambda x: x * np.sqrt(250))
    df = pd.DataFrame({"volatility_yearly": volatility_yearly})
    df.index = [multi_idx[1] for multi_idx in df.index]
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={"index": "stock_name"}, inplace=True)
    return df

def get_returns(data: pd.DataFrame, variable: str = "Adj Close") -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    returns_yearly = df.resample("Y").last().pct_change().mean()
    df = pd.DataFrame({"returns_yearly": returns_yearly})
    df.index = [multi_idx[1] for multi_idx in df.index]
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={"index": "stock_name"}, inplace=True)
    return df


def get_expected_portfolio_return(data:pd.DataFrame, w:dict) -> float:
    yearly_returns = get_returns(data)
    return (list(w.values())*yearly_returns.returns_yearly).sum()

def get_portfolio_variance(data:pd.DataFrame, w: dict) -> float:
    covariance_tbl = get_covariance_tbl(data, insert_stock_name=False)
    return covariance_tbl.mul(w, axis=0).mul(w, axis=1).sum().sum()

def get_shares_allocation_df(w:dict) -> pd.DataFrame:
    share_allocation_df = pd.DataFrame.from_dict(
        w, orient="index", columns=["portfolio_share"]
    )
    share_allocation_df.reset_index(drop=False, inplace=True)
    share_allocation_df.rename(columns={"index": "stock_name"}, inplace=True)
    return share_allocation_df


def get_portfolio_properties(data: pd.DataFrame, params: dict, w: dict = None) -> PortfolioReturnsProperties:
    """
    :param covariance_tbl:
    :param params:
    :param w: weight dictionary with key as stock name and value as portfolio share for the given stock
    :return:
    """
    if not w:
        chosen_stocks = params.get("chosen_stocks")
        w = {stock_name: 1 / len(chosen_stocks) for stock_name in chosen_stocks}
    variance_portfolio_return = get_portfolio_variance(data, w)
    share_allocation_df = get_shares_allocation_df(w)
    expected_portfolio_return = get_expected_portfolio_return(data, w)
    return PortfolioReturnsProperties(variance_portfolio_return, share_allocation_df, expected_portfolio_return)


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
