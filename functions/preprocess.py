def preprocess_SINAN(df, agrupamento):
    if agrupamento == 'Anual':
        df['DATA'] = df['DATA'].apply(lambda x: x[:4])
    if agrupamento == 'Mensal':
        df['DATA'] = df['DATA'].apply(lambda x: x[:7])
    df = df.groupby(['DT_NOTIFIC']).count().reset_index().rename(columns={'DT_NOTIFIC': 'Data','ID_AGRAVO': 'Casos'})
    return df

def preprocess_SIM(df, agrupamento):
    df2 = df.copy()
    if agrupamento == 'Anual':
        df2['DATA'] = df2['DATA'].apply(lambda x: x[:4])
    if agrupamento == 'Mensal':
        df2['DATA'] = df2['DATA'].apply(lambda x: x[:7])

    df2 = df2.groupby(['DATA']).count().reset_index().rename(columns={'DATA': 'Data','Unnamed: 0': 'Casos'})
    return df2