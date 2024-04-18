import pandas as pd
import numpy as np

filePath_source = '../../Datasets/movies.csv'
N = 4

df_source = pd.read_csv(filePath_source, low_memory=False)
df_source = df_source[:62420]

size_subset = int(len(df_source) / N)

df_parts = np.array_split(df_source, N)
i = 1
for df_part in df_parts:
    df_part.to_csv('../../Datasets/experiments/subset/movies/df' + str(i) + '.csv', index=False)
    i += 1
