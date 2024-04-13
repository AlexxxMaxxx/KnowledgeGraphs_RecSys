import pandas as pd

N = 42000    # размер, до которого обрезаем
filePath_source = '../../Datasets/cut/keys_dict_42k.csv'
filePath_save = '../../Datasets/cut/keys_dict_' + str(int(N / 1000)) + 'k.csv'

key_df = pd.read_csv(filePath_source)
print(f'Длина датасета до обрезания = {len(key_df)}')

key_df = key_df[:N]
print(f'Длина датасета после обрезания = {len(key_df)}')

key_df.to_csv(filePath_save, index=False)