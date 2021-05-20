import pytest
import pandas as pd
from src.frontend.callbacks import *
from src.utils import *
from src.constants import params
from src.frontend.plots import *
import plotly.express as px
from src.portfolio_optimization import *


@pytest.fixture
def stock() -> str:
    stock = "Nestlé"
    return stock


@pytest.fixture
def data_step1() -> pd.DataFrame:
    chosen_stocks = list(params.get("STOCKS_INFO").keys())
    num_simulations = 1_000

    params["chosen_stocks"] = chosen_stocks
    params["stocks_info"] = params.get("STOCKS_INFO")
    params["START_DATE"] = get_start_date()
    params["END_DATE"] = get_end_date()
    params["STOCKS_LIST"] = get_list_stocks()

    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)
    return data_step1


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

    portfolios_simulated = run_portfolios_simulations(
        data_step1, num_simulations, params
    )

    data = data_step2
    return data


@pytest.fixture
def portfolios_simulated(data_step1: pd.DataFrame) -> pd.DataFrame:
    num_simulations = 1_000
    portfolios_simulated = run_portfolios_simulations(
        data_step1, num_simulations, params
    )
    return portfolios_simulated


@pytest.fixture
def scatter_plot(data: pd.DataFrame) -> None:
    variable = "Open"
    title = f"Scatter Matrix for {variable} Prices"
    components = pd.concat(
        [
            data.query(f'stock_name=="{stock_name}"')[variable]
            for stock_name in params.get("STOCKS_INFO")
        ],
        axis=1,
    )
    components.columns = [
        f"{stock.capitalize()} {variable}" for stock in params.get("STOCKS_INFO")
    ]
    fig = px.scatter_matrix(components, title=title)


class TestPlot:
    def test_efficient_frontier_plot(self, portfolios_simulated: pd.DataFrame) -> None:
        fig = px.scatter(
            portfolios_simulated,
            x="volatility",
            y="returns",
            title="Efficient Frontier",
        )
        fig.show()

    def test_dist_returns_plots(self, data: pd.DataFrame) -> None:
        fig = plot_dist_returns(data, params)
        fig.show()

    def test_scatter_plot(self, data: pd.DataFrame, stock: str) -> None:
        fig = plot_scatter_matrix(data, params, "Open")
        fig.show()

    def test_plot_open_prices(self, data: pd.DataFrame, stock: str) -> None:
        fig = plot_low_high_prices(data, stock)
        fig.show()

    def test_plot_open_prices_all(self, data: pd.DataFrame) -> None:
        fig = plot(data, "Open", "Open prices")
        fig.show()
