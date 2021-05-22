import pandas as pd
from pandas_datareader import data as web
from collections import defaultdict
from src.constants import Stock

__all__ = [
    "get_data",
    "process_data",
    "remove_multi_index",
    "unstacking_stock_name",
    "pretty_print_percentage",
    "get_return",
    "get_stock_data_returns",
    "get_investment_data",
]


def get_investment_data(params: dict, Stock: Stock = Stock) -> pd.DataFrame:
    d = defaultdict(list)
    for field in Stock._fields:
        for stock_name, stock_obj in params.get("STOCKS_INFO").items():
            d[field].append(getattr(stock_obj, field))
    return pd.DataFrame.from_dict(d)


def get_stock_data_returns(data: pd.DataFrame, params: dict) -> pd.DataFrame:
    return pd.concat([get_return(data, stock) for stock in params.get("STOCKS_INFO")])


def get_return(data: pd.DataFrame, stock_name: str) -> pd.DataFrame:
    data = data.query(f'stock_name=="{stock_name}"')
    data["returns"] = data["Close"].pct_change(1)
    data["cum_returns"] = (1 + data["returns"]).cumprod()
    return data


def pretty_print_percentage(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df, pd.DataFrame):
        for col in df.columns:
            try:
                setattr(df, col, getattr(df, col).apply(lambda x: "{:.2%}".format(x)))
            except Exception as e:
                print(e)
    elif isinstance(df, pd.Series):
        df = df.apply(lambda x: "{:.2%}".format(x))
    else:
        raise NotImplementedError
    return df


def remove_multi_index(df: pd.DataFrame) -> pd.DataFrame:
    df.index = [idx_multi[1] for idx_multi in df.index]
    df.columns = [idx_multi[1] for idx_multi in df.columns]
    return df


def unstacking_stock_name(data: pd.DataFrame, variable: str) -> pd.DataFrame:
    df = data[[variable, "stock_name", "Date"]]
    df.reset_index(drop=True, inplace=True)
    df.set_index(["Date", "stock_name"], inplace=True)
    return df.unstack(level=1)


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
    stocks_data = stocks_data.sort_values(["stock_name", "Date"])
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
