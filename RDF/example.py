import rdflib
from rdflib.tools.rdf2dot import rdf2dot

# Пример использования функции
g = rdflib.Graph()
g.parse("example.ttl", format="turtle")

with open("example.dot", "w") as f:
    rdf2dot(g, stream=f)

# dot -Tpng example.dot -o example.png