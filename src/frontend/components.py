import pandas as pd
from types import FunctionType
import dash_html_components as html
import dash_core_components as dcc
from src.constants import params
from src.frontend.plots import *

__all__ = ['stock_list_dropdown',  'add_layout_components_for_multiple_plots']


def add_layout_components_for_multiple_plots(plot_func:FunctionType, data:pd.DataFrame, params:dict) ->list:
    '''
    Creates a list with [graph, html.Hr(), graph, html.Hr(), ...]
    to be further unpacked in the layout
    '''
    plots_lst =[]
    for stock in params.get('chosen_stocks'):
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
