def preprocess(df, agrupamento):
    df2 = df.copy()
        
    if agrupamento == 'Anual':
        df2[agrupamento] = df2['DATA'].apply(lambda x: x[:4])
    elif agrupamento == 'Mensal':
        df2[agrupamento] = df2['DATA'].apply(lambda x: x[:7])
    else:
        df2[agrupamento] = df2['DATA']
        
    
    df2 = df2.groupby([agrupamento]).count().reset_index().rename(columns={'ID': 'Casos'})
    return df2