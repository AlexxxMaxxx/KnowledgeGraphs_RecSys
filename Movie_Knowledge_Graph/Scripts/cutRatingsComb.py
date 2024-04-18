import pandas as pd

combs = ['comb1', 'comb2', 'comb3', 'comb4']

for comb in combs:
    dfs = ['df1', 'df2', 'df3', 'df4']
    for df in dfs:
        filePath_sourceMovies = '../../Datasets/merged/' + comb + '/' + df + '_dataset.csv'
        movies_df = pd.read_csv(filePath_sourceMovies)
        print(f'Length movies_df: {len(movies_df)}')

        filePath_sourceRatings = '../../Datasets/experiments/subset/ratings/' + df + '.csv'
        ratings_df = pd.read_csv(filePath_sourceRatings)
        print(f'Length ratings_df before: {len(ratings_df)}')

        df_filtered = ratings_df[ratings_df['movieId'].isin(movies_df['movieId'])]
        print(f'Length ratings_df after: {len(df_filtered)}')

        save_path = '../../Datasets/merged/' + comb + '/ratings_' + df + '.csv'
        df_filtered.to_csv(save_path, index=False)

