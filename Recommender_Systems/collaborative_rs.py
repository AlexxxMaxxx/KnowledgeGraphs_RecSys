from surprise.model_selection import train_test_split
from surprise.model_selection import GridSearchCV
from surprise import accuracy
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic

import additionalFunctions as af
import pandas as pd

from IPython.display import display
from surprise import SVD


def getInfo(ratings_df):
    print(f'Количество записей: {len(ratings_df)}')

    user_ids = ratings_df['userId'].unique()
    amount_users = len(user_ids)
    print(f'Количество уникальных пользователей: {amount_users}')

    movie_ids = ratings_df['movieId'].unique()
    amount_movies = len(movie_ids)
    print(f'Количество уникальных фильмов: {amount_movies}')

    print(f'Shape dataframe: {ratings_df.shape}')
    return amount_users, amount_movies


def checkDupl(ratings_df):
    len_df = len(ratings_df)
    len_df_drop_dupl = len(ratings_df.drop_duplicates())
    if len_df == len_df_drop_dupl:
        print('Очевидных дупликатов нет')
    else:
        print(f'{len_df_drop_dupl / len_df * 100} процентов данных являются дубликатами')


def typeRedefinition(ratings_df):
    ratings_df.loc[:, 'userId'] = ratings_df['userId'].astype('uint32')  # max value 4,294,967,295
    ratings_df.loc[:, 'movieId'] = ratings_df['movieId'].astype('uint32')  # max value 4,294,967,295
    ratings_df.loc[:, 'rating'] = ratings_df['rating'].astype('float16')    # max value 32,000
    return ratings_df


def startRatings(ratings_df, max_size):
    ratings_df.drop(['timestamp'], axis=1, inplace=True)
    ratings_df = ratings_df[:max_size]  # временно

    amount_users, amount_movies = getInfo(ratings_df)
    checkDupl(ratings_df)
    ratings_df = typeRedefinition(ratings_df)
    return ratings_df, len(ratings_df), amount_users, amount_movies


def startSurprise(ratings_df, test_size, train_file, test_file):
    reader = Reader(line_format='user item rating', rating_scale=(1, 5))
    ratings_data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader=reader)
    train_data, test_data = train_test_split(ratings_data, test_size=test_size, random_state=42)

    af.pickle_dump(train_file, train_data.build_testset())
    af.pickle_dump(test_file, test_data)
    return ratings_data, train_data, test_data


# Часто используют десятикратную прекрестную валидацию.
def gridSearch_KNNBasic(userBased, ratings_data):    # True or False
    model = KNNBasic()
    if userBased:
        title = 'KNNBasic_User'
        sim_options = {
            "name": ['cosine', 'msd', 'pearson'],
            "min_support": [3, 4, 5],
            "user_based": [True],
        }
    else:
        title = 'KNNBasic_Item'
        sim_options = {
            "name": ['cosine', 'msd', 'pearson'],
            "min_support": [3, 4, 5],
            "user_based": [False],
        }

    param_grid = {'k': [20, 40, 60], "sim_options": sim_options}

    gs = GridSearchCV(KNNBasic, param_grid, measures=["rmse", "mae"], cv=10, refit=True, n_jobs=-1)
    # cv=5 - 90% обучение, 10% - тест
    gs.fit(ratings_data)

    # результаты
    print(f'Grid Search {title}')
    print(f'Best MAE = {gs.best_score["mae"]}')
    print(f'Best RMSE = {gs.best_score["rmse"]}')
    print(f'Best params RMSE = {gs.best_params["rmse"]}')

    return gs.best_params["rmse"]['k'], gs.best_params["rmse"]['sim_options']


def fit_test_KNNBasic(k, sim_options, train_data, test_data):
    model = KNNBasic(k=k, sim_options=sim_options)

    start_time = af.timer()
    model.fit(train_data)
    fit_time = af.timer() - start_time

    start_time = af.timer()
    predictions = model.test(test_data)
    predict_time = af.timer() - start_time

    return model, round(fit_time, 4), predictions, round(predict_time, 4)

def rmse(predictions):
    return accuracy.rmse(predictions)

def mae(predictions):
    return accuracy.mae(predictions)

def createInfoDF():
    return pd.DataFrame(columns=['dataset_name', 'amount_records', 'use_amount_records', 'fraction_test',
                                    'type_RS', 'params', 'mae', 'rmse',
                                    't_fit', 't_pred', 't_all'])    # mem?

#gs_item = gridSearch_KNNBasic(False)
# KNNBasic itemBased
# add result table
# param = nan - неправильно
# предупреждение
# большой вывод от грида
# запуск для ItemBased
# 🥠
# оптимизации?




