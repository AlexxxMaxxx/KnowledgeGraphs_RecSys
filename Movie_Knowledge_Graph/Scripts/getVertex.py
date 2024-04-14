import getVertexEdge_func as gvef
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

multi_attr = ['genres', 'director', 'stars', 'countries']
# исходные данные
#AMOUNT_MOVIES = 10000    # самый полный датасет по кол-ву фильмов
AMOUNT_MOVIES = 56892    # самый полный датасет по кол-ву фильмов
#filePath_merged = '../../Datasets/random/10000_3+.csv'
filePath_merged = '../../Datasets/merged/dataset_' + str(AMOUNT_MOVIES) + '.csv'
filePath_multiAttr = '../../Datasets/merged/multi_attr_' + str(AMOUNT_MOVIES)

# сохранение
#filePath_vertex = '../../Datasets/visualization_vertex_edge/vertex_10000_3+.csv'
filePath_vertex = '../../Datasets/visualization_vertex_edge/vertex_' + str(AMOUNT_MOVIES) + '.csv'

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
    ma_path = filePath_multiAttr + '/' + ma + '.csv'
    ma_df = pd.read_csv(ma_path)
    vertex_df, next_id = gvef.getNewVertex(ma_df, ma, vertex_df, len(vertex_df) + 1)
    print(vertex_df.tail(10))

vertex_df.to_csv(filePath_vertex, index=False)
# для экспериментов возможно нужен укороченный датасет - изначально
# добавление ребер

