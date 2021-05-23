import pandas as pd
from pandas_datareader import data as web
from collections import defaultdict
from src.constants import Stock
import datetime

__all__ = [
    "get_data",
    "process_data",
    "remove_multi_index",
    "unstacking_stock_name",
    "pretty_print_percentage",
    "get_return",
    "get_stock_data_returns",
    "get_investment_data",
    'get_user_inputs',
]
def get_stock_input(params:dict) -> list:
    stock_info = params.get("STOCKS_INFO")

    print(f'Dear User, here is the list of stocks {params.get("APP_NAME")} chose by default for you!')

    for stock in stock_info.values():
        print(stock)

    chosen_stocks = list(stock_info.keys())
    reset_chosen_stock_lst = True
    done=False
    while not done:
        answer = input('Would you like to proceed with this set of stocks?[Y/N]')

        if answer in ['Y', 'y'] and chosen_stocks:
            done = True
        else:
            if reset_chosen_stock_lst:
                chosen_stocks = []
                reset_chosen_stock_lst = False
            mapping = {stock_obj.market_rank:stock for stock, stock_obj in stock_info.items()}
            answer = input(f'Please enter the market_rank of the stock')
            if answer in set(mapping.keys()):
                chosen_stock = mapping[answer]
                chosen_stocks.append(chosen_stock)
            else:
                print(f'The answer {answer} does not correspond to any market_rank from {params.get("APP_NAME")} database!')
            print(f'Currently you have selected: {", ".join(list(set(chosen_stocks)))}')
    else:
        print(f'You have selected: {", ".join(list(set(chosen_stocks)))}')

    return list(set(chosen_stocks))

def get_numerical_input(variable:str, type_:str='int') -> int:
    done = False
    while not done:
        try:
            answer = input(f'Enter the {variable}:')
            answer = int(answer) if type_ == 'int' else float(answer)
            done=True
        except ValueError:
            print(f'{answer} is not an {type_} value, try again!')
            done=False
    else:
        print(f'The {variable} you selected is:\n {answer}')
    return answer

def get_date_input(var_:str,params:dict)-> datetime.datetime:
    done=False
    while not done:
        answer = input('Would you like to change it?[Y/N]')
        if answer in ['Y','y']:
           year = get_numerical_input('Year')
           month = get_numerical_input('Month')
           day = get_numerical_input('Day')
           answer = datetime.datetime(year, month, day)
        else:
            answer = params.get(var_)
        final_answer= input(f'Do you confirm this date:{answer}?[Y/N]')
        if final_answer in ['Y', 'y']:
            done=True
    else:
        print(f'The {var_} you selected is:\n {answer}')
    return answer


def get_user_inputs(params:dict) -> dict:
    answer = input('Default mode?[Y/N]')
    if answer in ['Y','y']:
        params["chosen_stocks"] = list(params.get("STOCKS_INFO").keys())

        return params

    chosen_stocks = get_stock_input(params)
    num_simulations = get_numerical_input('number of simulations for the different portfolio allocation')
    num_simulations_stock = get_numerical_input('number of simulations for the different stocks scenarios')
    investment_amount = get_numerical_input('investment amount', type_='float')
    lower_quantile_lvl = get_numerical_input('worst scenario quantile level', type_='float')
    upper_quantile_lvl = get_numerical_input('best scenario quantile level', type_='float')
    start_date = get_date_input('START_DATE', params)
    end_date = get_date_input('END_DATE', params)



    params['chosen_stocks'] = chosen_stocks
    params['num_simulations'] = num_simulations
    params['num_simulations_stock'] = num_simulations_stock
    params['investment_amount'] = investment_amount
    params['lower_quantile_lvl'] = lower_quantile_lvl
    params['upper_quantile_lvl'] = upper_quantile_lvl

    params["START_DATE"] = start_date
    params["END_DATE"] =end_date

    return params


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
