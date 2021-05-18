import dash_html_components as html
import dash_core_components as dcc
from src.constants import params

__all__ = ["stock_list_dropdown"]


stock_list_dropdown = dcc.Dropdown(
    id="chosen-stocks",
    options=[{"label": stock, "value": stock} for stock in params.get("STOCKS_INFO")],
    multi=True,
    searchable=True,
    value=list(params.get("STOCKS_INFO").keys()),
)
