import pandas as pd


dataset = {
    'SINAN':
        {
            'ZIKA': pd.read_csv('./assets/Dados/SINAN-ZIKA.csv'),
            # 'DENGUE': pd.read_csv('./assets/Dados/SINAN-DENG.csv'),
            'VIOL': pd.read_csv('./assets/Dados/SINAN-VIOL.csv'),
            'ACGR': pd.read_csv('./assets/Dados/SINAN-ACGR.csv')
        },
    'SIM': 
        {
            # 'DO': pd.read_csv('./assets/Dados/SIM-DO.csv'),
            'DOMAT': pd.read_csv('./assets/Dados/SIM-DOMAT.csv'),
            'DOFET': pd.read_csv('./assets/Dados/SIM-DOFET.csv',low_memory=False),
            'DOEXT': pd.read_csv('./assets/Dados/SIM-DOEXT.csv')
        }
                
}