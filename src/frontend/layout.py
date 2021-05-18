import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from dash_main import app
from src.constants import params
from src.frontend.components import stock_list_dropdown


layout = html.Div(
    children=[
        html.H1(children="Smart Invest"),
        html.H2(children="The best trading tool for young swiss individuals!"),
        dcc.Tabs(
            [
                dcc.Tab(label="Stock market data", children=[stock_list_dropdown]),
                dcc.Tab(label="Enter your investment inputs"),
                dcc.Tab(label="Portfolio Optimization"),
            ]
        ),
    ]
)

#
# dcc.Dropdown(
#                             id="chosen-stocks",
#                             options=[
#                                 {"label": stock, "value": stock}
#                                 for stock in ["adam", "marino"]
#                             ],
#                             multi=True,
#                             searchable=True,
#                             value=["adam", "marino"],
#                         ),

# html.Div(id='container')
# html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'})
# ],style={"display":"inline-block"})


if __name__ == "__main__":
    app.run_server(debug=True)
