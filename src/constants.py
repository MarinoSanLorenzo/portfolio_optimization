import datetime
from collections import namedtuple

Stock = namedtuple("Stock", "name code sector market_rank")

stocks_info = {
    "Nestlé": Stock("Nestlé", "NESN.SW", "Food", "1"),
    "Novartis AG": Stock("Novartis AG", "NOVN.SW", "Pharmaceuticals", "2"),
    "Roche Holding AG": Stock("Roche Holding AG", "ROG.SW", "Pharmaceuticals", "3"),
    "Zurich Insurance Group AG": Stock(
        "Zurich Insurance Group AG", "ZURN.SW", "Insurance", "4"
    ),
    "UBS Group AG": Stock("UBS Group AG", "UBSG.SW", "Banking", "5"),
    # TODO: update the yahoo finance code
    # 'ABB Ltd':Stock('ABB Ltd','ABB', 'Industry', '6'),
    # 'Compagnie Financiere Richemont SA':Stock('ABB Ltd','CFR', 'Luxury', '7'),
    # 'Lonza':Stock('Lonza','LONN', 'Chemicals', '8'),
    # 'Givaudan':Stock('Givaudan','GIVN', 'Chemicals', '9'),
    # 'Alcon':Stock('Alcon','ALC', 'Pharmaceuticals', '10'),
    # 'Sika':Stock('Sika','SIKA', 'Chemicals', '11'),
    # 'Swiss Re AG':Stock('Swiss Re AG','SREN.SW', 'Insurance', '12'),
    # 'Crédit suisse':Stock('Crédit suisse','CS', 'Banking', '13'),
    # "SMI PR": Stock("SMI PR", "^SSMI", "Index", "14"),
}

code_name_mapping = {v.code: v.name for v in stocks_info.values()}
code_rank_mapping = {v.code: v.sector for v in stocks_info.values()}

external_stylesheets = [
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    ' https://codepen.io/chriddyp/pen/dZVMbK.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
params = {
    "STOCKS_INFO": stocks_info,
    "CODE_NAME_MAPPING": code_name_mapping,
    "CODE_RANK_MAPPING": code_rank_mapping,
    # "STYLE_SHEET": ["https://codepen.io/chriddyp/pen/bWLwgP.css"],
    "STYLE_SHEET": external_stylesheets,
    'APP_NAME':'Wealth Management app',
    "START_DATE" : datetime.datetime(2019, 1, 1),
    "END_DATE" : datetime.date.today(),
    'num_simulations': 100,
    'num_simulations_stock': 100,
    'investment_amount': 1_000,
    'lower_quantile_lvl': 0.05,
    'upper_quantile_lvl': 0.95,
    'params_to_show':['STOCKS_INFO',
                         'CODE_NAME_MAPPING',
                         'CODE_RANK_MAPPING',
                         'STYLE_SHEET',
                         'APP_NAME',
                         'START_DATE',
                         'END_DATE',
                         'num_simulations',
                         'num_simulations_stock',
                         'investment_amount',
                         'lower_quantile_lvl',
                         'upper_quantile_lvl']
}
