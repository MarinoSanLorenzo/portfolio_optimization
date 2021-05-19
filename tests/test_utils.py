import pytest
import pandas as pd
import datetime
from src.frontend.callbacks import *
from src.constants import params
from src.utils import *
from pandas_datareader import data


@pytest.fixture
def data_step0() -> pd.DataFrame:
    ### get_data
    start_date = params.get("START_DATE")
    end_date = params.get("END_DATE")
    stocks_info = params.get("STOCKS_INFO")
    chosen_stocks = None
    if not chosen_stocks:
        chosen_stocks = [stock_name for stock_name, stock in stocks_info.items()]
    chosen_codes = [stocks_info[stock_name].code for stock_name in chosen_stocks]
    data_step0 = data.DataReader(chosen_codes, "yahoo", start=start_date, end=end_date)
    return data_step0


### preprocess_data


def data_step1(data_step0: pd.DataFrame) -> pd.DataFrame:
    code_name_mapping = params.get("CODE_NAME_MAPPING")
    code_rank_mapping = params.get("CODE_RANK_MAPPING")
    stocks_data = data_step0.stack()
    dates = [idx[0] for idx in stocks_data.index]
    stocks_data = stocks_data.reset_index(drop=False)
    stocks_data.index = dates
    stocks_data.rename(columns={"Symbols": "stock_code"}, inplace=True)
    stocks_data["stock_name"] = stocks_data.stock_code.apply(
        lambda code: code_name_mapping.get(code)
    )
    stocks_data["sector"] = stocks_data.stock_code.apply(
        lambda x: code_rank_mapping.get(x)
    )

    data_step1 = stocks_data.sort_values(["stock_name", "Date"])
    return data_step1


class TestUtils:
    def test_preprocess_data(self, data_step0):
        data_step1 = process_data(data_step0, params)
        chosen_codes = [stock.code for stock in params.get("STOCKS_INFO").values()]
        for col in ["stock_name", "stock_code", "sector"]:
            assert col in data_step1.columns

    def test_get_data(self):
        data_step0 = get_data(params)
        chosen_codes = [stock.code for stock in params.get("STOCKS_INFO").values()]
        for multi_idx in data_step0.columns:
            assert multi_idx[1] in set(chosen_codes)
