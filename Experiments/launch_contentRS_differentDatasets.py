from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import additionalFunctions as af
import sys
sys.path.append('../Recommender_Systems/')
import content_rs as crs
import collaborative_rs as clbr_rs
from itertools import product
import pandas as pd
import numpy as np

dataset_names = ['df1', 'df2', 'df3', 'df4']
comb = 'comb4'

topN = 16
fraction_test = 0.05
max_size = 100000

folderName = '../Datasets/experiments/content_rs/differentDatasets/'
af.folderExists(folderName)
info_df_filePath = folderName + '/info_differentDatasets.csv'

if af.fileExists(info_df_filePath):
    info_df = pd.read_csv(info_df_filePath)
    print('df exist')
else:
    info_df = crs.createInfoDF()
    print('df create')

for dataset_name in dataset_names:
    merged_df = pd.read_csv('../Datasets/merged/' + comb + '/' + dataset_name + '_dataset.csv')
    lastMovieVertexId = len(merged_df)
    filePath_vertex = '../Datasets/visualization_vertex_edge/vertex/vertex_' + dataset_name + '_' + comb + '.csv'
    ratings_path = '../Datasets/merged/' + comb + '/' + 'ratings_' + dataset_name + '.csv'
    train_file = folderName + '/data/train_data_' + dataset_name + '.pkl'
    test_file = folderName + '/data/test_data_' + dataset_name + '.pkl'

    ratings_df, initLen_Ratings, amount_users, amount_movies = clbr_rs.startRatings(pd.read_csv(ratings_path), max_size)
    ratings_data, _, __ = clbr_rs.startSurprise(ratings_df, fraction_test, train_file, test_file)

    vertex_df = pd.read_csv(filePath_vertex)
    test_data = af.pikcle_load(test_file)
    train_data = af.pikcle_load(train_file)

    folder_emb = '../Datasets/emb_data/' + comb + '_' + dataset_name + '/'
    folder_emb_emb = folder_emb + 'emb'
    folder_model = folder_emb + 'model'


    all_combinations = [[64, 50, 30, 2]]
    for combination in all_combinations:
        strCombination = '_'.join([str(x) for x in combination])
        print(f'strCombination = {strCombination}')  # remove
        modelPath = folder_model + '/model_' + strCombination
        embPath = folder_emb_emb + '/emb_' + strCombination

        if crs.checkCombination(modelPath, embPath):
            print('if')
            model = Word2Vec.load(modelPath)
            embeddings = KeyedVectors.load_word2vec_format(embPath)

            start_time = af.timer()
            mem_before = af.mem()

            predictions, real_ratings, fraction_zero, mean_t_iter = crs.getAllEmbPredictions(model, embeddings,
                                                                                             test_data,
                                                                                             train_data, vertex_df,
                                                                                             topN,
                                                                                             lastMovieVertexId,
                                                                                             merged_df)


            af.folderExists(folderName + '/predictions')
            predict_filePath = folderName + '/predictions' + '/predict_' + strCombination + '.csv'
            crs.savePredictions(predictions, predict_filePath)

            real_ratings = np.array(real_ratings)
            predictions = np.array(predictions)

            rmse = crs.rmse_content(predictions, np.array(real_ratings))
            mae = crs.mae_content(predictions, real_ratings)

            info_df.loc[len(info_df)] = [dataset_name, lastMovieVertexId, strCombination, fraction_test, topN,
                                         round(fraction_zero, 4), str(mae), round(rmse, 4), str(mean_t_iter),
                                         round(af.timer() - start_time, 4), round(af.mem() - mem_before, 4)]

            print(info_df.tail(5))  # remove
            info_df.to_csv(info_df_filePath, index=False)

        else:
            continue
