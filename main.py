import numpy as np
import pandas as pd

from dash_main import app
from src.frontend.callbacks import *
from src.frontend.plots import *
from src.constants import params
from src.utils import *
from src.frontend.layout import layout


### inputs
# TODO:
# list of stocks (list of strings)
# filter by sector (list of strings)
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

    ###########################################################
    #################         FRONTEND                #################
    ###########################################################

    params["open_prices_plot"] = plot(data_step1, "Open", "Open prices")
    params["open_prices_plot"] = plot(data_step1, "Open", "Open prices")

    app.layout = layout
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
