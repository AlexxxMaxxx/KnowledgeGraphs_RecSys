import pandas as pd

filePath_movies = '../Datasets/merged/comb4/df*_dataset.csv'
movies_df = pd.read_csv(filePath_movies)
movies_df = movies_df[['movieId', 'title', 'releaseYear', 'rating', 'runtimes']]
print(movies_df)

filePath_id = '../Datasets/more_info/id.csv'
id_df = pd.read_csv(filePath_id)
print(id_df)

movies_df = pd.merge(movies_df, id_df, on='movieId')
print(movies_df)

filePath_keys = '../Datasets/more_info/keys_dict.csv'
keys_df = pd.read_csv(filePath_keys)
keys_df.drop(columns=['cast'], inplace=True)
keys_df.drop(columns=['director'], inplace=True)
keys_df.drop(columns=['producer'], inplace=True)
keys_df.drop(columns=['writer'], inplace=True)
keys_df.drop(columns=['stars'], inplace=True)
keys_df.drop(columns=['countries'], inplace=True)
keys_df.drop(columns=['rating'], inplace=True)
keys_df.drop(columns=['top 250 rank'], inplace=True)
keys_df.drop(columns=['runtimes'], inplace=True)
print(keys_df)

movies_df = pd.merge(movies_df, keys_df, on='IMDb_Id')
print(movies_df)
print(movies_df.columns)

movies_df.drop(columns=['IMDb_Id'], inplace=True)
print(movies_df)
print(movies_df.columns)

movies_df = movies_df.rename(columns={'tt_IMDb_Id': 'IMDb_Id'})
print(movies_df)
print(movies_df.columns)

movies_df = movies_df[['movieId', 'IMDb_Id', 'title', 'releaseYear', 'rating', 'plot', 'runtimes', 'votes']]
print(movies_df)

movies_df.to_csv('./movies.csv', index=False)
