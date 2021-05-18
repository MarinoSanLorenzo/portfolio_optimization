import datetime
from collections import namedtuple

Stock = namedtuple("Stock", "name code sector rank")

stocks_info = {
    "Nestlé": Stock("Nestlé", "NESN.SW", "Food", "1"),
    "Novartis AG": Stock("Novartis AG", "NOVN.SW", "Pharmaceuticals", "2"),
    "Roche Holding AG ": Stock("Roche Holding AG", "ROG.SW", "Pharmaceuticals", "3"),
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
    "SMI PR": Stock("SMI PR", "^SSMI", "Index", "14"),
}

code_name_mapping = {v.code: v.name for v in stocks_info.values()}
code_rank_mapping = {v.code: v.sector for v in stocks_info.values()}

params = {
    "STOCKS_INFO": stocks_info,
    "CODE_NAME_MAPPING": code_name_mapping,
    "CODE_RANK_MAPPING": code_rank_mapping,
    "STYLE_SHEET": ["https://codepen.io/chriddyp/pen/bWLwgP.css"],
}
