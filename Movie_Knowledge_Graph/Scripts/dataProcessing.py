import dataProcessing_func as dpf
import additionalFunctions as af
import pandas as pd

filePath_source = '../../Datasets/more_info/keys_dict.csv'
'''source_columns = ['IMDb_Id', 'cast', 'director', 'producer', 'writer', 'stars', 
                  'countries', 'rating', 'votes', 'top 250 rank', 'plot', 'runtimes']'''
# по умолчанию граф содержит movieId, genres, titles, releaseYears
# здесь указываем какие столбцы добавить, IMDb_Id - обязательно
# target_columns = ['IMDb_Id', 'director', 'rating', 'stars', 'countries', 'runtimes']
target_columns = ['IMDb_Id', 'rating', 'director',  'countries', 'stars', 'runtimes']

# исходные данные
multi_attr = ['genres', 'cast', 'director', 'producer', 'writer', 'stars', 'countries']

filePath_titles = '../../Datasets/more_info/titles.csv'
filePath_genres = '../../Datasets/more_info/genres.csv'
filePath_years = '../../Datasets/more_info/years.csv'

# куда сохранять - шаблон
filePath_merged = '../../Datasets/merged/dataset_'
filePath_multiAttr = '../../Datasets/merged/multi_attr_'

# Объединение датасетов в 1
input_df = pd.DataFrame(pd.read_csv(filePath_source))
input_df = input_df[target_columns]
# temp
input_df = input_df[:11000]


print(f'Исходный набор данных с выбранными колонками:\n {input_df.head(10)}')

# замена 'IMDb_Id' --> 'movieId'
input_df = dpf.replaceIMDbToMovieID(input_df)
print(f'Набор данных с movieId:\n {input_df.head(10)}')

# + title, genres и releaseYear - всегда добавляем
input_df = dpf.addColumn(input_df, filePath_titles, 'title')
input_df = dpf.addColumn(input_df, filePath_genres, 'genres')
input_df = dpf.addColumn(input_df, filePath_years, 'releaseYear')

# для удобства поменяем порядок
temp = input_df.pop('movieId')
input_df.insert(0, 'movieId', temp)
print(f'Набор данных, дополненный title, genres и releaseYear:\n {input_df.head(10)}')

# удаление строк с пустыми значениями
columns_names = input_df.columns
for col_name in columns_names[1:]:
    print(f'Len df before = {len(input_df)}')
    if col_name != 'releaseYear':
        input_df = dpf.checkAttribute(input_df, col_name, True)
    else:
        input_df = dpf.checkReleaseYear(input_df, True)
    print('Remove ' + col_name + f' -> Len df after = {len(input_df)}')

input_df.reset_index(drop=True, inplace=True)

add_name = str(len(input_df))
filePath_multiAttr += add_name
af.folderExists(filePath_multiAttr)

# если атрибут, который может иметь много значений, то обрабатываем иначе
for col_name in columns_names[1:]:
    if col_name in multi_attr:
        amountUniqueValue = dpf.getMaxAmountUniqueValue(input_df, col_name)
        print(f"Максимальное количество разных {col_name} в одной строке: {amountUniqueValue}")

        if amountUniqueValue > 10:
            amountUniqueValue = 10

        attr_df = dpf.splitAttribute(input_df, col_name, amountUniqueValue)
        attr_df.to_csv(filePath_multiAttr + '/' + col_name + '.csv', index=False)

        print(input_df.head(5))
        print(f'Полученный датасет: {attr_df.head(15)}')

        del input_df[col_name]
        #input_df = input_df.drop('column_name_to_drop', axis=1)

# что-то сделать с этими multi-attr-cols
print(f'Итоговый набор данных: {input_df}')
filePath_merged += add_name + '.csv'
input_df.to_csv(filePath_merged, index=False)
print(f'filePath_merged = \'{filePath_merged}\'')

