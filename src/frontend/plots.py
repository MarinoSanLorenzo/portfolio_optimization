import numpy as np
import pandas as pd
from  copy import deepcopy
from pandas.plotting import scatter_matrix
import plotly.express as px
import plotly.graph_objects as go
import plotly
from dash.dependencies import Input, Output
import dash
import plotly.figure_factory as ff
from src.constants import params
from dash_main import *


__all__ = [
    "plot"
        ]

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
