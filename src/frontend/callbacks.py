import datetime
from dash.dependencies import Input, Output
import plotly
import dash_core_components as dcc
import dash_html_components as html
from src.constants import *
from dash_main import app
from src.frontend.plots import *

__all__ = ["get_list_stocks", "get_start_date", "get_end_date"]

#
#
# @app.callback(Output('open_prices_plot_all', 'figure'), [Input('chosen-stocks', 'value')])
# def update_open_price_plot(stocks_list:list) -> plotly.graph_objects.Figure:
#     global  data
#     filtered_df = data.query(f'stock_name in {stocks_list}')
#     return plot(filtered_df, "Open", "Open prices")


#
# @app.callback(Output("container", "children"), [Input("chosen-stocks", "value")])
# def display_graphs(value):
#     graphs = []
#     for i in value:
#         graphs.append(
#             dcc.Graph(
#                 id="graph-{}".format(i),
#                 figure={
#                     "data": [{"x": [1, 2, 3], "y": [3, 1, 2]}],
#                     "layout": {"title": "Graph {}".format(i)},
#                 },
#             )
#         )
#     return html.Div(graphs)
#


def get_list_stocks() -> list:
    pass


def get_start_date(
    start_date: datetime.datetime = datetime.datetime(2019, 1, 1)
) -> datetime.datetime:
    return start_date


def get_end_date(
    end_date: datetime.datetime = datetime.date.today(),
) -> datetime.datetime:
    return end_date
