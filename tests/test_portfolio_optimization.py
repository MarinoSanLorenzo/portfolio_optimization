import pytest
import numpy as np
import pandas as pd
from src.frontend.callbacks import *
from src.utils import *
from src.constants import params
from src.frontend.plots import *

@pytest.fixture
def stock() -> str:
    stock = 'Nestlé'
    return stock

@pytest.fixture
def data() -> pd.DataFrame:
    chosen_stocks = list(params.get("STOCKS_INFO").keys())
    params['chosen_stocks'] = chosen_stocks
    params["stocks_info"] = params.get("STOCKS_INFO")
    params["START_DATE"] = get_start_date()
    params["END_DATE"] = get_end_date()
    params["STOCKS_LIST"] = get_list_stocks()

    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)

    data = data_step1
    return data


class TestPortfolioOptimization:

    def test_get_covariance_and_correlation_matrix(self):
        adj_close = data[['Adj Close', 'stock_name', 'Date']]
        adj_close.reset_index(drop=True, inplace=True)
        adj_close.set_index(['Date','stock_name'], inplace=True)
        adj_close =adj_close.unstack(level=1)

        adj_close.pct_change().apply(lambda x: np.log(1+x)).cov()



