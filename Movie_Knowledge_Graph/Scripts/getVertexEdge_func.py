import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def getVertexMovies(input_df):
    vertex_df = pd.DataFrame({'id': range(1, len(input_df) + 1)})
    vertex_df['label'] = input_df.apply(lambda input_df: f"{input_df['title']}_{input_df['movieId']}", axis=1)
    return vertex_df

def getNewVertex(input_df, col_name, vertex_df, next_id):
    unique_values = input_df[col_name].unique()
    print(f'unique_values {unique_values}')
    print(f'col_name {col_name}')
    for i in range(0, len(unique_values)):
        vertex_df.loc[len(vertex_df)] = pd.Series({'id': next_id, 'label': col_name + '_' + str(unique_values[i])})
        next_id += 1

    return vertex_df, next_id

def getVertexId(vertex_df, label):
    return int(vertex_df[vertex_df['label'] == str(label)]['id'].values)
