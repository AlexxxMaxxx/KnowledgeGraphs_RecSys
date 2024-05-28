import additionalFunctions as af
import sys
sys.path.append('../Recommender_Systems/')
import collaborative_rs as clbr_rs
import pandas as pd

dataset_names = ['df1']
comb = 'comb4'

folderName = '../Datasets/experiments/content_rs/combsEmb/'
af.folderExists(folderName)

fraction_test = 0.05
max_size = 100000

for dataset_name in dataset_names:
    #lastMovieVertexId = len(pd.read_csv('../Datasets/merged/' + comb + '/' + dataset_name + '_dataset.csv'))
    #filePath_vertex = '../Datasets/visualization_vertex_edge/vertex/vertex_' + dataset_name + '_' + comb + '.csv'
    ratings_path = '../Datasets/merged/' + comb + '/' + 'ratings_' + dataset_name + '.csv'
    train_file = folderName + dataset_name + '_' + comb + '/data/train_data_' + dataset_name + '.pkl'
    test_file = folderName + dataset_name + '_' + comb + '/data/test_data_' + dataset_name + '.pkl'

    ratings_df, initLen_Ratings, amount_users, amount_movies = clbr_rs.startRatings(pd.read_csv(ratings_path), max_size)
    ratings_data, _, __ = clbr_rs.startSurprise(ratings_df, fraction_test, train_file, test_file)