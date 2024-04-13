import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON    # для удаленного выполнения запросов
import requests
import time
import csv
import re    # for split()


def splitTitle(title):
    result = list(filter(lambda x: x !='', re.split(r' \(|\)', title)))
    check_the = re.split(r', The', result[0])
    if len(check_the) > 1:
        if not check_the[1]:
            result[0] = check_the[0]
    if len(result) == 2:
        return result[0], '', result[1]
    elif len(result) == 3:
        return result[0], result[1], result[2]
    else:
        return result[0], '', ''


def getIMDB_wiki(title, year):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "type": "item",
        "search": title,
        "year": year
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверяем статус ответа
        data = response.json()

        if "search" in data and data["search"]:
            imdb_id = None
            # Поиск IMDB id среди полученных результатов
            for item in data["search"]:
                if "id" in item and "label" in item and item["label"] == title and "description" in item and str(
                        year) in item["description"]:
                    entity_id = item["id"]
                    # Получение свойств сущности для поиска IMDB id
                    entity_url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
                    entity_data = requests.get(entity_url).json()
                    if "P345" in entity_data["entities"][entity_id]["claims"]:
                        imdb_id = entity_data["entities"][entity_id]["claims"]["P345"][0]["mainsnak"]["datavalue"][
                            "value"]
                        break
            return imdb_id if imdb_id else ""
        else:
            return ""

    except requests.exceptions.HTTPError as err:
        if response.status_code == 429:  # Обработка ошибки 429 - слишком много запросов
            print("Too many requests. Waiting for 5 seconds...")
            time.sleep(5)  # Подождем 5 секунд и отправим запрос заново
        else:
            return f"Error: {err}"
    except Exception as e:
        return f"Error: {e}"

ml_movies = pd.read_csv('../../Datasets/movies.csv', sep=',')
print(ml_movies.tail(10))

movies_movielens_path = '../../Datasets/movies.csv'
headers_id_path = '../../Datasets/wikidata/headers_id.csv'
not_found_path = '../../Datasets/wikidata/not_found_id.csv'

limitRows = len(ml_movies)
start = 1

fieldnames = list(['movieId'])
addColumns = ['IMDbID', 'title', 'releaseYear']  # какие столбцы добавляем из ГЗ
fieldnames.extend(addColumns)

headers_id = open(headers_id_path, 'a', newline='')
not_found_id = open(not_found_path, 'a', newline='')

with open(movies_movielens_path, 'r', newline='') as movies_movielens:
    reader = csv.DictReader(movies_movielens)  # рез-т чтения в словаре
    writer = csv.DictWriter(headers_id, fieldnames=fieldnames)
    writer_not_found = csv.DictWriter(not_found_id, fieldnames=fieldnames)

    if start == 1:
        writer.writeheader()
        writer_not_found.writeheader()

    for count, row in enumerate(reader):
        if count < start - 1:
            continue
        elif count == limitRows:
            break
        else:
            title, originalTitle, releaseYear = splitTitle(row['title'])
            imdb_id = getIMDB_wiki(title, releaseYear)
            if (imdb_id == ''):
                imdb_id = getIMDB_wiki(originalTitle, releaseYear)
                if (imdb_id == ''):
                    writer_not_found.writerow({fieldnames[0]: row[fieldnames[0]],
                                               fieldnames[1]: imdb_id,
                                               fieldnames[2]: title,
                                               fieldnames[3]: releaseYear})
            writer.writerow({fieldnames[0]: row[fieldnames[0]],
                             fieldnames[1]: imdb_id,
                             fieldnames[2]: title,
                             fieldnames[3]: releaseYear})

movies_movielens.close()
headers_id.close()
not_found_id.close()