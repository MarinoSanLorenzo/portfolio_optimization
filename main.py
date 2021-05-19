import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.express as px
import json

from dash_main import app
from src.frontend.callbacks import *
from src.frontend.plots import *
from src.constants import params
from src.utils import *
from src.frontend.layout import *
from src.frontend.components import *
from src.portfolio_optimization import *


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
    chosen_stocks = list(params.get("STOCKS_INFO").keys())
    params['chosen_stocks'] = chosen_stocks
    params["stocks_info"] = params.get("STOCKS_INFO")
    params["START_DATE"] = get_start_date()
    params["END_DATE"] = get_end_date()
    params["STOCKS_LIST"] = get_list_stocks()

    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)
    covariance_tbl = get_covariance_tbl(data_step1)
    correlation_tbl = get_correlation_tbl(data_step1)

    data = data_step1


    ###########################################################
    #################         FRONTEND                #################
    ###########################################################

    params['data'] = data
    params["open_prices_plot_all"] = plot(data, "Open", "Open prices")
    params["open_prices_plot_lst"] = add_layout_components_for_multiple_plots(plot_low_high_prices, data, params)
    params['covariance_tbl_dt'] = get_data_table(covariance_tbl)
    params['correlation_tbl_dt'] = get_data_table(correlation_tbl)


    app.layout = get_layout(params)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
