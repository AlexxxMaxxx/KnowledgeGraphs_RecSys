import additionalFunctions as af
import sys
sys.path.append('../Recommender_Systems/')
from collaborative_rs import *
import pandas as pd

# Тут меняем-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
max_size = 100000  # временно
test_size = 0.05
dataset_name = '10694'

ratings_path = '../Datasets/cutRatings/ratings_' + dataset_name + '.csv'
RS_type = 'KNNBasic_User'    # KNNBasic_Item
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.

folderName = '../Datasets/experiments/collaborative_rs/' + RS_type + '/' + dataset_name
af.folderExists(folderName)

filePath_results = folderName + '/info_df.csv'
predictions_filePath = folderName + '/predictions_df.csv'
train_file = folderName + '/train_data_' + dataset_name + '.pkl'
test_file = folderName + '/test_data_' + dataset_name + '.pkl'

af.folderExists(folderName + '/models')
RS_model_filePath = folderName + '/models/' + RS_type + '.pkl'

if af.fileExists(filePath_results):
    info_df = pd.read_csv(filePath_results)
    print('movies exist')
else:
    info_df = createInfoDF()
    print('movies create')

ratings_df, initLen_Ratings, amount_users, amount_movies = startRatings(pd.read_csv(ratings_path), max_size)
ratings_data, train_data, test_data = startSurprise(ratings_df, test_size, train_file, test_file)

if af.fileExists(RS_model_filePath):
    loaded_model = af.pikcle_load(RS_model_filePath)
    predictions = loaded_model.test(test_data)

    print(f'mae = {round(accuracy.mae(predictions), 4)}')
    print(f'rmse = {round(accuracy.rmse(predictions), 4)}')

    # что с ней делать дальше?
else:
    start_time = af.timer()
    best_k, best_sim_options = gridSearch_KNNBasic(True, ratings_data)    # KNNBasic userBased

    model, fit_time, predictions, predict_time = fit_test_KNNBasic(best_k, best_sim_options, train_data, test_data)
    af.pickle_dump(RS_model_filePath, model)    # сохранение модели
    all_time = af.timer() - start_time

    info_df.loc[len(info_df)] = [dataset_name, initLen_Ratings, max_size, test_size, RS_type,
                                 str(best_k) + ' ' + str(best_sim_options), round(mae(predictions), 4),
                                 round(rmse(predictions), 4), fit_time, predict_time, round(all_time, 4)]
    # "{:.4f}".format(number)
    print(info_df.tail(5))
    info_df.to_csv(filePath_results, index=False)

columns = ['userId', 'movieId', 'rating', 'pred', 'other']
df = pd.DataFrame(predictions, columns=columns)
df.to_csv(predictions_filePath, index=False)