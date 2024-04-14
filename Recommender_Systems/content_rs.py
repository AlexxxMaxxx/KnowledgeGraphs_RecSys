from sklearn.metrics.pairwise import cosine_similarity
import additionalFunctions as af
import pandas as pd
import numpy as np


def checkCombination(modelPath, embPath):
    return af.fileExists(modelPath) and af.fileExists(embPath)

def calcRating(sim_nodes, ratings_nodes):
    sim_nodes = np.array(sim_nodes)
    ratings_nodes = np.array(ratings_nodes)
    sim_sum = np.sum(sim_nodes)

    if sim_sum != 0:
        weighted_sum = np.sum(sim_nodes * ratings_nodes)
        return weighted_sum / sim_sum
    else:
        return 0


def isFoundRating(found_movieId, ratingsUser):
    return next((rating for movieId, rating in ratingsUser.items() if movieId == found_movieId), None)


def getMovieId(vertexId, vertex_df):
    row = vertex_df.loc[vertex_df['id'] == vertexId].iloc[0]
    splitStr = row['label'].split('_')
    return int(splitStr[-1])


def getEmbPredictions(model, vertex_df, ratingsUser, vertex_movieId, topN, lastMovieVertexId, koef):
    similar_nodes = model.wv.most_similar(vertex_movieId, topn=pow(topN, koef))

    counterMovies = 0
    sim_nodes = []
    ratings_nodes = []

    for sim_node in similar_nodes:
        if counterMovies < topN:  # еще не набрали
            vertex = int(sim_node[0])
            if vertex <= lastMovieVertexId:  # если фильм
                movieId = getMovieId(vertex, vertex_df)
                found_rating = isFoundRating(movieId, ratingsUser)
                if found_rating is not None:
                    sim_nodes.append(sim_node[1])
                    ratings_nodes.append(found_rating)
                    counterMovies += 1
        else:
            break

    if counterMovies < topN and koef == 3:
        rating = getEmbPredictions(model, vertex_df, ratingsUser, vertex_movieId, topN, lastMovieVertexId, 4)
    elif counterMovies >= topN:
        rating = calcRating(sim_nodes, ratings_nodes)
    else:
        rating = 0
    return rating


def getVertexId(movieId, vertex_df):
    filtered_row = vertex_df.loc[vertex_df['label'].str.endswith('_{}'.format(movieId))].iloc[0]
    return str(filtered_row['id'])


# пользователь оценивал не все фильмы, поэтому нужно знать, какие фильмы из best_similar имеют оценки
def getAllRatingsUser(userId, train_data):
    dict_from_tuples = {tup[1]: tup[2] for tup in train_data if tup[0] == userId}
    return dict_from_tuples


def calcSim(embeddings, vertex1, vertex2):
    embedding1 = np.array(embeddings[vertex1]).reshape(1, -1)  # преобразуем вектор в матрицу (1, N)
    embedding2 = np.array(embeddings[vertex2]).reshape(1, -1)

    cosine_sim = cosine_similarity(embedding1, embedding2)
    return cosine_sim[0][0]


# вычисляем рейтинг фильма row[1] на основе ранее оцененных пользователем row[0]
# фильмов и на основе их близости с нашим фильмом
def getAllEmbPredictions(model, embeddings, test_data, train_data, vertex_df, topN, lastMovieVertexId):
    predictions = []
    real_ratings = []
    timers = []
    counter_zero = 0

    for row in test_data:  # row[0] - userId, row[1] - movieId, row[2] - rating
        real_ratings.append(row[2])
        ratingsUser = getAllRatingsUser(row[0], train_data)
        start_time = af.timer()

        if len(ratingsUser) == 0:
            rating = 0
        else:
            vertex_movieId = getVertexId(row[1], vertex_df)    # эмбеддинги строятся по vertexId, а у нас movieId

            if len(ratingsUser) < topN:
                sim_nodes = [calcSim(embeddings, vertex_movieId, getVertexId(movieId, vertex_df)) for movieId, rating in
                             ratingsUser.items()]
                ratings_nodes = [rating for movieId, rating in ratingsUser.items()]
                rating = calcRating(sim_nodes, ratings_nodes)
            else:
                rating = getEmbPredictions(model, vertex_df, ratingsUser, vertex_movieId, topN, lastMovieVertexId, 3)
        timers.append(af.timer() - start_time)

        if rating == 0:
            counter_zero += 1

        predictions.append(rating)
    return predictions, real_ratings, \
           counter_zero / len(predictions) if counter_zero != 0 else 0, \
           np.mean(np.array(timers))


def rmse_content(predictions, real_ratings):
    return np.sqrt(np.mean((predictions - real_ratings) ** 2))


def mae_content(predictions, real_ratings):
    return np.mean(abs(predictions - real_ratings))

def createInfoDF():
    return pd.DataFrame(columns=['dataset_name', 'amount_movies', 'combination', 'fraction_test',
                                 'topN', 'fraction_zero', 'mae', 'rmse', 't_iter', 't_all', 'memory'])

def savePredictions(predictions, predict_filePath):
    with open(predict_filePath, 'w') as f:
        f.writelines(f"{pred}\n" for pred in predictions)

