import sys
sys.path.append('../Recommender_Systems/')
import hybrid_rs_folds as hrs

import additionalFunctions as af
import pandas as pd
import pickle

removes = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000]
dfs = ['df1', 'df2', 'df3', 'df4']
comb = 'comb4'
combination = '64_50_30_2'
types = ['KNNBasic_Item', 'KNNBasic_User']

for df in dfs:
    for RS_type in types:
        for remove in removes:
            print(f'df = {df}, RS_type = {RS_type}')
            filePath_clbrRS = '../Datasets/experiments/collaborative_rs/' + RS_type + '/' + df + '_' + comb
            filePath_model = filePath_clbrRS + '/models/' + RS_type + str(remove) + '.pkl'

            # Загрузка сохраненной модели из файла
            with open(filePath_model, 'rb') as file:
                KNNBasic_User_model = pickle.load(file)

            test_data_path = '../Datasets/experiments/content_rs/combsEmb/' + df + '_' +\
                             comb + '/data/' + df + '_' + str(remove) + '.test'
            test_data = af.pikcle_load(test_data_path)

            predictions_RS = KNNBasic_User_model.test(test_data)

            # content RS
            filePath_predictions_CRS = '../Datasets/experiments/content_rs/combsEmb/' + \
                                        df + '_' + comb + '/predictions/predict_' + \
                                       combination + '_' + str(remove) + '.csv'
            predictions_CRS = pd.read_csv(filePath_predictions_CRS, header=None)
            column_names = ['est']  # замените на нужные названия столбцов
            predictions_CRS.columns = column_names
            predictions_CRS = predictions_CRS['est'].tolist()
            hrs.hybridPrediction(predictions_RS, predictions_CRS, RS_type)