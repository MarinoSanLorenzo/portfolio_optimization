import numpy as np
import pandas as pd
from copy import deepcopy
from pandas.plotting import scatter_matrix
import plotly.express as px
import plotly.graph_objects as go
import plotly
from dash.dependencies import Input, Output
import dash
import plotly.figure_factory as ff
from src.constants import params
from dash_main import *


__all__ = ['plot', 'plot_low_high_prices', 'plot_scatter_matrix']

def plot_scatter_matrix(
    data: dict, params: dict, variable:str
) -> plotly.graph_objects.Figure:
    title = f'Scatter Matrix for {variable} Prices'
    components = pd.concat(
        [data.query(f'stock_name=="{stock_name}"')[variable] for stock_name in params.get("STOCKS_INFO")], axis=1
    )
    components.columns = [
        f"{stock.capitalize()} {variable}" for stock in params.get("STOCKS_INFO")
    ]
    return px.scatter_matrix(components, title=title)



def add_trace_high_low(
    fig: plotly.graph_objects.Figure, df: pd.DataFrame
) -> plotly.graph_objects.Figure:

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.High,
            name="High",
            line=dict(color="firebrick", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.Low,
            name="Low",
            line=dict(color="royalblue", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df.Open, name="Open", line=dict(color="firebrick", width=1)
        )
    )
    return fig

def plot_low_high_prices(df: pd.DataFrame, stock_name: str) -> plotly.graph_objects.Figure:
    df = df.query(f'stock_name=="{stock_name}"')
    fig = go.Figure()
    # Create and style traces
    fig = add_trace_high_low(fig, df)
    # Edit the layout
    fig.update_layout(
        title=f"Average High, Low and Open Prices for the {stock_name} stock",
        xaxis_title="Date",
        yaxis_title="Prices",
    )
    return fig



def plot(
    data: pd.DataFrame,
    y,
    title=None,
    x="Date",
    label="stock_name",
    line_shape="spline",
    render_mode="svg",
) -> plotly.graph_objects.Figure:
    return px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=label,
        line_group=label,
        hover_name=label,
        line_shape=line_shape,
        render_mode=render_mode,
    )
