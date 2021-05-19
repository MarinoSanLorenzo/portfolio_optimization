import pytest
import pandas as pd
from src.frontend.callbacks import *
from src.utils import *
from src.constants import params
from src.frontend.plots import *
from src.frontend.components import *

@pytest.fixture
def stock() -> str:
    tock = 'Nestlé'
    return stock

@pytest.fixture
def data() -> pd.DataFrame:
    chosen_stocks = list(params.get("STOCKS_INFO").keys())
    params['chosen_stocks'] = chosen_stocks
    params["stocks_info"] = params.get("STOCKS_INFO")
    params["START_DATE"] = get_start_date()
    params["END_DATE"] = get_end_date()
    params["STOCKS_LIST"] = get_list_stocks()
    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)
    return data_step1

class TestLayoutComponents:

     def test_add_layout_components_for_multiple_plots(self, data):
         open_prices_plot_lst = add_layout_components_for_multiple_plots(plot_low_high_prices, data, params)
         assert isinstance(open_prices_plot_lst, list)
         assert len(open_prices_plot_lst) == 2*len(params['chosen_stocks'])