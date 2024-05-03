import getVertexEdge_func as gvef
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def start(df, comb, multi_attr):
    # comb1 - для начала
    filePath_multiAttr = '../../Datasets/merged/' + comb + '/' + df + '_multi_attr'

    # сохранение
    filePath_edge = '../../Datasets/visualization_vertex_edge/edge/edge_' + df + '_' + comb + '.csv'

    data = {}
    data['Source'] = []
    data['Target'] = []
    edge_df = pd.DataFrame(data)

    input_df = pd.read_csv('../../Datasets/merged/' + comb + '/' + df + '_dataset.csv')
    vertex_df = pd.read_csv('../../Datasets/visualization_vertex_edge/vertex/vertex_' + df + '_' + comb + '.csv')

    dict_ma_df = {ma: pd.read_csv(filePath_multiAttr + '/' + df + '_' + ma + '.csv') for ma in multi_attr}

    columns_names = input_df.columns
    for i, row in input_df.iterrows():
        source = gvef.getVertexId(vertex_df, str(row['title']) + '_' + str(row['movieId']))
        targets = []
        targets.extend(
            [gvef.getVertexId(vertex_df, col_name + '_' + str(row[col_name])) for col_name in columns_names[1:] if
             col_name != 'title'])

        for name_attr, df in dict_ma_df.items():
            foundValue = df.loc[df['movieId'] == row['movieId'], name_attr].tolist()
            if name_attr == 'likes':
                print(f'foundValue = {foundValue}')
            targets.extend([gvef.getVertexId(vertex_df, name_attr + '_' + str(fv)) for fv in foundValue])
            if name_attr == 'likes':
                print('targets extend')
        for j in range(0, len(targets)):
            edge_df.loc[len(edge_df)] = pd.Series({'Source': source, 'Target': targets[j]})

    edge_df.to_csv(filePath_edge, index=False)


dfs = ['df1', 'df2', 'df3', 'df4']
#'df1',

#combs = ['comb1', 'comb2', 'comb3', 'comb4', 'comb5', 'comb6']
combs = ['comb6'] # 'comb6'

for comb in combs:
    if comb == 'comb1':
        multi_attr = ['genres']
    elif comb == 'comb2':
        multi_attr = ['genres', 'writer']
    elif comb == 'comb3':
        multi_attr = ['genres', 'writer', 'director', 'producer']
    elif comb == 'comb4':
        multi_attr = ['genres', 'writer', 'director', 'producer', 'stars', 'countries']
    elif comb == 'comb5':
        multi_attr = ['genres', 'writer', 'director', 'producer', 'stars', 'countries', 'likes']
    else:
        multi_attr = ['genres', 'likes']
    print(f'comb = {comb}')
    print(f'multi_attr = {multi_attr}')
    for df in dfs:
        print(f'df = {df}')
        start(df, comb, multi_attr)





