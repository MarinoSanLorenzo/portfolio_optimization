import datetime
from collections import namedtuple

Stock = namedtuple('Stock', 'name code rank sector')

stocks_info = {'Nestlé':Stock('Nestlé','NESN', 'Food', '1'),
               'Novartis': Stock('Novartis','NOVN', 'Pharmaceuticals', '2'),
                'Hoffmann-La Roche':Stock('Hoffmann-La Roche','RO', 'Pharmaceuticals', '3'),
                'Zurich Insurance Group':Stock('Zurich Insurance Group','ZURN', 'Insurance', '4'),
                'UBS':Stock('UBS','UBSG', 'Banking', '5'),
                'ABB Ltd':Stock('ABB Ltd','ABB', 'Industry', '6'),
                'Compagnie Financiere Richemont SA':Stock('ABB Ltd','CFR', 'Luxury', '7'),
                'Lonza':Stock('Lonza','LONN', 'Chemicals', '8'),
                'Givaudan':Stock('Givaudan','GIVN', 'Chemicals', '9'),
                'Alcon':Stock('Alcon','ALC', 'Pharmaceuticals', '10'),
                'Sika':Stock('Sika','SIKA', 'Chemicals', '11'),
                'Swiss Re':Stock('Swiss Re','SREN', 'Insurance', '12'),
                'Crédit suisse':Stock('Crédit suisse','CS', 'Banking', '13'),

               }

params = {

}
