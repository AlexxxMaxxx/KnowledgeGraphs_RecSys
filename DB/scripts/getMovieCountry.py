import pandas as pd

filePath_countryId = '../datasets/countries.csv'
countryId_df = pd.read_csv(filePath_countryId)

filePath_countries = '../../Datasets/merged/comb4/df*_multi_attr/df*_countries.csv'
countries_df = pd.read_csv(filePath_countries)

for index, row in countries_df.iterrows():
    countryId = countryId_df.loc[countryId_df['title'] == row['countries'], 'countryId'].values
    if len(countryId) > 0:
        countries_df.at[index, 'countries'] = countryId[0]

countries_df = countries_df.rename(columns={'countries': 'countryId'})

filePath_movies = '../datasets/movies.csv'
movies = pd.read_csv(filePath_movies)
del movies['title']
del movies['releaseYear']
del movies['rating']
del movies['plot']
del movies['runtimes']
del movies['votes']
print(movies)

countries_df = pd.merge(countries_df, movies, on='movieId')
del countries_df['movieId']
print(countries_df)

countries_df.to_csv('./movieCountry.csv', index=False)
