import pandas as pd

filePath_genreId = '../datasets/genres.csv'
genreId_df = pd.read_csv(filePath_genreId)

filePath_genres = '../../Datasets/merged/comb4/df*_multi_attr/df*_genres.csv'
genres_df = pd.read_csv(filePath_genres)

for index, row in genres_df.iterrows():
    genreId = genreId_df.loc[genreId_df['title'] == row['genres'], 'genreId'].values
    if len(genreId) > 0:
        genres_df.at[index, 'genres'] = genreId[0]

genres_df = genres_df.rename(columns={'genres': 'genreId'})


filePath_movies = '../datasets/movies.csv'
movies = pd.read_csv(filePath_movies)
del movies['title']
del movies['releaseYear']
del movies['rating']
del movies['plot']
del movies['runtimes']
del movies['votes']
print(movies)

genres_df = pd.merge(genres_df, movies, on='movieId')
del genres_df['movieId']
print(genres_df)

genres_df = genres_df[genres_df['genreId'] != '(no genres listed)']
genres_df.to_csv('./movieGenre.csv', index=False)
