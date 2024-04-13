# Строим эмбеддинги не для всех возможных фильмов, следовательно, из рейтингов нужно удалить лишнее.
import pandas as pd

def getListMoviesId(filePath_vertex):
    moviesId = []
    for index, row in pd.read_csv(filePath_vertex).iterrows():
        if index < lastMovieId:
            splitStr = row['label'].split("_")
            moviesId.append(int(splitStr[len(splitStr)-1]))
        else:
            break
    return moviesId

# тут меняем-.-.-.-.-.-.-.-.-.-
ratings_path = '../../Datasets/ratings.csv'
filePath_vertex = '../../Datasets/visualization_vertex_edge/vertex_10000_4.csv'
save_path = '../../Datasets/cutRatings/ratings_10000_4.csv'
lastMovieId = 10000
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-

moviesId = getListMoviesId(filePath_vertex)

ratings_df = pd.read_csv(ratings_path)
print(f'Length before: {len(ratings_df)}')

ratings_df = ratings_df[ratings_df['movieId'].isin(moviesId)]
print(f'Length after: {len(ratings_df)}')

ratings_df.to_csv(save_path, index=False)
print('success')
