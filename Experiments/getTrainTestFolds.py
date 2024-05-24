import additionalFunctions as af
import sys
sys.path.append('../Recommender_Systems/')
import collaborative_rs_folds as clbr_rs_f
import pandas as pd

dfs = ['df1', 'df2', 'df3', 'df4']
comb = 'comb4'

folderName = '../Datasets/experiments/content_rs/combsEmb/'
af.folderExists(folderName)

fraction_test = 0.05
max_size = 100000

removes = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000]
#remove = 3000

for dataset_name in dfs:
    ratings_path = '../Datasets/merged/' + comb + '/' + 'ratings_' + dataset_name + '.csv'
    ratings_df, initLen_Ratings, amount_users, amount_movies = clbr_rs_f.startRatings(pd.read_csv(ratings_path),
                                                                                      max_size)

    test = ratings_df.sample(n=int(max_size * fraction_test))
    print(f'len test {len(test)}')

    base = ratings_df.drop(test.index)
    print(f'len base {len(base)}')

    for remove in removes:
        train_file = folderName + dataset_name + '_' + comb + '/data/' + dataset_name + '_' + str(remove) + '.base'
        test_file = folderName + dataset_name + '_' + comb + '/data/' + dataset_name + '_' + str(remove) + '.test'

        if remove == 250:
            rem = test.sample(n=remove)
            rem_indx = rem.index

        else:
            temp_test = test.drop(rem_indx)
            add_rem = temp_test.sample(n=250)
            rem = pd.concat([rem, add_rem], ignore_index=True)

        print(f'len rem {len(rem)}')


        rows_to_delete = []
        for index, row in base.iterrows():
            userId_value = row['userId']

            if userId_value in rem['userId'].values:
                rows_to_delete.append(index)

        filtered_base = base.drop(rows_to_delete)
        print(f'len filtered_base = {len(filtered_base)}')

        # сохранение обоих датасетов в отдельные файлы
        filtered_base.to_csv(train_file, index=False, header=False,)
        test.to_csv(test_file, index=False, header=False,)