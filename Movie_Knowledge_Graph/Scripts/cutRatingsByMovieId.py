import pandas as pd

ratings_path = '../../Datasets/ratings.csv'
N = 4

filePath_df = '../../Datasets/experiments/subset/movies/df'
save_path = '../../Datasets/experiments/subset/ratings/df'

ratings_df = pd.read_csv(ratings_path)
print(f'Length ratings_df before: {len(ratings_df)}')

for i in range(1, N + 1):
    movies_df = pd.read_csv(filePath_df + str(i) + '.csv')
    print(f'Length movies_df before: {len(movies_df)}')
    # Оставляем только те записи из df1, чьи id есть в df2
    df_filtered = ratings_df[ratings_df['movieId'].isin(movies_df['movieId'])]
    print(f'Length ratings_df after: {len(df_filtered)}')
    df_filtered.to_csv(save_path + str(i) + '.csv', index=False)

    unique_ids = set(movies_df['movieId']) - set(df_filtered['movieId'])
    print(f'Количество фильмов для которых нет рейтингов: {len(unique_ids)}')
    movies_filtered = movies_df[~movies_df['movieId'].isin(unique_ids)]
    movies_filtered.to_csv(filePath_df + str(i) + '.csv', index=False)
    print(f'Length movies_df after: {len(movies_filtered)}')




