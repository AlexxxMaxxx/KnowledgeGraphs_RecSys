import pandas as pd
import numpy as np

combined_list = []
dfs = ['director', 'producer', 'stars', 'writer']
for df in dfs:
    path = pd.read_csv('../../Datasets/merged/comb4/df*_multi_attr/df*_' + df + '.csv')
    person_df = pd.DataFrame(path)
    unique_person = person_df[df].unique()
    print(len(unique_person))

    if df == 'director':
        combined_list = unique_person
    else:
        set1 = set(combined_list)
        set2 = set(unique_person)
        combined_list = set1 | set2

IMDbId = np.array([''] * len(combined_list))
df = pd.DataFrame({
    'unique_person': list(combined_list),
    'IMDbId': IMDbId
})

df.to_csv('../../Datasets/merged/comb4/df*_multi_attr/df*_all_people.csv', index=False)