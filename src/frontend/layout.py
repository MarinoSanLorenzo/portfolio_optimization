import dash_html_components as html
import dash_core_components as dcc

from dash_main import app
from src.frontend.components import stock_list_dropdown

__all__ = ["get_layout"]


def get_layout(params: dict) -> html.Div:
    return html.Div(
        children=[
            html.H1(children=params.get('APP_NAME')),
            html.H2(children="The best trading tool for young swiss individuals!"),
            dcc.Tabs(
                [
                    dcc.Tab(label="Summary", children=[*params.get("summary_msg")]),
                    dcc.Tab(
                        label="Investment data",
                        children=[
                            html.Div(
                                f'You invested in {", ".join(params.get("chosen_stocks"))}'
                            ),
                            params.get("your_investment_data"),
                            html.Hr(),
                            params.get('investment_data_component')
                        ],
                    ),
                    dcc.Tab(
                        label="Stock market data",
                        children=[
                            stock_list_dropdown,
                            dcc.Graph(figure=params.get("open_prices_plot_all")),
                            html.Hr(),
                            *params.get("open_prices_plot_lst"),
                            html.Div("Covariance matrix"),
                            params.get("covariance_tbl_dt"),
                            html.Hr(),
                            html.Div("Correlation matrix"),
                            params.get("correlation_tbl_dt"),
                            dcc.Graph(figure=params.get("open_scatter_matrix")),
                            html.Hr(),
                            html.Div("Portfolio Share and expected returns"),
                            params.get("portfolio_info_dt"),
                            html.Div(
                                f"The portfolio variance is:\t"
                                f'{params.get("default_portfolio_variance")} for the above allocation.\n'
                                f'The portfolio expected return is {params.get("default_portfolio_expected_return")}'
                            ),
                            html.Hr(),
                            html.Div("Distribution of returns"),
                            dcc.Graph(figure=params.get("dist_returns_plot"))
                            # html.Div(id='container'),
                        ],
                    ),
                    dcc.Tab(
                        label="Portfolio Optimization",
                        children=[
                            dcc.Graph(
                                figure=params.get(
                                    "efficient_frontier_optimal_point_plot"
                                )
                            ),
                            html.Hr(),
                            dcc.Graph(
                                figure=params.get(
                                    "efficient_frontier_continuous_color_plot"
                                )
                            ),
                            html.Hr(),
                            *params.get("simulated_stock_plots_lst"),
                            html.Hr(),
                            dcc.Graph(
                                figure=params.get("simulations_optimal_portfolio_plot")
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="Simulated Portfolios",
                        children=[
                            html.Div(
                                f'Find below the results of the portfolios {params.get("APP_NAME")} simulated for the '
                                f'sake of your wealth!'
                            ),
                            params.get("portfolios_simulated_dt"),
                        ],
                    ),
                ]
            ),
        ],
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
