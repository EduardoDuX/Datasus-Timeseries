def preprocess_SINAN(df, agrupamento):
    if agrupamento == 'Anual':
        df['DATA'] = df['DATA'].apply(lambda x: x[:4])
    if agrupamento == 'Mensal':
        df['DATA'] = df['DATA'].apply(lambda x: x[:7])
        
    df = df.loc[df['DATA'].apply(lambda x: len(str(x))) > 8]

    df = df.groupby(['DT_NOTIFIC']).count().reset_index().rename(columns={'DT_NOTIFIC': 'Data','ID_AGRAVO': 'Casos'})
    return df

def preprocess_SIM(df, agrupamento):
    df2 = df.copy()
    
    df2 = df2.loc[df2['DATA'].apply(lambda x: len(str(x))) > 8]
    
    if agrupamento == 'Anual':
        df2[agrupamento] = df2['DATA'].apply(lambda x: x[:4])
    elif agrupamento == 'Mensal':
        df2[agrupamento] = df2['DATA'].apply(lambda x: x[:7])
    else:
        df2[agrupamento] = df2['DATA']
        
    
    df2 = df2.groupby([agrupamento]).count().reset_index().rename(columns={'Unnamed: 0': 'Casos'})
    return df2