import re

from rdflib import Graph, Namespace, URIRef, Literal

# Define namespaces
ex = Namespace("http://example.org/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
focu = Namespace("http://focu.io/schema#")

graph = Graph()
graph.bind("ex", ex)
graph.bind("rdf", rdf)
graph.bind("rdfs", rdfs)
graph.bind("foaf", foaf)
graph.bind("focu", focu)


# extracted_entities = [
#     ('Joe', 'PERSON', 'Q600789', 'https://www.wikidata.org/wiki/Q600789', 0.3715),
#     ('Concordia University', 'ORG', 'Q326342', 'https://www.wikidata.org/wiki/Q326342', 0.8926),
#     ('Joe', 'PERSON', 'Q600789', 'https://www.wikidata.org/wiki/Q600789', 0.3715),
#     ('Jane', 'PERSON', 'Q3039162', 'https://www.wikidata.org/wiki/Q3039162', 0.3768),
#     ('McGill University', 'ORG', 'Q201492', 'https://www.wikidata.org/wiki/Q201492', 0.9164),
#     ('Joe', 'PERSON', 'Q600789', 'https://www.wikidata.org/wiki/Q600789', 0.3715),
#     ('Concordia', 'GPE', 'Q52578', 'https://www.wikidata.org/wiki/Q52578', 0.4877),
#     ('Montreal', 'GPE', 'Q340', 'https://www.wikidata.org/wiki/Q340', 0.7097),
#     ('McGill', 'ORG', 'Q201492', 'https://www.wikidata.org/wiki/Q201492', 0.6022),
#     ('Montreal', 'GPE', 'Q340', 'https://www.wikidata.org/wiki/Q340', 0.7097),
#     ('Joe', 'PERSON', 'Q600789', 'https://www.wikidata.org/wiki/Q600789', 0.3715),
#     ('Concordia', 'GPE', 'Q1913996', 'https://www.wikidata.org/wiki/Q1913996', 0.4099),
#     ('RDF', 'ORG', 'Q54872', 'https://www.wikidata.org/wiki/Q54872', 0.4584),
#     ('Concordia University', 'ORG', 'Q326342', 'https://www.wikidata.org/wiki/Q326342', 0.4333),
#     ('RDF', 'ORG', 'Q54872', 'https://www.wikidata.org/wiki/Q54872', 0.4584),
#     ('RDF', 'ORG', 'Q54872', 'https://www.wikidata.org/wiki/Q54872', 0.4584),
#     ('’s', 'GPE', 'Q3631750', 'https://www.wikidata.org/wiki/Q3631750', 0.3811),
#     ('Concordia', 'GPE', 'Q1913996', 'https://www.wikidata.org/wiki/Q1913996', 0.4914),
#     ('RDF', 'ORG', 'Q1367488', 'https://www.wikidata.org/wiki/Q1367488', 0.6672),
#     ('Concordia', 'GPE', 'Q1913996', 'https://www.wikidata.org/wiki/Q1913996', 0.4914),
#     ('Joe', 'PERSON', 'Q600789', 'https://www.wikidata.org/wiki/Q600789', 0.3761),
#     ('Jane', 'PERSON', 'Q3039162', 'https://www.wikidata.org/wiki/Q3039162', 0.3813),
#     ('Wikidata', 'PERSON', 'Q2013', 'https://www.wikidata.org/wiki/Q2013', 0.6927),
#     ('Facebook', 'GPE', 'Q355', 'https://www.wikidata.org/wiki/Q355', 0.7417),
#     ('LinkedIn', 'GPE', 'Q213660', 'https://www.wikidata.org/wiki/Q213660', 0.7039),
#     ('Concordia', 'GPE', 'Q1913996', 'https://www.wikidata.org/wiki/Q1913996', 0.4914),
#     ('Jane', 'PERSON', 'Q3039162', 'https://www.wikidata.org/wiki/Q3039162', 0.3813),
#     ('Joe', 'PERSON', 'Q600789', 'https://www.wikidata.org/wiki/Q600789', 0.3761),
#     ('Jane', 'PERSON', 'Q3039162', 'https://www.wikidata.org/wiki/Q3039162', 0.3813),
#     ('RDF', 'ORG', 'Q54872', 'https://www.wikidata.org/wiki/Q54872', 0.4584),
#     ('Joe', 'PERSON', 'Q1077266', 'https://www.wikidata.org/wiki/Q1077266', 0.3416),
#     ('RDF', 'ORG', 'Q54872', 'https://www.wikidata.org/wiki/Q54872', 0.4584)
#
# ]

extractedEntities = []
with open("COMP474/Worksheets/worksheet01_LinkedEntities.txt", "r") as file:
    for line in file:
        entity = eval(line.strip())
        extractedEntities.append(entity)

for entity in extractedEntities:
    topic_name, entity_type, wikidata_id, wikidata_url, confidence = entity

    if re.match(r'^[^a-zA-Z0-9]+$', topic_name) or len(topic_name) < 4:
        continue

    #topic instances
    topic_uri = ex[f"{re.sub(r'[^a-zA-Z0-9]', '', topic_name)}Topic"]
    graph.add((topic_uri, rdf.type, focu.Topic))
    graph.add((topic_uri, focu.topicName, Literal(topic_name)))
    graph.add((topic_uri, focu.linkedTo, URIRef(wikidata_url)))

    #link topic to lecture
    graph.add((topic_uri, focu.provenance, ex.COMP474Worksheet01))
graph.add((ex.COMP474Lecture02, rdf.type, focu.Lecture))
graph.add((ex.COMP474Lecture02, focu.lectureNumber, Literal("2")))
graph.add((ex.COMP474Lecture02, focu.lectureName, Literal("Introduction to Knowledge Graphs (RDF)")))
graph.add((ex.COMP474Lecture02, focu.lectureContent, ex.COMP474Slides02))
graph.add((ex.COMP474Lecture02, focu.lectureContent, ex.COMP474Worksheet01))
graph.add((ex.COMP474Lecture02, focu.seeAlso,
           URIRef("https://moodle.concordia.ca/moodle/pluginfile.php/6430001/mod_resource/content/7/slides02.pdf")))
graph.add((ex.COMP474Slides02, rdf.type, focu.Slides))
graph.add((ex.COMP474Slides02, rdfs.label, Literal("Slides 02: Introduction to Knowledge Graphs (RDF)")))
graph.add((ex.COMP474Slides02, focu.seeAlso,
           URIRef("file:///Users/kimiagoodarzi/Desktop/roboprof/COMP4746741/Lectures/slides02.pdf")))




graph.add((ex.COMP474Worksheet01, rdf.type, focu.Worksheets))
graph.add((ex.COMP474Worksheet01, rdfs.label, Literal("Worksheet 01")))
graph.add((ex.COMP474Worksheet01, focu.seeAlso,
           URIRef("file:///Users/kimiagoodarzi/Desktop/roboprof/COMP4746741/Worksheets/Worksheet01.pdf")))
with open("Worksheet01.ttl", "w") as f:
    f.write(graph.serialize(format="turtle"))