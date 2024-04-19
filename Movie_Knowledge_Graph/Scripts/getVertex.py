import getVertexEdge_func as gvef
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#multi_attr = ['genres', 'cast', 'director', 'producer', 'writer', 'stars', 'countries']
# comb3: comb2 + director, producer
# исходные данные

df = 'df4'
comb = 'comb6'
multi_attr = ['genres', 'likes']
# посчитать для оставшихся комбинаций


filePath_merged = '../../Datasets/merged/' + comb + '/' + df + '_dataset.csv'
filePath_multiAttr = '../../Datasets/merged/' + comb + '/' + df + '_multi_attr'

# сохранение
filePath_vertex = '../../Datasets/visualization_vertex_edge/vertex/vertex_' + df + '_' + comb + '.csv'

input_df = pd.read_csv(filePath_merged)
print(input_df.head(10))

vertex_df = gvef.getVertexMovies(input_df)
print(f'фильмы-вершины: {vertex_df.tail(10)}')
print(f'amount movies = {len(vertex_df)}')

columns_names = input_df.columns
for col_name in columns_names[1:]:
    if col_name != 'title':
        vertex_df, next_id = gvef.getNewVertex(input_df, col_name, vertex_df, len(vertex_df) + 1)

for ma in multi_attr:
    ma_path = filePath_multiAttr + '/' + df + '_' + ma + '.csv'
    print(f'ma_path {ma_path}')
    ma_df = pd.read_csv(ma_path)
    print(f'ma_df {ma_df.head(10)}')
    vertex_df, next_id = gvef.getNewVertex(ma_df, ma, vertex_df, len(vertex_df) + 1)
    print(vertex_df.tail(10))

vertex_df.to_csv(filePath_vertex, index=False)
# для экспериментов возможно нужен укороченный датасет - изначально
# добавление ребер

