from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import additionalFunctions as af
from itertools import product
import sys
sys.path.append('../Recommender_Systems/')
import content_rs as crs
import pandas as pd
import numpy as np


def start(dataset_name, comb, all_combinations, topN, remove):
    folderName = '../Datasets/experiments/content_rs/combsEmb/'
    af.folderExists(folderName)
    subFolderName = dataset_name + '_' + comb
    af.folderExists(folderName + subFolderName)
    info_df_filePath = folderName + subFolderName + '/info_rem_' + dataset_name + '.csv'

    if af.fileExists(info_df_filePath):
        info_df = pd.read_csv(info_df_filePath)
    else:
        info_df = crs.createInfoDF()


    filePath_vertex = '../Datasets/visualization_vertex_edge/vertex/vertex_' + dataset_name + '_' + comb + '.csv'
    vertex_df = pd.read_csv(filePath_vertex)

    train_file = '../Datasets/experiments/content_rs/combsEmb/' + dataset_name + '_' + comb + '/data/' + dataset_name + '_' + str(
        remove) + '.base'
    train_data = pd.read_csv(train_file)
    train_data = [(row[1], row[2], row[3]) for row in train_data.itertuples()]

    test_file = '../Datasets/experiments/content_rs/combsEmb/' + dataset_name + '_' + comb + '/data/' + dataset_name + '_' + str(
        remove) + '.test'
    test_data = pd.read_csv(test_file)
    test_data = [(row[1], row[2], row[3]) for row in test_data.itertuples()]

    folder_emb = '../Datasets/emb_data/' + comb + '_' + dataset_name + '/'
    folder_emb_emb = folder_emb + 'emb'
    folder_model = folder_emb + 'model'

    for combination in all_combinations:
        strCombination = '_'.join([str(x) for x in combination])
        print(f'strCombination = {strCombination}')  # remove
        modelPath = folder_model + '/model_' + strCombination
        embPath = folder_emb_emb + '/emb_' + strCombination

    # добавить проверку, если существует и есть запись в датафрейме, то пропускать
        if crs.checkCombination(modelPath, embPath):
            print('if')
            model = Word2Vec.load(modelPath)
            embeddings = KeyedVectors.load_word2vec_format(embPath)

            start_time = af.timer()
            mem_before = af.mem()

            predictions, real_ratings, fraction_zero, mean_t_iter = crs.getAllEmbPredictions(model, embeddings, test_data,
                                                                                         train_data, vertex_df, topN,
                                                                                         lastMovieVertexId, merged_df)

            af.folderExists(folderName + subFolderName + '/predictions')
            predict_filePath = folderName + subFolderName + '/predictions/predict_' + strCombination + '_' + str(r) + '.csv'
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

removes = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000]
dfs = ['df3', 'df4']
comb = 'comb4'

for dataset_name in dfs:
    for r in removes:
        print(f'df = {dataset_name}')
        merged_df = pd.read_csv('../Datasets/merged/' + comb + '/' + dataset_name + '_dataset.csv')
        lastMovieVertexId = len(merged_df)
        topN = 16
        fraction_test = 0.05
        all_combinations = [[64, 50, 30, 2]]
        start(dataset_name, comb, all_combinations, topN, r)