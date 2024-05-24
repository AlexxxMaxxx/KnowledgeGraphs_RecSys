from surprise.model_selection import train_test_split
from surprise.model_selection import PredefinedKFold
from surprise.model_selection import GridSearchCV
from surprise import accuracy
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic

import additionalFunctions as af
import pandas as pd


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
    reader = Reader(line_format='user item rating', sep=',', rating_scale=(0.0, 5.0))
    train_file = train_file
    test_file = test_file
    folds_files = [(train_file, test_file)]

    ratings_data = Dataset.load_from_folds(folds_files, reader=reader)
    pkf = PredefinedKFold()

    for trainset, testset in pkf.split(ratings_data):
        train_data = trainset
        test_data = testset

    return ratings_data, train_data, test_data

def fit_test_KNNBasic(k, sim_options, ratings_data):
    model = KNNBasic(k=k, sim_options=sim_options)
    pkf = PredefinedKFold()

    for trainset, testset in pkf.split(ratings_data):
        # train and test algorithm.
        start_time = af.timer()
        model.fit(trainset)
        fit_time = af.timer() - start_time

        start_time = af.timer()
        predictions = model.test(testset)
        predict_time = af.timer() - start_time

        # Compute and print Root Mean Squared Error
        print(accuracy.rmse(predictions, verbose=True))

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




