import pandas as pd

filePath_merged = '../../Datasets/merged/dataset_27248.csv'
filePath_save = '../../Datasets/random/1k.csv'
size = 1000

df = pd.read_csv(filePath_merged, low_memory=False)
print(f'Len df = {len(df)}')
df.head(10)

shuffled_df = df.sample(n=size).reset_index(drop=True)
print(shuffled_df)
shuffled_df.to_csv(filePath_save, index=False)