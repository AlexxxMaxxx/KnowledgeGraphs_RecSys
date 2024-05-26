import pandas as pd

filePath_countryId = '../DB/countries.csv'
countryId_df = pd.read_csv(filePath_countryId)

filePath_countries = '../Datasets/merged/comb4/df*_multi_attr/df*_countries.csv'
countries_df = pd.read_csv(filePath_countries)

for index, row in countries_df.iterrows():
    countryId = countryId_df.loc[countryId_df['title'] == row['countries'], 'countryId'].values
    if len(countryId) > 0:
        countries_df.at[index, 'countries'] = countryId[0]

countries_df = countries_df.rename(columns={'countries': 'countryId'})
countries_df.to_csv('./movieCountry.csv', index=False)
