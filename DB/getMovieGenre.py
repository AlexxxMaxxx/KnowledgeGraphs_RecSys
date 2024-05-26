import pandas as pd

filePath_genreId = '../DB/genres.csv'
genreId_df = pd.read_csv(filePath_genreId)

filePath_genres = '../Datasets/merged/comb4/df*_multi_attr/df*_genres.csv'
genres_df = pd.read_csv(filePath_genres)

for index, row in genres_df.iterrows():
    genreId = genreId_df.loc[genreId_df['title'] == row['genres'], 'genreId'].values
    if len(genreId) > 0:
        genres_df.at[index, 'genres'] = genreId[0]

countries_df = genres_df.rename(columns={'genres': 'genreId'})
countries_df.to_csv('./movieGenre.csv', index=False)
