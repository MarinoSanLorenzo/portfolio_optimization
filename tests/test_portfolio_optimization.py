import pytest
import numpy as np
import pandas as pd
from src.frontend.callbacks import *
from src.constants import params
from src.portfolio_optimization import *
from src.utils import *


@pytest.fixture
def stock() -> str:
    stock = "Nestlé"
    return stock


@pytest.fixture
def data() -> pd.DataFrame:
    chosen_stocks = list(params.get("STOCKS_INFO").keys())
    params["chosen_stocks"] = chosen_stocks
    params["stocks_info"] = params.get("STOCKS_INFO")
    params["START_DATE"] = get_start_date()
    params["END_DATE"] = get_end_date()
    params["STOCKS_LIST"] = get_list_stocks()

    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)

    data = data_step1
    return data


@pytest.fixture
def covariance_tbl(data: pd.DataFrame) -> pd.DataFrame:
    insert_stock_name = False
    # unstacking_stock_name
    adj_close = data[["Adj Close", "stock_name", "Date"]]
    adj_close.reset_index(drop=True, inplace=True)
    adj_close.set_index(["Date", "stock_name"], inplace=True)
    adj_close = adj_close.unstack(level=1)

    covariance_tbl = adj_close.pct_change().apply(lambda x: np.log(1 + x)).cov()
    covariance_tbl.index = [idx_multi[1] for idx_multi in covariance_tbl.index]
    covariance_tbl.columns = [idx_multi[1] for idx_multi in covariance_tbl.columns]
    if insert_stock_name:
        covariance_tbl.insert(0, "stock_name", list(covariance_tbl.index))
    return covariance_tbl


@pytest.fixture
def portfolio_variance(data: pd.DataFrame) -> float:
    covariance_tbl = get_covariance_tbl(data, insert_stock_name=False)
    chosen_stocks = params.get("chosen_stocks")
    w = {stock_name: 1 / len(chosen_stocks) for stock_name in chosen_stocks}
    portfolio_variance = covariance_tbl.mul(w, axis=0).mul(w, axis=1).sum().sum()
    return portfolio_variance


class TestPortfolioOptimization:
    def test_get_returns(self):
        variable = "Adj Close"
        df = unstacking_stock_name(data, variable)
        returns_yearly = df.resample("Y").last().pct_change().mean()

    def test_calc_portfolio_variance(self, data: pd.DataFrame) -> float:
        portfolio_variance = get_portfolio_variance(data, params)
        assert isinstance(portfolio_variance, float)

    def test_get_covariance_and_correlation_matrix(self, data: pd.DataFrame) -> None:
        covariance_tbl = get_covariance_tbl(data)
        nb_unique_stocks = len(data.stock_name.unique())
        assert covariance_tbl.shape == (nb_unique_stocks, nb_unique_stocks + 1)
        assert "stock_name" in covariance_tbl.columns
        covariance_tbl = get_covariance_tbl(data, insert_stock_name=False)
        nb_unique_stocks = len(data.stock_name.unique())
        assert covariance_tbl.shape == (nb_unique_stocks, nb_unique_stocks)
        assert "stock_name" not in covariance_tbl.columns
