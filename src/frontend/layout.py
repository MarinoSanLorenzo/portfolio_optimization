import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from dash_main import app



layout = html.Div([
    # html.Button(id='button', n_clicks=0, children='Add graph'),

    dcc.Dropdown(
                                id="chosen-stocks",
                                options=[
                                    {"label": stock, "value": stock}
                                    for stock in ["adam", "marino"]
                                ],
                                multi=True,
                                searchable=True,
                                value=["adam", "marino"],
                            ),

    html.Div(id='container')
    # html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'})
],style={"display":"inline-block"})





if __name__ == '__main__':
    app.run_server(debug=True)
