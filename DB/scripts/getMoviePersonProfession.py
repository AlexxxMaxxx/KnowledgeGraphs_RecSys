import pandas as pd

filePath_id = './datasets/persons.csv'
id_df = pd.read_csv(filePath_id)
'''id_df['personId'] = 'nm' + id_df['personId'].astype(str)
print(id_df)
id_df.to_csv(filePath_id, index=False)'''

filePath_director = '../Datasets/merged/comb4/df*_multi_attr/df*_director.csv'
director_df = pd.read_csv(filePath_director)

director_df = pd.merge(director_df, id_df, left_on='director', right_on='name', how='left')
director_df = director_df.dropna()
director_df.reset_index(drop=True, inplace=True)
del director_df['name']
del director_df['director']
director_df['professionId'] = 'Q2526255'
print(director_df)


filePath_producer = '../Datasets/merged/comb4/df*_multi_attr/df*_producer.csv'
producer_df = pd.read_csv(filePath_producer)
producer_df = pd.merge(producer_df, id_df, left_on='producer', right_on='name', how='left')
producer_df = producer_df.dropna()
producer_df.reset_index(drop=True, inplace=True)
del producer_df['name']
del producer_df['producer']
producer_df['professionId'] = 'Q3282637'
print(producer_df)

df_concatenated = pd.concat([director_df, producer_df], ignore_index=True)
print(df_concatenated)


filePath_stars = '../Datasets/merged/comb4/df*_multi_attr/df*_stars.csv'
stars_df = pd.read_csv(filePath_stars)
stars_df = pd.merge(stars_df, id_df, left_on='stars', right_on='name', how='left')
stars_df = stars_df.dropna()
stars_df.reset_index(drop=True, inplace=True)
del stars_df['name']
del stars_df['stars']
stars_df['professionId'] = 'Q33999'
print(stars_df)

df_concatenated = pd.concat([df_concatenated, stars_df], ignore_index=True)
print(df_concatenated)

filePath_writer = '../Datasets/merged/comb4/df*_multi_attr/df*_writer.csv'
writer_df = pd.read_csv(filePath_writer)
writer_df = pd.merge(writer_df, id_df, left_on='writer', right_on='name', how='left')
writer_df = writer_df.dropna()
writer_df.reset_index(drop=True, inplace=True)
del writer_df['name']
del writer_df['writer']
writer_df['professionId'] = 'Q36180'
print(writer_df)

df_concatenated = pd.concat([df_concatenated, writer_df], ignore_index=True)
df_concatenated = df_concatenated.sort_values(by='movieId')
df_concatenated.reset_index(drop=True, inplace=True)
print(df_concatenated)

filePath_movies = './datasets/movies.csv'
movies = pd.read_csv(filePath_movies)
del movies['title']
del movies['releaseYear']
del movies['rating']
del movies['plot']
del movies['runtimes']
del movies['votes']
print(movies)

df_concatenated = pd.merge(df_concatenated, movies, on='movieId')
del df_concatenated['movieId']
print(df_concatenated)
df_concatenated.to_csv('./datasets/moviePersonProfession.csv', index=False)
