# берем файл рейтингов, обрезанный под merge - в нем есть только те фильмы, которые есть в датасете с фильмами
# в этом датасете, удаляем все строки, где значение рейтинга меньше заданного
# удаляем сам столбец рейтинга - больше не нужен
# и теперь нужно преобразовать эту штуку в формат multipleAttr - а он наверное в нем и есть - проверить
# этот файл просто отправляем как multipleAttr
# ну и все пересчитываем вершины, ребра - эмбеддинги - предсказания

# запускаем после обработки датасетов, но перед построением вершин
# будем считать,
import pandas as pd
# запустить еще с threshold = 4.5, 4.0
threshold = 4.5946
combs = ['comb5', 'comb6']
dfs = ['df1', 'df2', 'df3', 'df4']

for comb in combs:
    for df in dfs:
        filePath_ratings = '../../Datasets/merged/' + comb + '/ratings_' + df + '.csv'
        ratings_df = pd.read_csv(filePath_ratings)
        del ratings_df['timestamp']
        print(ratings_df.head(10))

        # Удаляем строки, где значение в столбце 'rating' меньше порога
        ratings_df = ratings_df[ratings_df['rating'] >= threshold]
        ratings_df.rename(columns={'userId': 'likes'}, inplace=True)
        del ratings_df['rating']
        new_order = ['movieId', 'likes']
        ratings_df = ratings_df[new_order]
        # Сортируем DataFrame по столбцу movieId
        ratings_df = ratings_df.sort_values(by='movieId')

        print(ratings_df.head(10))

        filePath_likes = '../../Datasets/merged/' + comb + '/' + df + '_multi_attr/' + df + '_likes.csv'
        ratings_df.to_csv(filePath_likes, index=False)
