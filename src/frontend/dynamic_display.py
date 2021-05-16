import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()

app.layout = html.Div([
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

    html.Div(id='container'),
    html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'})
])


@app.callback(Output('container', 'children'), [Input('chosen-stocks', 'value')])
def display_graphs(value):
    graphs = []
    for i in value:
        graphs.append(dcc.Graph(
            id='graph-{}'.format(i),
            figure={
                'data': [{
                    'x': [1, 2, 3],
                    'y': [3, 1, 2]
                }],
                'layout': {
                    'title': 'Graph {}'.format(i)
                }
            }
        ))
    return html.Div(graphs)


if __name__ == '__main__':
    app.run_server(debug=True)