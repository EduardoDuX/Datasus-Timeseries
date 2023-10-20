import pandas as pd
from functions.preprocess import *
import numpy as np
from scipy import stats
import statsmodels.api as sm
import plotly.express as px

def linear(df, base_chosen, ano, agrupamento, transformacao, lambda_box_cox):
    if ano != []:
        df_ano = df[df['DATA'].apply(lambda x: int(x[:4])).isin(ano)].copy()
    else:
        df_ano = df.copy()
    # Preprocessa os dados
    if base_chosen == 'SINAN':
        df_process = preprocess_SINAN(df_ano, agrupamento)
    elif base_chosen == 'SIM':
        df_process = preprocess_SIM(df_ano, agrupamento)    
    if transformacao != 'Nenhum':
        if transformacao == 'Box-Cox' and lambda_box_cox != None:
            df_process['Casos'] = stats.boxcox(df_process['Casos'], lmbda = int(lambda_box_cox))

        elif transformacao == 'Tendência':
            tam = len(df_process['Casos'])
            lista = np.array(list(range(1,tam+1)))
            X = np.column_stack(lista)
            X = X.reshape([tam,1])

            Xm = X ** np.arange(0,5)

            model = sm.OLS(df_process['Casos'],Xm)
            results = model.fit()

            df_process['Casos'] = df_process['Casos']-results.predict(Xm)
    return px.line(data_frame=df_process, x=agrupamento, y='Casos', title=f'Gráfico por tempo')