import pytest
import pandas as pd
from src.frontend.callbacks import *
from src.utils import *
from src.constants import params
from src.frontend.plots import *

@pytest.fixture
def data() -> pd.DataFrame:
    params["stocks_info"] = params.get("STOCKS_INFO")
    params["START_DATE"] = get_start_date()
    params["END_DATE"] = get_end_date()
    params["STOCKS_LIST"] = get_list_stocks()

    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)
    return data_step1






class TestPlot:

    def test_plot_open_prices(self, data:pd.DataFrame) -> None:
        fig = plot(data, 'Open', 'Open prices')
        fig.show()