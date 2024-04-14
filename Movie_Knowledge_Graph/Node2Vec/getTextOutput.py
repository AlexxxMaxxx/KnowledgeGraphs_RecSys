from gensim.models import Word2Vec
import pandas as pd

def getInfoVertex(id, merged_df):
    return [row for index, row in merged_df.iterrows() if row['movieId'] == int(id)][0]

def getMovieId(vertex, filePath_vertex):
    row = [row for index, row in pd.read_csv(filePath_vertex).iterrows() if row['id'] == int(vertex)][0]
    splitStr = row['label'].split("_")
    return int(splitStr[len(splitStr)-1])

def detailedOutput(infoVertex):
    title = infoVertex['title']
    rating = infoVertex['rating']
    runtimes = infoVertex['runtimes']
    releaseYear = infoVertex['releaseYear']
    genres = infoVertex['genres']
    return f'Фильм {title} с рейтингом {rating}, продолжительностью {runtimes} мин, {releaseYear} года выпуска, ' \
           f'\nжанры: {genres} '

# тут меняем
fileName_merged_dataset = '../../Datasets/random/1k.csv'
strCombination = '8_10_5_2'

# по умолчанию
merged_df = pd.read_csv(fileName_merged_dataset)
SIZE_DF = lastVertexId = len(merged_df)

filePath_vertex = '../../Datasets/visualization_vertex_edge/vertex_' + str(SIZE_DF) + '.csv'

model = Word2Vec.load('../../Datasets/emb_data/' + str(SIZE_DF) +'/model/model_' + strCombination)
counter_movies = 0
# тут меняем
target_vertex = '1'
topN = 10

similar_nodes = model.wv.most_similar(target_vertex, topn=pow(topN, 2))
infoVertex = getInfoVertex(getMovieId(target_vertex, filePath_vertex), merged_df)
print(detailedOutput(infoVertex))
print('\n')

for sim_node in similar_nodes:
    if counter_movies < topN:    # если еще не набрали
        vertex = int(sim_node[0])
        if vertex <= lastVertexId:    # если фильм
            print(f'Похож на {round(sim_node[1] * 100, 2)}% на')
            print(detailedOutput(getInfoVertex(getMovieId(vertex, filePath_vertex), merged_df)))
            print('\n\n')
            counter_movies += 1
    else:
        break
