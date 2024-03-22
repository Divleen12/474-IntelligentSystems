import rdflib
# knowledge base for Concordia University


g = rdflib.Graph()

ex = rdflib.Namespace('https://example.org/')
rdf = rdflib.namespace.RDF

g.bind('ex', ex)

concordiaURI = ex.ConcordiaUniversity

g.add((concordiaURI, rdf.type, ex.University))
g.add((concordiaURI, ex.universityName, rdflib.Literal('Concordia University')))
g.add((concordiaURI, ex.dbpediaLink, rdflib.URIRef('https://dbpedia.org/page/Concordia_University')))
g.add((concordiaURI, ex.wikidataLink, rdflib.URIRef('https://www.wikidata.org/wiki/Q326342')))

# Turtle file
g.serialize(destination='concordia_university.ttl', format='turtle')

# N-Triples file
g.serialize(destination='concordia_university.nt', format='nt')
