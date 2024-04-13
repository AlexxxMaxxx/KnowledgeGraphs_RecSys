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

'''import pandas as pd
import numpy as np

filePath_merged = '../Datasets/merged/dataset_40912.csv'

filePath_save1 = '../Datasets/random/10k_1.csv'
filePath_save2 = '../Datasets/random/10k_2.csv'
filePath_save3 = '../Datasets/random/10k_3.csv'
filePath_save4 = '../Datasets/random/10k_4.csv'

size = 10000

df = pd.read_csv(filePath_merged, low_memory=False)
df = df[:40000]
print(len(df))

# Перемешиваем строки
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Разбиваем перемешанный датафрейм на 4 части по 10 тысяч строк в каждой
df_parts = np.array_split(df_shuffled, 4)

# Создаем 4 новых датафрейма из полученных частей
df_part1, df_part2, df_part3, df_part4 = df_parts

# Проверяем количество строк в каждом новом датафрейме
print(len(df_part1), len(df_part2), len(df_part3), len(df_part4))

df_part1.to_csv(filePath_save1, index=False)
df_part2.to_csv(filePath_save2, index=False)
df_part3.to_csv(filePath_save3, index=False)
df_part4.to_csv(filePath_save4, index=False)'''