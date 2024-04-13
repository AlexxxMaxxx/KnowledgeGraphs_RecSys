from imdb import Cinemagoer, IMDbError
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import time

def getRuntimes(movie):
    try:
        ret = movie['runtimes'][0]
    except IMDbError:
        time.sleep(2)
        ret = ''
    return ret

def getPlot(movie):
    first_plot = ''
    try:
        for plot in movie['plot']:
            first_plot = plot
            break
    except IMDbError:
        time.sleep(2)
        first_plot = ''
    return first_plot

def getNumb(movie, key):
    try:
        ret = movie[key]
    except IMDbError:
        time.sleep(2)
        ret = ''
    return ret

def getStr(movie, key):
    new_str = ''
    try:
        for name in movie[key]:
            new_str += str(name) + '|'
        new_str = new_str[:-1] # delete last '|'
    except IMDbError:
        time.sleep(2)
        new_str = ''
    return new_str

def getPerson(movie, key):
    persons = ''
    try:
        for person in movie[key]:
            persons += person['name'] + '|'
        persons = persons[:-1]
    except IMDbError:
        time.sleep(2)
        persons = ''
    return persons

# свойства, которые хотим получать и сохранить в датасет
file_path = '../../Datasets/more_info/keys_dict.csv'
keys_dict = dict([('cast', 'Person'), ('director', 'Person'), ('producer', 'Person'),
                  ('writer', 'str'), ('stars', 'str'), ('countries', 'str'),
                  ('rating', 'numb'), ('votes', 'numb'), ('top 250 rank', 'numb'),
                  ('plot', 'plot'), ('runtimes', 'runtimes')])

key_df = pd.read_csv(file_path)
ia = Cinemagoer()

set_index = 59196
end_index = 63000

start_time = time.time()
for index, IDmovie in enumerate(key_df['IMDb_Id']):
    try:
        print(index)
        if index < set_index:
            continue
        elif index >= set_index and index <= end_index:
            movie = ia.get_movie(IDmovie)

            for key, type in keys_dict.items():
                if pd.isnull(key_df.loc[index, key]):
                    add_value = ''
                    if key in movie:  # у фильма есть такой ключ
                        if type == 'Person':
                            add_value = getPerson(movie, key)
                        elif type == 'str':
                            add_value = getStr(movie, key)
                        elif type == 'numb':
                            add_value = getNumb(movie, key)
                        elif type == 'plot':
                            add_value = getPlot(movie)
                        elif type == 'runtimes':
                            add_value = getRuntimes(movie)

                    else:
                        add_value = ''
                    key_df.at[index, key] = add_value
                    key_df.to_csv(file_path, index=False)
        elif index > end_index:
            break

    except IMDbError as e:
        print(e)

end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения кода: {execution_time} секунд")
print(f"Количество строк: {end_index - set_index}")