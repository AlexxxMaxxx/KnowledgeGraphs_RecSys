import pandas as pd

filePath_source= '../../Datasets/movies.csv'
df = pd.read_csv(filePath_source, low_memory=False)
size = len(df)

print(f'Len df = {len(df)}')
df.head(10)

shuffled_df = df.sample(n=size).reset_index(drop=True)
print(shuffled_df)

shuffled_df.to_csv(filePath_source, index=False)
