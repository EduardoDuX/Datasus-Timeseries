import pandas as pd
import plotly.express as px

MONTHS = {'01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr', '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago', '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'}

def plot_seasonality(df, x, agrupamento):
    df_season = df.copy()

    if 'Dia' in (x, agrupamento):
        df_season['Dia'] = df_season['DATA'].apply(lambda y: str(y)[8:])
    if 'Mes' in (x, agrupamento):
        df_season['Mes'] = df_season['DATA'].apply(lambda y: str(y)[5:7])
    if 'Ano' in (x, agrupamento):
        df_season['Ano'] = df_season['DATA'].apply(lambda y: str(y)[:4])

    df_season = df_season[[x, agrupamento, 'Unnamed: 0']].groupby([x, agrupamento]).sum().reset_index().rename(columns={'Unnamed: 0': 'Casos'})

    df_season.sort_values(by=x)
    
    if 'Mes' in (x, agrupamento):
        df_season['Mes'] = df_season['Mes'].apply(lambda y: MONTHS[y])

    graph = px.line(df_season, x, 'Casos', color = agrupamento)
    return graph