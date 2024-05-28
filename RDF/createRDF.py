from rdflib import Namespace, Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, DC, FOAF
import pandas as pd

g = Graph()

imdb_preds = Namespace("https://github.com/AlexxxMaxxx/KnowledgeGraphs_RecSys/blob/master/RDF/dict_imdb_predicates.ttl/")
imdb_movie = Namespace("https://m.imdb.com/title/")
imdb_person = Namespace("https://m.imdb.com/name/")
wd = Namespace("http://www.wikidata.org/wiki/")
ex = Namespace("http://example.org/")

# class COUNTRY
class_country = wd['Q6256']
country_literal = Literal("Country", lang="en")
g.add((class_country, DC.title, country_literal))
g.add((class_country, RDF.type, RDFS.Class))

# subclass COUNTRIEs
filePath_country = '../DB/datasets/countries.csv'
country_df = pd.read_csv(filePath_country)
for index, row in country_df.iterrows():
     subclass = wd[row['countryId']]
     literal = Literal(row['title'], lang="en")
     g.add((subclass, DC.title, literal))
     g.add((subclass, RDFS.subClassOf, class_country))

# class PROFESSION
class_prof = wd['Q28640']
prof_literal = Literal("Profession", lang="en")
g.add((class_prof, DC.title, prof_literal))
g.add((class_prof, RDF.type, RDFS.Class))

# subclass PROFESSIONs
filePath_prof = '../DB/datasets/profession.csv'
prof_df = pd.read_csv(filePath_prof)
for index, row in prof_df.iterrows():
     subclass = wd[row['professionId']]
     literal = Literal(row['title'], lang="en")
     g.add((subclass, DC.title, literal))
     g.add((subclass, RDFS.subClassOf, class_prof))

# class GENRE
class_genre = wd['Q483394']
genre_literal = Literal("Genre", lang="en")
g.add((class_genre, DC.title, genre_literal))
g.add((class_genre, RDF.type, RDFS.Class))

# subclass GENREs
filePath_genre = '../DB/datasets/genres.csv'
genre_df = pd.read_csv(filePath_genre)
for index, row in genre_df.iterrows():
    subclass = wd[row['genreId']]
    literal = Literal(row['title'], lang="en")
    g.add((subclass, DC.title, literal))
    g.add((subclass, RDFS.subClassOf, class_genre))

# class FILM
class_film = wd['Q11424']
movie_literal = Literal("Movie", lang="en")
g.add((class_film, DC.title, movie_literal))
g.add((class_film, RDF.type, RDFS.Class))

# subclass movies
filePath_movies = '../DB/datasets/movies.csv'
movies_df = pd.read_csv(filePath_movies)
for index, row in movies_df.iterrows():
    IMDb_Id = row['IMDb_Id']
    if len(IMDb_Id) < 9:
        IMDb_Id = "0" * (9 - len(IMDb_Id)) + IMDb_Id
    movie = imdb_movie[IMDb_Id]
    g.add((movie, RDFS.subClassOf, class_film))
    g.add((movie, DC.title, Literal(row['title'], lang="en")))
    g.add((movie, DC.date, Literal(row['releaseYear'], datatype=XSD.date)))
    g.add((movie, imdb_preds.rating, Literal(row['rating'], datatype=XSD.float)))
    g.add((movie, imdb_preds.votes, Literal(row['votes'], datatype=XSD.integer)))
    g.add((movie, imdb_preds.runtimes, Literal(row['runtimes'], datatype=XSD.integer)))
    g.add((movie, imdb_preds.plot, Literal(row['plot'], lang="en")))

# add predicates movie wasReleased country
filePath_movieCountry = '../DB/datasets/movieCountry.csv'
movieCountry_df = pd.read_csv(filePath_movieCountry)
for index, row in movieCountry_df.iterrows():
    g.add((imdb_movie[row['IMDb_Id']], imdb_preds.wasReleased, wd[row['countryId']]))

# add predicates movie hasGenre Genre
filePath_movieGenre = '../DB/datasets/movieGenre.csv'
movieGenre_df = pd.read_csv(filePath_movieGenre)
for index, row in movieGenre_df.iterrows():
    g.add((imdb_movie[row['IMDb_Id']], imdb_preds.hasGenre, wd[row['genreId']]))

#add people
filePath_people = '../DB/datasets/persons.csv'
people_df = pd.read_csv(filePath_people)
for index, row in people_df.iterrows():
    g.add((imdb_person[row['personId']], FOAF.name, Literal(row['name'], lang="en")))

# add moviePersonProfession
filePath_mpp = '../DB/datasets/moviePersonProfession.csv'
mpp_df = pd.read_csv(filePath_mpp)
for index, row in mpp_df.iterrows():
    movie = imdb_movie[row['IMDb_Id']]
    person = imdb_person[row['personId']]
    prof = row['personId']
    if prof == 'Q3282637':
        predicate1 = imdb_preds.hasProducer
        predicate2 = imdb_preds.isProducer
    elif prof == 'Q2526255':
        predicate1 = imdb_preds.hasDirector
        predicate2 = imdb_preds.isDirector
    elif prof == 'Q36180':
        predicate1 = imdb_preds.hasWriter
        predicate2 = imdb_preds.isWriter
    else:
        predicate1 = imdb_preds.hasActor
        predicate2 = imdb_preds.isActor

    g.add((movie, predicate1, person))
    g.add((person, predicate2, movie))
    if (person, RDF.type, wd[prof]) not in g:
        g.add((person, RDF.type, wd[prof]))

# Вывод RDF графа
print(g.serialize(format="turtle"))
g.serialize(destination='knowledgeGraphMovies.rdf', format='turtle')

#film_uri = imdb_movie['tt00114709']