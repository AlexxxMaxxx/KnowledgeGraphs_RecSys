from imdb import Cinemagoer, IMDbError
import pandas as pd
import time
import csv
import warnings
warnings.filterwarnings('ignore')

# переименование столбца IMDbId в tt_IMDbId
# добавление столбцов IMDbId и fullTitle в итоговый файл
def addColumns(headers_id_path):
    headers_id_df = pd.read_csv(headers_id_path)
    headers_id_df.rename(columns={'IMDbID': 'tt_IMDb_Id'}, inplace=True)
    headers_id_df['IMDb_Id'] = ''
    headers_id_df['fullTitle'] = ''
    headers_id_df = headers_id_df[['movieId', 'IMDb_Id', 'tt_IMDb_Id', 'title', 'fullTitle', 'releaseYear']]
    headers_id_df.to_csv(headers_id_path, index=False)

def getEmptyHeadersId(headers_id_path):
    headers_pd = pd.read_csv(headers_id_path)
    empty_cells_count = headers_pd['tt_IMDb_Id'].isnull().sum()
    return empty_cells_count

def getLengthHeadersId(headers_id_path):
    headers_pd = pd.read_csv(headers_id_path)
    return len(headers_pd)

def getLengthNotFound(not_found_path):
    not_found_pd = pd.read_csv(not_found_path)
    print(f'All row in not_found_pd: {len(not_found_pd)}')

# movieId from not_found_id
def getNotFound(not_found_path):
    with open(not_found_path, 'r') as not_found:
        reader_not_found = csv.DictReader(not_found)
        moviesId = []
        for count, row in enumerate(reader_not_found):
            moviesId.append(row['movieId']) # для какого фильма будем искать
    not_found.close()
    return moviesId

# IMDb = функция для получения ID по title* (fullTitle)
def getNotFound_IMDbId(fullTitle):
    try:
        ia = Cinemagoer()
        movies = ia.search_movie(fullTitle)
        if movies:
            return movies[0].movieID
        else:
            return ''
    except IMDbError as e:
        print(e)
        time.sleep(30)
        return ''

def writeToCell(file_path, movieId, value):
    df = pd.read_csv(file_path)
    df.loc[df['movieId'] == int(movieId), 'tt_IMDb_Id'] = value
    df.to_csv(file_path, index=False)


def writeToCell2(file_path, row_index, value, isFound):
    df = pd.read_csv(file_path)
    df['fullTitle'] = df['fullTitle'].astype(str)
    df.at[row_index, 'fullTitle'] = value

    if isFound:
        IMDb_Id = df.at[row_index, 'tt_IMDb_Id']
        df.at[row_index, 'IMDb_Id'] = str(IMDb_Id[2:])

    df.to_csv(file_path, index=False)

def dropStr_NotFound(not_found_path, movieId):
    not_found_pd = pd.read_csv(not_found_path)
    not_found_pd = not_found_pd[not_found_pd['movieId'] != int(movieId)]
    not_found_pd.reset_index(drop=True, inplace=True)
    not_found_pd.to_csv(not_found_path, index=False)


def getNotFound_tt_IMDbID(not_found_path, movielens_path, moviesId, amount_blocks):
    counter_bloks = 0

    with open(movielens_path, 'r') as movies_movielens:
        reader_movielens = csv.DictReader(movies_movielens)
        for count, row in enumerate(reader_movielens):
            if moviesId and counter_bloks != amount_blocks:
                if row['movieId'] == moviesId[0]:
                    IMDbId = getNotFound_IMDbId(row['title'])
                    if IMDbId != '':
                        writeToCell(headers_id_path, row['movieId'], 'tt' + IMDbId)
                        dropStr_NotFound(not_found_path, moviesId[0])
                        counter_bloks += 1
                    else:
                        time.sleep(15)
                    moviesId.pop(0)
                else:
                    continue
            else:
                break
    movies_movielens.close()

def pasteFullTitle_IMDbID(movielens_path, headers_id_path, length, moviesId):
    counter = 0
    with open(movielens_path, 'r') as movies_movielens:
        reader_movielens = csv.DictReader(movies_movielens)
        for count, row in enumerate(reader_movielens):
            if counter < length:
                if row['movieId'] not in moviesId:
                    writeToCell2(headers_id_path, count, row['title'], True)
                else:
                    writeToCell2(headers_id_path, count, row['title'], False)
                counter += 1
            else:
                break
    movies_movielens.close()


movielens_path = '../../Datasets/movies.csv'
ratings_path = '../../Datasets/ratings.csv'
headers_id_path = '../../Datasets/headers_id.csv'
not_found_path = '../../Datasets/not_found_id.csv'

amount_blocks = 360  # варьиативно
size_block = 10

addColumns(headers_id_path)  # вызываем 1 раз в начале
prev_emptyHeadersId = getEmptyHeadersId(headers_id_path)

moviesId = getNotFound(not_found_path)
for block_index in range(1, amount_blocks + 1):
    emptyHeadersId = getEmptyHeadersId(headers_id_path)
    if emptyHeadersId == 0:  # уже все нашли
        break
    elif emptyHeadersId < size_block:
        if emptyHeadersId != prev_emptyHeadersId:
            getNotFound_tt_IMDbID(not_found_path, movielens_path, moviesId, emptyHeadersId)
            prev_emptyHeadersId = emptyHeadersId
        else:  # не можем найти эти ID
            break
    else:  # emptyHeadersId > size_block
        getNotFound_tt_IMDbID(not_found_path, movielens_path, moviesId, size_block)
    time.sleep(20)

getLengthNotFound(not_found_path)

moviesId = getNotFound(not_found_path)  # вызываем 1 раз в конце
pasteFullTitle_IMDbID(movielens_path, headers_id_path, getLengthHeadersId(headers_id_path), moviesId)

getLengthNotFound(not_found_path)
