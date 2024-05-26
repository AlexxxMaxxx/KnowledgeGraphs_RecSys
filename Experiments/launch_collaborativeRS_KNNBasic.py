import additionalFunctions as af
import sys
sys.path.append('../Recommender_Systems/')
import collaborative_rs as clbr_rs
import pandas as pd

# Тут меняем-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
max_size = 250000
test_size = 0.05
dataset_name = 'df2'
comb = 'comb4'
RS_type = 'KNNBasic_Item'    # KNNBasic_Item
repeat = True

ratings_path = '../Datasets/merged/' + comb + '/' + 'ratings_' + dataset_name + '.csv'
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
folderName = '../Datasets/experiments/collaborative_rs/' + RS_type
af.folderExists(folderName)
folderName += '/' + dataset_name + '_' + comb
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
    info_df = clbr_rs.createInfoDF()
    print('movies create')

ratings_df, initLen_Ratings, amount_users, amount_movies = clbr_rs.startRatings(pd.read_csv(ratings_path), max_size)
ratings_data, train_data, test_data = clbr_rs.startSurprise(ratings_df, test_size, train_file, test_file)

if af.fileExists(RS_model_filePath) and not repeat:
    loaded_model = af.pikcle_load(RS_model_filePath)
    predictions = loaded_model.test(test_data)

    print(f'mae = {round(clbr_rs.accuracy.mae(predictions), 4)}')
    print(f'rmse = {round(clbr_rs.accuracy.rmse(predictions), 4)}')

    # что с ней делать дальше?
else:
    start_time = af.timer()
    flag = False
    if RS_type == 'KNNBasic_User':
        flag = True
    best_k, best_sim_options = clbr_rs.gridSearch_KNNBasic(flag, ratings_data)

    model, fit_time, predictions, predict_time = clbr_rs.fit_test_KNNBasic(best_k, best_sim_options, train_data, test_data)
    af.pickle_dump(RS_model_filePath, model)    # сохранение модели
    all_time = af.timer() - start_time

    info_df.loc[len(info_df)] = [dataset_name, initLen_Ratings, max_size, test_size, RS_type,
                                 str(best_k) + ' ' + str(best_sim_options), round(clbr_rs.mae(predictions), 4),
                                 round(clbr_rs.rmse(predictions), 4), fit_time, predict_time, round(all_time, 4)]
    # "{:.4f}".format(number)
    print(info_df.tail(5))
    info_df.to_csv(filePath_results, index=False)

columns = ['userId', 'movieId', 'rating', 'pred', 'other']
df = pd.DataFrame(predictions, columns=columns)
df.to_csv(predictions_filePath, index=False)