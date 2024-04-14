from sklearn.model_selection import train_test_split
import additionalFunctions as af
from gensim.models import Word2Vec
import pandas as pd
import os

def getTestData(SIZE_DF, test_size, random_state):
    _, testData = train_test_split(list(range(1, SIZE_DF)), test_size=test_size, random_state=random_state)
    return testData

def strExists(str, df):
    result = df[df['params'].str.contains(str, case=False, na=False)]
    if not result.empty:
        return True
    else:
        return False

def getInfoVertex(id, merged_df):
    return [row for index, row in merged_df.iterrows() if row['movieId'] == int(id)][0]

def getMovieId(vertex, filePath_vertex):
    row = [row for index, row in pd.read_csv(filePath_vertex).iterrows() if row['id'] == int(vertex)][0]
    splitStr = row['label'].split("_")
    return int(splitStr[len(splitStr)-1])

def estimateDiff(a, b, val1, val2):
    diff = abs(float(a) - float(b))
    return 1 if diff == 0 else 0.75 if diff <= val1 else 0.5 if diff <= val2 else 0

def compareMovie(target_movie, other_movie):
    real_similarity = 0

    real_similarity += estimateDiff(target_movie['rating'], other_movie['rating'], 0.5, 1.0)
    real_similarity += estimateDiff(target_movie['runtimes'], other_movie['runtimes'], 15, 30)
    real_similarity += estimateDiff(target_movie['releaseYear'], other_movie['releaseYear'], 5, 10)

    # длина пересечения
    genres_tm = set(target_movie['genres'].split("|"))
    genres_om = set(other_movie['genres'].split("|"))
    real_similarity += len(genres_tm & genres_om) / max(len(genres_tm), len(genres_om))

    return real_similarity

def get_most_similar(model, target_vertex, lastVertexId, topN, filePath_vertex, merged_df):
    similar_nodes = model.wv.most_similar(target_vertex, topn=pow(topN, 2))

    target_vertex = getInfoVertex(getMovieId(target_vertex, filePath_vertex), merged_df)
    real_similarity = 0
    counter_movies = 0

    for sim_node in similar_nodes:
        if counter_movies < topN:  # если еще не набрали
            vertex = int(sim_node[0])
            if vertex <= lastVertexId:  # если фильм
                real_similarity += compareMovie(target_vertex, getInfoVertex(getMovieId(vertex, filePath_vertex), merged_df))
                counter_movies += 1
            else:
                continue
        else:
            break

    return real_similarity / counter_movies if counter_movies != 0 else 0


fileName_merged_dataset = '../../Datasets/merged/dataset_40912.csv'
# ------------------------------
merged_df = pd.read_csv(fileName_merged_dataset, low_memory=False)
SIZE_DF = len(merged_df)
filePath_vertex = '../../Datasets/visualization_vertex_edge/vertex_' + str(SIZE_DF) + '.csv'
folder_emb = '../../Datasets/emb_data/' + str(SIZE_DF) + '/'
folder_model = folder_emb + 'model'
folder_emb_emb = folder_emb + 'emb'
filePath_statistics = folder_emb + 'statistics_df.csv'

flag_newDf = False

if af.fileExists(filePath_statistics):
    statistics_df = pd.read_csv(filePath_statistics)
    print('statistics_df существует')      # remove
    print(statistics_df.head(5))     # remove
else:
    statistics_df = pd.DataFrame(columns=['params', 'movie_match'])
    print('statistics_df не существует')
    flag_newDf = True

testData = getTestData(SIZE_DF, 0.1, 42)    # тестовый набор
SIZE_testData = len(testData)
SIZE_simVertex = round(SIZE_testData * 0.1)

for file in os.listdir(folder_model):
    combination = file[6:]
    model = Word2Vec.load(folder_model + '/' + file)

    if not flag_newDf and strExists(combination, statistics_df):
        continue    # если для комбинации уже вычислена метрика

    similarity = 0
    similarity = sum([get_most_similar(model, target_vertex, SIZE_DF, SIZE_simVertex, filePath_vertex, merged_df) for target_vertex in testData])
    statistics_df.loc[len(statistics_df)] = [combination, round(similarity / SIZE_testData, 4)]
    print(combination, round(similarity / SIZE_testData, 4))

    statistics_df = statistics_df.sort_values(by='movie_match', ascending=False)
    statistics_df.to_csv(filePath_statistics, index=False)