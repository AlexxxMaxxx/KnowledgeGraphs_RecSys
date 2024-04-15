from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import additionalFunctions as af
from itertools import product
import sys
sys.path.append('../Recommender_Systems/')
from content_rs import *
import pandas as pd
import numpy as np

# тут менять -.-.-.-.-.-.-.
dataset_name = '10694'
lastMovieVertexId = 10694 #?
topN = 10
fraction_test = 0.05
# -.-.-.-.-.-.-.-.-.-.-.-.-.

folderName = '../Datasets/experiments/content_rs/combsEmb/' + dataset_name
af.folderExists(folderName)

info_df_filePath = folderName + '/info.csv'

if af.fileExists(info_df_filePath):
    info_df = pd.read_csv(info_df_filePath)
else:
    info_df = createInfoDF()


filePath_vertex = '../Datasets/visualization_vertex_edge/vertex_' + dataset_name + '.csv'
train_data_path = '../Datasets/experiments/collaborative_rs/KNNBasic_User/' + dataset_name + '/train_data_' + dataset_name + '.pkl'
test_data_path = '../Datasets/experiments/collaborative_rs/KNNBasic_User/' + dataset_name + '/test_data_' + dataset_name + '.pkl'

vertex_df = pd.read_csv(filePath_vertex)
test_data = af.pikcle_load(test_data_path)
print(test_data)
train_data = af.pikcle_load(train_data_path)

folder_emb = '../Datasets/emb_data/' + dataset_name + '/'
folder_emb_emb = folder_emb + 'emb'
folder_model = folder_emb + 'model'

dimensions = [16, 32]
walk_length = [10, 20, 40]
num_walks = [10, 20, 40]
window = [2, 5, 10]

#all_combinations = list(product(dimensions, walk_length, num_walks, window))
all_combinations = [[8, 55, 35, 8], [16, 55, 35, 8], [32, 55, 35, 8], [64, 55, 35, 8], [128, 55, 35, 8]]
for combination in all_combinations:
    strCombination = '_'.join([str(x) for x in combination])
    print(f'strCombination = {strCombination}')  # remove
    modelPath = folder_model + '/model_' + strCombination
    embPath = folder_emb_emb + '/emb_' + strCombination

    # добавить проверку, если существует и есть запись в датафрейме, то пропускать
    if checkCombination(modelPath, embPath):
        print('if')
        model = Word2Vec.load(modelPath)
        embeddings = KeyedVectors.load_word2vec_format(embPath)

        start_time = af.timer()
        mem_before = af.mem()

        predictions, real_ratings, fraction_zero, mean_t_iter = getAllEmbPredictions(model, embeddings, test_data,
                                                                                         train_data, vertex_df, topN,
                                                                                         lastMovieVertexId)

        predict_filePath = folderName + '/predictions/predict_' + strCombination + '.csv'
        savePredictions(predictions, predict_filePath)

        real_ratings = np.array(real_ratings)
        predictions = np.array(predictions)

        rmse = rmse_content(predictions, np.array(real_ratings))
        mae = mae_content(predictions, real_ratings)

        info_df.loc[len(info_df)] = [dataset_name, lastMovieVertexId, strCombination, fraction_test, topN,
                                     round(fraction_zero, 4), str(mae), round(rmse, 4), str(mean_t_iter),
                                     round(af.timer() - start_time, 4), round(af.mem() - mem_before, 4)]

        print(info_df.tail(5))  # remove
        info_df.to_csv(info_df_filePath, index=False)

    else:
        continue
