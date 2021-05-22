import numpy as np
import pandas as pd
from collections import namedtuple
from tqdm import tqdm
import dash_html_components as html
import datetime

from src.utils import *


__all__ = [
    'get_covariance_tbl',
    'get_correlation_tbl',
    'get_portfolio_properties',
    'get_returns',
    'get_portfolio_variance',
    'get_shares_allocation_df',
    'get_expected_portfolio_return',
    'PortfolioReturnsProperties',
    'get_volatility_yearly',
    'run_portfolios_simulations',
    'get_portfolio_with',
    'get_investment_summary',
    'add_sharpe_ratio',
    'get_simulated_stock',
    'get_simulated_stocks',
    'weight_simulated_stocks',
    'Scenarios',
    'get_data_range',
    'get_df_simulated_stock',
    'get_scenarios_portfolio',
    'Scenarios',
    'get_best_and_worst_scenarios',
    'get_data_range'
]

Simulations = namedtuple('Simulations', 'simulated_stocks weighted_sim_stocks scenario')

PortfolioReturnsProperties = namedtuple(
    'PortfolioReturnsProperties',
    'variance_portfolio_return share_allocation_df ' 'expected_portfolio_return',
)

Scenarios = namedtuple('Scenarios', 'worst best worst_str '
                                                            'best_str')

def get_best_and_worst_scenarios(scenarios_portfolio:np.array, lower_quantile_lvl:float = 0.05,
                                 upper_quantile_lvl:float = 0.95) -> Scenarios:
    last_sim_portfolio_prices = scenarios_portfolio[-1, :]
    first_value = scenarios_portfolio[0, :].mean()
    worst_scenario = np.quantile(last_sim_portfolio_prices, q=lower_quantile_lvl)
    best_scenario = np.quantile(last_sim_portfolio_prices, q=upper_quantile_lvl)
    worst_yearly_return = (worst_scenario - first_value) / first_value
    best_yearly_return = (best_scenario - first_value) / first_value
    worst_yearly_return_str = '{:.2%}'.format(worst_yearly_return)
    best_yearly_return_str = '{:.2%}'.format(best_yearly_return)
    return Scenarios(worst_yearly_return, best_yearly_return, worst_yearly_return_str, best_yearly_return_str)

def get_scenarios_portfolio_df() -> pd.DataFrame:
    pass


def get_scenarios_portfolio( weighted_sim_stocks:dict) -> np.array:
    return np.sum(list(weighted_sim_stocks.values()), axis=0)


def get_df_simulated_stock(stock_name:str, simulated_stocks: dict, params:dict) -> pd.DataFrame:
    data_range = params.get('data_range')
    simulated_stock = simulated_stocks.get(stock_name)
    df = pd.DataFrame(simulated_stock, index=data_range, columns=[f'sim_{i}_{stock_name}' for i in range(
        simulated_stock.shape[1])])
    s = df.stack()
    df = pd.DataFrame(s)
    df.reset_index(drop=False, inplace=True)
    df.columns = ['Date', 'simulation_name', 'Adj Close Price simulated']
    return df

def get_scenarios(data:pd.DataFrame, nb_simulations:int, optimal_portfolio:dict,params:dict) -> Simulations:
    simulated_stocks = get_simulated_stocks(data, nb_simulations, params)

    weighted_sim_stocks = weight_simulated_stocks(simulated_stocks, optimal_portfolio)
    siimulations_optimal_portfolio = get_scenarios_portfolio(weighted_sim_stocks)
    scenarios_optimal_portfolio = get_best_and_worst_scenarios(siimulations_optimal_portfolio)
    return Simulations(simulated_stocks, weighted_sim_stocks, siimulations_optimal_portfolio, scenarios_optimal_portfolio)


def weight_simulated_stocks(simulated_stocks: dict, optimal_portfolio:dict) -> dict:
    weighted_sim_stocks = {}
    for stock_name, simulated_stock in simulated_stocks.items():
        for optimal_stock_weight_name, optimal_weight in optimal_portfolio.items():
            if stock_name in optimal_stock_weight_name:
                weighted_sim_stocks[stock_name] = simulated_stock * optimal_weight
    return weighted_sim_stocks


def get_simulated_stocks( data:pd.DataFrame, nb_simulations:int, params:dict) ->dict:
    return {stock_name:get_simulated_stock(stock_name, data, nb_simulations) for stock_name in params.get(
        'chosen_stocks')}

def get_data_range(data:pd.DataFrame, params:dict) -> pd.DatetimeIndex:
    stock_name = list(params.get('chosen_stocks').keys())[0]
    stock_data = data.query(f'stock_name=="{stock_name}"')
    last_observed_date = stock_data.index[-1]
    first_simulated_day = last_observed_date + datetime.timedelta(days=1)
    return pd.date_range(start=first_simulated_day, end=first_simulated_day + datetime.timedelta(days=365),
                               freq='B')  # business days


def get_simulated_stock(stock_name:str, data:pd.DataFrame, nb_simulations:int, params:dict) -> np.array:
    stock_data = data.query(f'stock_name=="{stock_name}"')
    last_observed_value = stock_data['Adj Close'][stock_data.last_valid_index()]
    data_range = get_data_range(stock_data, params)
    mean_returns = stock_data.returns.mean()
    std_returns = stock_data.returns.std()
    brownian_motion = np.random.normal(mean_returns, std_returns, (len(data_range), nb_simulations))
    simulated_returns = brownian_motion +1
    simulated_returns_cum = simulated_returns.cumprod(axis=1)
    simulated_value_stocks = last_observed_value * simulated_returns_cum
    return simulated_value_stocks


def add_sharpe_ratio(portfolios_simulated:pd.DataFrame) -> pd.DataFrame:
    rf = 0.01  # risk factor
    portfolios_simulated['sharpe_ratio'] = (portfolios_simulated['returns'] - rf) / portfolios_simulated['volatility']
    return portfolios_simulated



def get_portfolio_with(portfolios_simulated:pd.DataFrame,
                       lowest_volatility:bool=True,
                       highest_return:bool=False,
                       pretty_print_perc=False) -> pd.DataFrame:
    if lowest_volatility and not(highest_return):
        portfolio = portfolios_simulated.iloc[portfolios_simulated['volatility'].idxmin()]
    elif highest_return and not(lowest_volatility):
        portfolio = portfolios_simulated.iloc[portfolios_simulated['returns'].idxmax()]
    elif highest_return and lowest_volatility:
        portfolio = portfolios_simulated.iloc[portfolios_simulated['sharpe_ratio'].idxmax()]
    else:
        raise NotImplementedError
    if pretty_print_perc:
        return pretty_print_percentage(portfolio)
    return portfolio

def get_investment_summary(portfolios_simulated:pd.DataFrame) -> list:
    portfolio_with_lowest_volatility = get_portfolio_with(portfolios_simulated, lowest_volatility=True,
                                                          highest_return=False,
                                                          pretty_print_perc=True)
    portfolio_with_highest_return = get_portfolio_with(portfolios_simulated,
                                                       lowest_volatility=False,
                                                       highest_return=True,
                                                       pretty_print_perc=True)
    optimal_portfolio = get_portfolio_with(portfolios_simulated, lowest_volatility=True,
                                                       highest_return=True,
                                                       pretty_print_perc=True)

    summary_msg1 = 'Smart Invest found few portfolios out of your simulations.'
    summary_msg2 = 'The portfolio with lowest volatility is presented as follow:\n'
    summary_msg3 = html.Ul(children=[html.Li(f'{k}:\t{v}') for k,v in portfolio_with_lowest_volatility.items()])
    summary_msg4 = 'The portfolio with highest returns is presented as follow:\n'
    summary_msg5 = html.Ul(children=[html.Li(f'{k}:\t{v}') for k, v in portfolio_with_highest_return.items()])
    summary_msg6 = 'The optimal portfolio is presented as follow:\n'
    summary_msg7 = html.Ul(children=[html.Li(f'{k}:\t{v}') for k, v in optimal_portfolio.items()])


    return [html.Div(summary_msg1), html.Hr(), summary_msg2, summary_msg3, html.Hr(), summary_msg4,
          summary_msg5, html.Hr(), summary_msg6, summary_msg7]

def run_portfolios_simulations(
    data: pd.DataFrame, num_simulations: int, params: dict
) -> pd.DataFrame:
    chosen_stocks = params.get('chosen_stocks')
    num_assets = len(chosen_stocks)
    returns_yearly = get_returns(data).returns_yearly
    covariance_tbl = get_covariance_tbl(data).drop(columns=['stock_name'])
    returns = []
    volatilities = []
    weights = []
    for _ in tqdm(range(num_simulations)):
        weight = np.random.random(num_assets)
        weight = weight / np.sum(weight)
        return_ = np.dot(weight, returns_yearly)
        var = (
            covariance_tbl.mul(weight, axis=0).mul(weight, axis=1).sum().sum()
        )  # Portfolio variance
        sd = np.sqrt(var)  # Daily standard deviation
        volatility_yearly = sd * np.sqrt(250)  # Annual standard deviation = volatility
        volatilities.append(volatility_yearly)
        returns.append(return_)
        weights.append(weight)

    data_dic = {'returns': returns, 'volatility': volatilities}

    for counter, stock_name in enumerate(chosen_stocks):
        # print(counter, symbol)
        data_dic[stock_name + ' weight'] = [w[counter] for w in weights]
    simulated_portfolios = pd.DataFrame(data_dic)
    simulated_portfolios  = add_sharpe_ratio(simulated_portfolios)
    return simulated_portfolios


def get_volatility_yearly(
    data: pd.DataFrame, variable: str = 'Adj Close'
) -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    volatility_yearly = (
        df.pct_change()
        .apply(lambda x: np.log(1 + x))
        .std()
        .apply(lambda x: x * np.sqrt(250))
    )
    df = pd.DataFrame({'volatility_yearly': volatility_yearly})
    df.index = [multi_idx[1] for multi_idx in df.index]
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={'index': 'stock_name'}, inplace=True)
    return df


def get_returns(data: pd.DataFrame, variable: str = 'Adj Close') -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    returns_yearly = df.resample('Y').last().pct_change().mean()
    df = pd.DataFrame({'returns_yearly': returns_yearly})
    df.index = [multi_idx[1] for multi_idx in df.index]
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={'index': 'stock_name'}, inplace=True)
    return df


def get_expected_portfolio_return(data: pd.DataFrame, w: dict) -> float:
    yearly_returns = get_returns(data)
    return (list(w.values()) * yearly_returns.returns_yearly).sum()


def get_portfolio_variance(data: pd.DataFrame, w: dict) -> float:
    covariance_tbl = get_covariance_tbl(data, insert_stock_name=False)
    return covariance_tbl.mul(w, axis=0).mul(w, axis=1).sum().sum()


def get_shares_allocation_df(w: dict) -> pd.DataFrame:
    share_allocation_df = pd.DataFrame.from_dict(
        w, orient='index', columns=['portfolio_share']
    )
    share_allocation_df.reset_index(drop=False, inplace=True)
    share_allocation_df.rename(columns={'index': 'stock_name'}, inplace=True)
    return share_allocation_df


def get_portfolio_properties(
    data: pd.DataFrame, params: dict, w: dict = None
) -> PortfolioReturnsProperties:
    """
    :param covariance_tbl:
    :param params:
    :param w: weight dictionary with key as stock name and value as portfolio share for the given stock
    :return:
    """
    if not w:
        chosen_stocks = params.get('chosen_stocks')
        w = {stock_name: 1 / len(chosen_stocks) for stock_name in chosen_stocks}
    variance_portfolio_return = get_portfolio_variance(data, w)
    share_allocation_df = get_shares_allocation_df(w)
    expected_portfolio_return = get_expected_portfolio_return(data, w)
    return PortfolioReturnsProperties(
        variance_portfolio_return, share_allocation_df, expected_portfolio_return
    )


def get_correlation_tbl(
    data: pd.DataFrame, variable: str = 'Adj Close', insert_stock_name: bool = True
) -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    df = df.pct_change().apply(lambda x: np.log(1 + x)).corr()
    df = remove_multi_index(df)
    if insert_stock_name:
        df.insert(0, 'stock_name', list(df.index))
    return df


def get_covariance_tbl(
    data: pd.DataFrame, variable: str = 'Adj Close', insert_stock_name: bool = True
) -> pd.DataFrame:
    df = unstacking_stock_name(data, variable)
    df = df.pct_change().apply(lambda x: np.log(1 + x)).cov()
    df = remove_multi_index(df)
    if insert_stock_name:
        df.insert(0, 'stock_name', list(df.index))
    return df
