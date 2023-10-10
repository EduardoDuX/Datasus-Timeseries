def preprocess_SINAN(df):
    df = df.groupby(['DT_NOTIFIC']).count().reset_index().rename(columns={'DT_NOTIFIC': 'Data','ID_AGRAVO': 'Casos'})
    return df

def preprocess_SIM(df):
    df = df.groupby(['DATA']).count().reset_index().rename(columns={'DATA': 'Data','Unnamed: 0': 'Casos'})
    return df