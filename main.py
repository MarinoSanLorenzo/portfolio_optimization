import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import plotly

from dash_main import app
from src.frontend.callbacks import *
from src.frontend.plots import *
from src.constants import params
from src.utils import *
from src.frontend.layout import *


### inputs
# TODO:
# list of stocks (list of strings) multidropdown menu
# filter by sector (list of strings) multidropdown menu
# number of simulations (int)
# value of investment (float)


def main():
    ###########################################################
    #################       BACKEND                  #################
    ###########################################################
    params["stocks_info"] = params.get("STOCKS_INFO")
    params["START_DATE"] = get_start_date()
    params["END_DATE"] = get_end_date()
    params["STOCKS_LIST"] = get_list_stocks()

    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)

    data = data_step1


    @app.callback(Output('data', 'data'), [Input('chosen-stocks', 'value')])
    def update_data(chosen_stocks:list) -> pd.DataFrame:
        return data.query(f'stock_name in {chosen_stocks}')

    @app.callback(Output('open_prices_plot_all', 'figure'),
                  [Input('data', 'data')])
    def update_open_price_plot(data:pd.DataFrame) -> plotly.graph_objects.Figure:
        return plot(data, "Open", "Open prices")
    ###########################################################
    #################         FRONTEND                #################
    ###########################################################

    params["open_prices_plot"] = plot(data_step1, "Open", "Open prices")
    params["open_prices_plot"] = plot(data_step1, "Open", "Open prices")

    app.layout = get_layout(params)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
