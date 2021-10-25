import pandas as pd
import os

def LoadPrerecordedResults():
    if os.path.exists('Data/Results.xlsx'):
        # As results are stored by category in sheets of Results.xlsx, collect all and concat
        df = pd.read_excel('Data/Results.xlsx',sheet_name=None)
        df = (pd.concat(list(df.values()))
                .sort_values("TOTAL"))
        
        dataBase = [df, True]
    else:
        dataBase = [None, False]
    return dataBase

def LoadData(binaryObject):
    df = pd.read_excel(binaryObject,header=None)

    categs_index = df[df.iloc[:,-2] == 'NOMBRE'].index - 1
    cols_names = df.iloc[1].values
    categs = df.loc[categs_index,0].values

    df_final = pd.DataFrame()

    for i in range(len(categs_index)):
        try: df_i = df.iloc[categs_index[i]+2:categs_index[i+1]]
        except: df_i = df.iloc[categs_index[i]+2:]
        
        cat_i = categs[i]
        df_i.columns = cols_names
        df_i = df_i.dropna(axis=0,how='all')
        df_i['CATEGORIA'] = cat_i
        df_final = pd.concat([df_final,df_i])

    dataBase = (df_final
                .reindex(columns=['NOMBRE','NÚMERO','CATEGORIA','HORA SALIDA','HORA LLEGADA', 'TOTAL',
                              'POSICIÓN','CANTIDAD'])
                .drop(columns='CANTIDAD'))

    dataBase['NÚMERO'] = dataBase['NÚMERO'].astype(int)
    dataBase['NOMBRE'] = dataBase['NOMBRE'].str.title()  # Convert to name format (capitalize only first character of each word)

    return dataBase
