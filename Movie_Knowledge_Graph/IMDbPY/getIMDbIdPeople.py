from imdb import Cinemagoer
import pandas as pd
import csv

def getTenPerson(data):
    counter = 0
    with open('IMDbIds.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        #writer.writerow(['Name', 'IMDbId'])
        for person in data['unique_person']:
            if counter < 10:
                if person:
                    person_id = ia.search_person(person)

                    counter += 1
                    if person_id:
                        writer.writerow([person, person_id[0].personID])
                    else:
                        writer.writerow([person, 'Not Found'])

    print("Информация о IMDbIds сохранена в файле 'IMDbIds.csv'")

ia = Cinemagoer()
data = pd.read_csv('../../Datasets/merged/comb4/df*_multi_attr/df*_all_people.csv')

amount_blocks = len(data)

for i in range (1, int((amount_blocks / 10) + 1) + 1):
    getTenPerson(data)
    data = data.iloc[10:]





