import additionalFunctions as af
import sys
sys.path.append('../Recommender_Systems/')
import collaborative_rs_folds as clbr_rs
import pandas as pd

# Тут меняем-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
comb = 'comb4'
max_size = 100000
test_size = 0.05

removes = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000]
dfs = ['df1', 'df2', 'df3', 'df4']
RS_types = ['KNNBasic_User', 'KNNBasic_Item']

for dataset_name in dfs:
    for RS_type in RS_types:
        for remove in removes:
            ratings_path = '../Datasets/merged/' + comb + '/' + 'ratings_' + dataset_name + '.csv'
            # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
            folderName = '../Datasets/experiments/collaborative_rs/' + RS_type
            af.folderExists(folderName)
            folderName += '/' + dataset_name + '_' + comb
            af.folderExists(folderName)

            filePath_results = folderName + '/info_df.csv'
            predictions_filePath = folderName + '/predictions_df.csv'

            train_file = '../Datasets/experiments/content_rs/combsEmb/' + dataset_name + '_' + comb + '/data/' + dataset_name + '_' + str(remove) + '.base'
            test_file = '../Datasets/experiments/content_rs/combsEmb/' + dataset_name + '_' + comb + '/data/' + dataset_name + '_' + str(remove) + '.test'

            af.folderExists(folderName + '/models')
            RS_model_filePath = folderName + '/models/' + RS_type + str(remove) + '.pkl'

            if af.fileExists(filePath_results):
                info_df = pd.read_csv(filePath_results)
                print('movies exist')
            else:
                info_df = clbr_rs.createInfoDF()
                print('movies create')

            ratings_df, initLen_Ratings, amount_users, amount_movies = clbr_rs.startRatings(pd.read_csv(ratings_path), max_size)
            ratings_data, train_data, test_data = clbr_rs.startSurprise(ratings_df, test_size, train_file, test_file)

            start_time = af.timer()

            if RS_type == 'KNNBasic_User':
                title = 'KNNBasic_User_rem' + str(remove)
                best_sim_options = {
                    "name": 'cosine',
                    "user_based": True,
                }
            else:
                title = 'KNNBasic_Item_rem' + str(remove)
                best_sim_options = {
                    "name": 'cosine',
                    "user_based": False,
                }

            best_k = 20

            model, fit_time, predictions, predict_time = clbr_rs.fit_test_KNNBasic(best_k, best_sim_options, ratings_data)
            af.pickle_dump(RS_model_filePath, model)    # сохранение модели
            all_time = af.timer() - start_time

            info_df.loc[len(info_df)] = [dataset_name, initLen_Ratings, max_size, test_size, title,
                        str(best_k) + ' ' + str(best_sim_options), round(clbr_rs.mae(predictions), 4),
                        round(clbr_rs.rmse(predictions), 4), fit_time, predict_time, round(all_time, 4)]

            print(info_df.tail(5))
            info_df.to_csv(filePath_results, index=False)

            columns = ['userId', 'movieId', 'rating', 'pred', 'other']
            df = pd.DataFrame(predictions, columns=columns)
            df.to_csv(predictions_filePath, index=False)