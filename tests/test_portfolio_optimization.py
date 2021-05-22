import pytest
import numpy as np
import pandas as pd
import datetime
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
    num_simulations = 1_000

    params["chosen_stocks"] = chosen_stocks
    params["stocks_info"] = params.get("STOCKS_INFO")
    params["START_DATE"] = get_start_date()
    params["END_DATE"] = get_end_date()
    params["STOCKS_LIST"] = get_list_stocks()

    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)
    covariance_tbl = get_covariance_tbl(data_step1)
    correlation_tbl = get_correlation_tbl(data_step1)
    portfolio_properties = get_portfolio_properties(data_step1, params)
    yearly_returns = get_returns(data_step1)
    volatility_yearly = get_volatility_yearly(data_step1)

    portfolio_info = pd.merge(
        portfolio_properties.share_allocation_df,
        yearly_returns,
        how="left",
        on="stock_name",
    )
    portfolio_info = pd.merge(
        portfolio_info, volatility_yearly, how="left", on="stock_name"
    )

    data_step2 = get_stock_data_returns(data_step1, params)

    data = data_step2

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
def portfolio_properties(data: pd.DataFrame) -> PortfolioReturnsProperties:
    w = None
    if not w:
        chosen_stocks = params.get("chosen_stocks")
        w = {stock_name: 1 / len(chosen_stocks) for stock_name in chosen_stocks}
    variance_portfolio_return = get_portfolio_variance(data, w)
    share_allocation_df = get_shares_allocation_df(w)
    expected_portfolio_return = get_expected_portfolio_return(data, w)
    portfolio_properties = PortfolioReturnsProperties(
        variance_portfolio_return, share_allocation_df, expected_portfolio_return
    )
    return portfolio_properties


@pytest.fixture
def yearly_returns(data: pd.DataFrame) -> pd.DataFrame:
    variable = "Adj Close"
    df = unstacking_stock_name(data, variable)
    returns_yearly = df.resample("Y").last().pct_change().mean()
    df = pd.DataFrame({"returns_yearly": returns_yearly})
    df.index = [multi_idx[1] for multi_idx in df.index]
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={"index": "stock_name"}, inplace=True)
    return df


@pytest.fixture
def volatility_yearly(data: pd.DataFrame) -> pd.DataFrame:
    variable = "Adj Close"
    df = unstacking_stock_name(data, variable)
    volatility_yearly = (
        df.pct_change()
        .apply(lambda x: np.log(1 + x))
        .std()
        .apply(lambda x: x * np.sqrt(250))
    )
    df = pd.DataFrame({"volatility_yearly": volatility_yearly})
    df.index = [multi_idx[1] for multi_idx in df.index]
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={"index": "stock_name"}, inplace=True)
    return df


@pytest.fixture
def simulated_portfolios(data: pd.DataFrame) -> pd.DataFrame:
    num_simulations = 1_000
    chosen_stocks = list(params.get("STOCKS_INFO").keys())
    params["chosen_stocks"] = chosen_stocks
    chosen_stocks = params.get("chosen_stocks")
    num_assets = len(chosen_stocks)
    returns_yearly = get_returns(data).returns_yearly
    covariance_tbl = get_covariance_tbl(data).drop(columns=["stock_name"])
    returns = []
    volatilities = []
    weights = []
    for num_simulation in range(num_simulations):
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

    data_dic = {"returns": returns, "volatility": volatilities}

    for counter, stock_name in enumerate(chosen_stocks):
        # print(counter, symbol)
        data_dic[stock_name + " weight"] = [w[counter] for w in weights]

    simulated_portfolios = pd.DataFrame(data_dic)
    simulated_portfolios = add_sharpe_ratio(simulated_portfolios)
    return simulated_portfolios

@pytest.fixture
def simulated_stock(data) -> np.array:
    stock_name = 'Nestlé'
    stock_data = data.query(f'stock_name=="{stock_name}"')
    last_observed_value = stock_data['Adj Close'][stock_data.last_valid_index()]
    last_observed_date = stock_data.index[-1]
    first_simulated_day = last_observed_date + datetime.timedelta(days=1)
    data_range = pd.date_range(start=first_simulated_day, end=first_simulated_day + datetime.timedelta(days=365),
                               freq='B')  # business days
    nb_simulations = 100
    mean_returns = stock_data.returns.mean()
    std_returns = stock_data.returns.std()
    brownian_motion = np.random.normal(mean_returns, std_returns, (len(data_range), nb_simulations))
    simulated_returns = brownian_motion +1
    simulated_returns_cum = simulated_returns.cumprod(axis=1)
    simulated_value_stocks = last_observed_value * simulated_returns_cum
    return simulated_value_stocks

@pytest.fixture
def simulated_stocks(data:pd.DataFrame) -> dict:
    nb_simulations = 100
    chosen_stocks = list(params.get("STOCKS_INFO").keys())
    params["chosen_stocks"] = chosen_stocks
    simulated_stocks = get_simulated_stocks(data, nb_simulations, params)
    return simulated_stocks

@pytest.fixture
def weighted_sim_stocks(simulated_stocks: dict, simulated_portfolios: pd.DataFrame) -> dict:
    chosen_stocks = list(params.get("STOCKS_INFO").keys())
    params["chosen_stocks"] = chosen_stocks
    optimal_portfolio = get_portfolio_with(simulated_portfolios, lowest_volatility=True, highest_return=True).to_dict()
    weighted_sim_stocks = {}
    for stock_name, simulated_stock in simulated_stocks.items():
        for optimal_stock_weight_name, optimal_weight in optimal_portfolio.items():
            if stock_name in optimal_stock_weight_name:
                weighted_sim_stocks[stock_name] = simulated_stock * optimal_weight
    return weighted_sim_stocks

@pytest.fixture
def df_simulated_stock(data:pd.DataFrame, simulated_stocks:dict) -> pd.DataFrame:
        stock_name = 'Nestlé'
        stock_data = data.query(f'stock_name=="{stock_name}"')
        data_range = get_data_range(stock_data)
        simulated_stock = simulated_stocks.get(stock_name)
        df = pd.DataFrame(simulated_stock, index=data_range, columns=[f'sim_{i}_{stock_name}' for i in range(
            simulated_stock.shape[1])])
        s = df.stack()
        df = pd.DataFrame(s)
        df.reset_index(drop=False,inplace=True)
        df.columns = ['Date', 'simulation_name', 'Adj Close Price simulated']
        return df

@pytest.fixture
def scenarios_portfolio( weighted_sim_stocks:dict) -> np.array:
    scenarios_portfolio = np.sum(list(weighted_sim_stocks.values()), axis=0)
    return scenarios_portfolio

@pytest.fixture
def best_and_worst_scenarios(scenarios_portfolio:np.array) -> Scenarios:
    last_sim_portfolio_prices = scenarios_portfolio[-1, :]
    first_value = scenarios_portfolio[0, :].mean()
    lower_quantile_lvl = 0.05
    upper_quantile_lvl = 0.95
    worst_scenario = np.quantile(last_sim_portfolio_prices, q=lower_quantile_lvl)
    best_scenario = np.quantile(last_sim_portfolio_prices, q=upper_quantile_lvl)
    worst_yearly_return = (worst_scenario - first_value) / first_value
    best_yearly_return = (best_scenario - first_value) / first_value
    worst_yearly_return_str = '{:.2%}'.format(worst_yearly_return)
    best_yearly_return_str = '{:.2%}'.format(best_yearly_return)
    best_and_worst_scenario = Scenarios(worst_yearly_return, best_yearly_return, worst_yearly_return_str,
                                best_yearly_return_str)
    return best_and_worst_scenario

class TestPortfolioOptimization:

    def test_get_best_and_worst_scenarios(self, scenarios_portfolio:np.array) -> None:
        scenarios = get_best_and_worst_scenarios(scenarios_portfolio)
        assert isinstance(scenarios, Scenarios), f'{type(best_and_worst_scenarios)}'
        assert scenarios.worst < scenarios.best


    def test_get_scenarios_portfolio(self, weighted_sim_stocks:dict) -> None:
        stock_name = 'Nestlé'
        stock_shape = weighted_sim_stocks.get(stock_name).shape

        scenarios_portfolio = get_scenarios_portfolio(weighted_sim_stocks)

        assert type(scenarios_portfolio).__name__ == 'ndarray'
        assert scenarios_portfolio.shape == stock_shape

    def test_get_df_simulated_stocks(self, data:pd.DataFrame, simulated_stocks:dict) -> pd.DataFrame:
        stock_name = 'Nestlé'
        params['data_range'] = get_data_range(data, params)
        df_simulated_stock = get_df_simulated_stock(stock_name, simulated_stocks, params)
        for col in ['Date', 'simulation_name', 'Adj Close Price simulated']:
            assert col in df_simulated_stock.columns


    def test_weight_stocks(self, simulated_stocks:dict, simulated_portfolios:pd.DataFrame) -> None:
        chosen_stocks = list(params.get("STOCKS_INFO").keys())
        params["chosen_stocks"] = chosen_stocks
        optimal_portfolio = get_portfolio_with(simulated_portfolios, lowest_volatility=True, highest_return=True)
        weighted_sim_stocks = weight_simulated_stocks(simulated_stocks, optimal_portfolio)
        assert isinstance(weighted_sim_stocks, dict)
        assert len(weighted_sim_stocks) == len(params.get('chosen_stocks'))

    def test_get_simulated_stocks(self, data:pd.DataFrame)  -> None:
        nb_simulations = 100
        chosen_stocks = list(params.get("STOCKS_INFO").keys())
        params["chosen_stocks"] = chosen_stocks
        params['data_range'] = get_data_range(data, params)
        simulated_stocks = get_simulated_stocks(data, nb_simulations, params)
        assert isinstance(simulated_stocks, dict)
        assert len(simulated_stocks) == len(params.get('chosen_stocks'))

    def test_get_simulated_stock(self, data:pd.DataFrame)  -> None:
        stock_name = 'Nestlé'
        nb_simulations = 100
        params['data_range'] = get_data_range(data, params)
        simulated_stock = get_simulated_stock(stock_name, data, nb_simulations, params)
        assert type(simulated_stock).__name__ == 'ndarray'
        assert simulated_stock.shape[1] == nb_simulations

    def test_get_sharp_ratio(self, simulated_portfolios:pd.DataFrame) ->None:
        assert 'sharpe_ratio' in simulated_portfolios.columns

    def test_get_portfolio_with(self, simulated_portfolios:pd.DataFrame) ->None:
        portfolio = get_portfolio_with(simulated_portfolios, lowest_volatility=True)
        assert portfolio.dtype.name == 'float64'
        portfolio = get_portfolio_with(simulated_portfolios, lowest_volatility=True, pretty_print_perc=True)
        assert portfolio.dtype.name == 'object'
        with pytest.raises(NotImplementedError) as e:
            get_portfolio_with(simulated_portfolios, lowest_volatility=False)
        portfolio = get_portfolio_with(simulated_portfolios, lowest_volatility=False, highest_return=True)
        assert portfolio.dtype.name == 'float64'
        portfolio = get_portfolio_with(simulated_portfolios, lowest_volatility=True, highest_return=True)
        assert portfolio.dtype.name == 'float64'

    def test_run_simulation(self, data):
        num_simulations = 1_000
        chosen_stocks = list(params.get("STOCKS_INFO").keys())
        params["chosen_stocks"] = chosen_stocks
        chosen_stocks = params.get("chosen_stocks")
        portfolios = run_portfolios_simulations(data, num_simulations, params)
        assert portfolios.shape == (num_simulations, len(chosen_stocks) + 3)

    def test_get_volatility(self, data: pd.DataFrame) -> None:
        chosen_stocks = list(params.get("STOCKS_INFO").keys())
        volatility_yearly = get_volatility_yearly(data)
        assert "volatility_yearly" in volatility_yearly.columns
        assert volatility_yearly.shape == (len(chosen_stocks), 2)

    def test_get_returns(self, data):
        chosen_stocks = list(params.get("STOCKS_INFO").keys())
        yearly_returns = get_returns(data)
        assert "returns_yearly" in yearly_returns.columns
        assert yearly_returns.shape == (len(chosen_stocks), 2)

    def test_get_portfolio_properties(self, data: pd.DataFrame) -> None:
        chosen_stocks = list(params.get("STOCKS_INFO").keys())
        w = {stock_name: 1 / len(chosen_stocks) for stock_name in chosen_stocks}
        portfolio_variance, portfolio_share = (
            get_portfolio_variance(data, w),
            get_shares_allocation_df(w),
        )
        expected_portfolio_return = get_expected_portfolio_return(data, w)
        portfolio_properties = get_portfolio_properties(data, params)
        assert isinstance(portfolio_variance, float)
        assert isinstance(portfolio_share, pd.DataFrame)
        assert portfolio_share.shape == (len(chosen_stocks), 2)
        assert isinstance(expected_portfolio_return, float)
        assert isinstance(portfolio_properties, PortfolioReturnsProperties)

    def test_get_covariance_and_correlation_matrix(self, data: pd.DataFrame) -> None:
        covariance_tbl = get_covariance_tbl(data)
        nb_unique_stocks = len(data.stock_name.unique())
        assert covariance_tbl.shape == (nb_unique_stocks, nb_unique_stocks + 1)
        assert "stock_name" in covariance_tbl.columns
        covariance_tbl = get_covariance_tbl(data, insert_stock_name=False)
        nb_unique_stocks = len(data.stock_name.unique())
        assert covariance_tbl.shape == (nb_unique_stocks, nb_unique_stocks)
        assert "stock_name" not in covariance_tbl.columns
