import numpy as np
import pandas as pd

from src.frontend.callbacks import *
from src.constants import params


def main():
    pass


params['START_DATE'] = get_start_date()
params['END_DATE'] = get_end_date()
params['STOCKS_LIST'] = get_list_stocks()

data = get_data(params)
### inputs
# list of stocks
# number of simulations
# value of investment


if __name__ == '__main__':
    main()