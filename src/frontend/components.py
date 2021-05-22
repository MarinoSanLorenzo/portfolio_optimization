import pandas as pd
from types import FunctionType
import dash_html_components as html
import dash_core_components as dcc
from src.constants import params
from src.utils import *
import dash_table
from src.frontend.plots import *
from src.portfolio_optimization import *

__all__ = [
    "stock_list_dropdown",
    "add_layout_components_for_multiple_plots",
    "get_data_table",
    'add_layout_compoment_for_simulated_stock_plots'
]


def get_data_table(
    df: pd.DataFrame, pretty_print_perc: bool = False
) -> dash_table.DataTable:
    if pretty_print_perc:
        df = pretty_print_percentage(df)
    return dash_table.DataTable(

        columns=[{"name": i, "id": i} for i in df.columns], data=df.to_dict("records")
    )


def add_layout_compoment_for_simulated_stock_plots(data:pd.DataFrame, simulated_stocks:dict) -> list:
    components = []
    for stock_name, simulated_stock in simulated_stocks.items():
        df_simulated_stock = get_df_simulated_stock(stock_name, data, simulated_stocks)
        fig = plot_simulated_stocks(df_simulated_stock, "Adj Close Price simulated", f"Simulated {stock_name} Prices")
        components.append(dcc.Graph(figure=fig)), components.append(html.Hr())
    return components


def add_layout_components_for_multiple_plots(
    plot_func: FunctionType, data: pd.DataFrame, params: dict
) -> list:
    """
    Creates a list with [graph, html.Hr(), graph, html.Hr(), ...]
    to be further unpacked in the layout
    """
    plots_lst = []
    for stock in params.get("chosen_stocks"):
        graph, hr = dcc.Graph(figure=plot_func(data, stock)), html.Hr()
        plots_lst.append(graph), plots_lst.append(hr)
    return plots_lst


stock_list_dropdown = dcc.Dropdown(
    id="chosen-stocks",
    options=[{"label": stock, "value": stock} for stock in params.get("STOCKS_INFO")],
    multi=True,
    searchable=True,
    value=list(params.get("STOCKS_INFO").keys()),
)
