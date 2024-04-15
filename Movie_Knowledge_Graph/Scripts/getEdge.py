import getVertexEdge_func as gvef
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


multi_attr = ['genres', 'director', 'stars', 'countries']
# исходные данные
AMOUNT_MOVIES = 10694    # самый полный датасет по кол-ву фильмов

#AMOUNT_MOVIES = 56892    # самый полный датасет по кол-ву фильмов
filePath_multiAttr = '../../Datasets/merged/multi_attr_' + str(AMOUNT_MOVIES)

# сохранение
filePath_edge = '../../Datasets/visualization_vertex_edge/edge_' + str(AMOUNT_MOVIES) + '.csv'


data = {}
data['Source'] = []
data['Target'] = []
edge_df = pd.DataFrame(data)

input_df = pd.read_csv('../../Datasets/merged/dataset_' + str(AMOUNT_MOVIES) + '.csv')
vertex_df = pd.read_csv('../../Datasets/visualization_vertex_edge/vertex_' + str(AMOUNT_MOVIES) + '.csv')

dict_ma_df = {ma: pd.read_csv(filePath_multiAttr + '/' + ma + '.csv') for ma in multi_attr}

columns_names = input_df.columns
for i, row in input_df.iterrows():
    source = gvef.getVertexId(vertex_df, str(row['title']) + '_' + str(row['movieId']))
    targets = []
    targets.extend(
        [gvef.getVertexId(vertex_df, col_name + '_' + str(row[col_name])) for col_name in columns_names[1:] if
         col_name != 'title'])

    for name_attr, df in dict_ma_df.items():
        foundValue = df.loc[df['movieId'] == row['movieId'], name_attr].tolist()
        targets.extend([gvef.getVertexId(vertex_df, name_attr + '_' + str(fv)) for fv in foundValue])
    for j in range(0, len(targets)):
        edge_df.loc[len(edge_df)] = pd.Series({'Source': source, 'Target': targets[j]})


edge_df.to_csv(filePath_edge, index=False)



