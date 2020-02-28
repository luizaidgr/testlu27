import pandas as pd

def ret_mes(cota):
    df=cota.copy()
    df.index = pd.to_datetime(df.index)
    dfmax = df.iloc[df.reset_index().groupby(df.index.to_period('M'))['Date'].idxmax()]
    dfmin = df.iloc[df.reset_index().groupby(df.index.to_period('M'))['Date'].idxmin()]

    #cdi time
    cdi = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/CDI.csv',sep=',', index_col=0)
    cdi.index = pd.to_datetime(cdi.index)

    df2 = pd.merge(dfmax,cdi, left_index=True, right_index=True)
    df2 = df2.drop(['CDI', 'SELIC'], 1)
    df4=df2['CDI_ACUM']
    df2= df2.pct_change(1)

    df3=pd.merge(dfmin,cdi, left_index=True, right_index=True)
    df3 = df3.drop(['CDI', 'SELIC'], 1)

    df2['cota'] = df2.cota.fillna(dfmax.iloc[0][0]/dfmin.iloc[0][0]-1)
    df2['CDI_ACUM'] = df2.CDI_ACUM.fillna(df4.iloc[0]/df3.iloc[0,1]-1)

    return df2
def ret_ano(cota):
    df=cota.copy()
    df.index = pd.to_datetime(df.index)
    #nome da serie = list(df.columns)[0]
    dfmax = df.iloc[df.reset_index().groupby(df.index.to_period('Y'))['Date'].idxmax()]
    dfmin = df.iloc[df.reset_index().groupby(df.index.to_period('Y'))['Date'].idxmin()]


    #cdi time
    cdi = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/CDI.csv',sep=',', index_col=0)
    cdi.index = pd.to_datetime(cdi.index)

    df2 = pd.merge(dfmax,cdi, left_index=True, right_index=True)
    df2 = df2.drop(['CDI', 'SELIC'], 1)
    df4 = df2['CDI_ACUM']
    df2= df2.pct_change(1)

    df3 = pd.merge(dfmin, cdi, left_index=True, right_index=True)
    df3 = df3.drop(['CDI', 'SELIC'], 1)

    df2['cota'] = df2.cota.fillna(dfmax.iloc[0][0] / dfmin.iloc[0][0] - 1)
    df2['CDI_ACUM'] = df2.CDI_ACUM.fillna(df4.iloc[0]/df3.iloc[0,1]-1)

    return df2

def ret_ini(cota,year):
    df=cota.copy()
    df.index = pd.to_datetime(df.index)
    cdi = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/CDI.csv',sep=',', index_col=0)
    cdi.index = pd.to_datetime(cdi.index)
    df_0 = pd.merge_asof(df.reset_index(), cdi.reset_index().rename(columns={'index': 'Date'}), on='Date').drop(['CDI', 'SELIC'], 1)

    #nome da serie = list(df.columns)[0]
    df = df.iloc[df.reset_index().groupby(df.index.to_period('Y'))['Date'].idxmax()]
    df['Year'] = df.index.year
    df = df.loc[df['Year'] == year].drop('Year', 1)
    df = df / cota.iloc[0]
    #cdi time

    df2 = pd.merge(df,cdi, left_index=True, right_index=True)
    df2 = df2.drop(['CDI', 'SELIC'], 1)
    df2['CDI_ACUM'] = df2['CDI_ACUM'] / df_0['CDI_ACUM'].iloc[0]

    return df2

