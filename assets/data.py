import pandas as pd


dataset = {
    'SINAN':
        {
            'ZIKA': None,
            'DENGUE': None,
            'VIOL': None,
            'ACGR': None
        },
    'SIM': 
        {
            'DO': None,
            'DOMAT': None,
            'DOFET': None,
            'DOEXT': pd.read_csv('assets/Dados/SIM-DOEXT.csv')
        }
        
}