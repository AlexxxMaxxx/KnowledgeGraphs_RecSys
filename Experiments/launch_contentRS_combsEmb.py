from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import additionalFunctions as af
from itertools import product
import sys
sys.path.append('../Recommender_Systems/')
import content_rs as crs
import pandas as pd
import numpy as np


def start(dataset_name, comb, all_combinations, topN):
    folderName = '../Datasets/experiments/content_rs/combsEmb/'
    af.folderExists(folderName)
    subFolderName = dataset_name + '_' + comb
    af.folderExists(folderName + subFolderName)
    info_df_filePath = folderName + subFolderName + '/info.csv'

    if af.fileExists(info_df_filePath):
        info_df = pd.read_csv(info_df_filePath)
    else:
        info_df = crs.createInfoDF()


    filePath_vertex = '../Datasets/visualization_vertex_edge/vertex/vertex_' + dataset_name + '_' + comb + '.csv'
    train_data_path = folderName + dataset_name + '_' + comb + '/data/train_data_' + dataset_name + '.pkl'
    test_data_path = folderName + dataset_name + '_' + comb + '/data/test_data_' + dataset_name + '.pkl'

    vertex_df = pd.read_csv(filePath_vertex)
    test_data = af.pikcle_load(test_data_path)
    print(test_data)
    train_data = af.pikcle_load(train_data_path)

    folder_emb = '../Datasets/emb_data/' + comb + '_' + dataset_name + '/'
    folder_emb_emb = folder_emb + 'emb'
    folder_model = folder_emb + 'model'

    dimensions = [16, 32]
    walk_length = [10, 20, 40]
    num_walks = [10, 20, 40]
    window = [2, 5, 10]

    #all_combinations = list(product(dimensions, walk_length, num_walks, window))

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
            predict_filePath = folderName + subFolderName + '/predictions/predict_' + strCombination + '.csv'
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


dfs = ['df3']
#combs = ['comb1', 'comb2', 'comb3', 'comb4', 'comb5', 'comb6']
combs = ['comb1']

for comb in combs:
    print(f'comb = {comb}')
    for dataset_name in dfs:
        print(f'df = {dataset_name}')
        merged_df = pd.read_csv('../Datasets/merged/' + comb + '/' + dataset_name + '_dataset.csv')
        lastMovieVertexId = len(merged_df)
        topsN = [64, 128, 256]
        for topN in topsN:
            print(topN)
        #topN = 10
            fraction_test = 0.05
            all_combinations = [[64, 50, 30, 2]]
            start(dataset_name, comb, all_combinations, topN)