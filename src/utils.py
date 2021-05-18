import pandas as pd
from pandas_datareader import data as web

__all__ = ["get_data", "process_data"]


def process_data(data: pd.DataFrame, params: dict) -> pd.DataFrame:
    """
    Stack the data by symbols
    rename the symbol column
    add stock_name and sector variable
    """
    code_name_mapping = params.get("CODE_NAME_MAPPING")
    code_rank_mapping = params.get("CODE_RANK_MAPPING")
    stocks_data = data.stack()
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
    stocks_data = stocks_data.sort_values(['stock_name', 'Date'])
    return stocks_data


def get_data(params: dict, chosen_stocks: list = None) -> pd.DataFrame:
    start_date = params.get("START_DATE")
    end_date = params.get("END_DATE")
    stocks_info = params.get("STOCKS_INFO")
    chosen_stocks = None
    if not chosen_stocks:
        chosen_stocks = [stock_name for stock_name, stock in stocks_info.items()]
    chosen_codes = [stocks_info[stock_name].code for stock_name in chosen_stocks]
    return web.DataReader(chosen_codes, "yahoo", start=start_date, end=end_date)
