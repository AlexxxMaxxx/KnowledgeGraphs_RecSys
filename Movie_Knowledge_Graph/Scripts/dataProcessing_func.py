import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# замена 'IMDb_Id' --> 'movieId'
def replaceIMDbToMovieID(input_df):
    id_df = pd.read_csv('../../Datasets/more_info/id.csv')
    input_df['movieId'] = input_df['IMDb_Id'].map(id_df.set_index('IMDb_Id')['movieId'])
    del input_df['IMDb_Id']
    return input_df


def addColumn(input_df, filePath, colName):
    col_df = pd.read_csv(filePath)
    input_df[colName] = input_df['movieId'].map(col_df.set_index('movieId')[colName])
    return input_df


def checkAttribute(input_df, attribute, flag):
    input_df = input_df.dropna(subset=[attribute])
    input_df = input_df.drop(input_df[input_df[attribute] == ' '].index)

    if flag:
        print(f'Unique values:\n {input_df[attribute].unique()}')
    return input_df

def checkReleaseYear(input_df, flag):
    input_df = input_df.dropna(subset=['releaseYear'])
    input_df = input_df.drop(input_df[input_df['releaseYear'] == ' '].index)

    input_df = input_df.drop(input_df[input_df['releaseYear'] == 'Das Millionenspiel'].index)
    input_df = input_df.drop(input_df[input_df['releaseYear'] == 'Your Past Is Showing'].index)
    input_df = input_df.drop(input_df[input_df['releaseYear'] == 'Close Relations'].index)
    # 2006–2007?

    if flag:
        releaseYear_unique = input_df['releaseYear'].unique()
        print(f'Unique(releaseYear): {releaseYear_unique}\n')
    return input_df

def getMaxAmountUniqueValue(input_df, attribute):
    unique_value = input_df[attribute].unique()
    len_uv = []
    for uv in unique_value:
        len_uv.append(len(uv.split('|')))
    return max(len_uv)

def splitAttribute(input_df, attribute, amountUniqueValue):
    input_df = input_df[['movieId', attribute]]
    attr_df = pd.DataFrame(columns=['movieId', attribute])

    for i, row in input_df.iterrows():
        splitString = row[attribute].split('|')
        if len(splitString) > amountUniqueValue:
            splitString = splitString[:10]
        for single_attr in splitString:
            attr_df.loc[len(attr_df)] = [row['movieId'], single_attr]
    return attr_df


'''def splitAttribute(input_df, attribute, amountNewCols):
    attr_df = input_df[['movieId', attribute]]
    print(attr_df)

    сolsIndx = []
    startColIndx = attr_df.shape[1]

    for i in range(amountNewCols):
        new_column_name = f'{attribute}_{i + 1}'
        сolsIndx.append(startColIndx)
        startColIndx += 1
        attr_df.loc[:, new_column_name] = np.nan

    for i, row in attr_df.iterrows():
        splitString = row[attribute].split('|')

        for col_indx in сolsIndx:
            if splitString != []:
                attr_df.iloc[i, col_indx] = splitString.pop(0)
            else:
                break

    #del attr_df[attribute]
    return attr_df
'''

def mergeDatasets(df1, df2, on):
    return pd.merge(df1, df2, on=on, how='inner')
