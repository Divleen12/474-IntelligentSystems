
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
def process_entities(filename, worksheet_uri, lecture_uri):
    with open(filename, "r") as file:
        for line in file:
            entity = eval(line.strip())
            topic_name, entity_type, wikidata_id, wikidata_url, _ = entity

            if not (re.match(r'^[^a-zA-Z0-9]+$', topic_name) or len(topic_name) < 4):
                topic_uri = ex[f"{re.sub(r'[^a-zA-Z0-9]', '', topic_name)}Topic"]
                graph.add((topic_uri, rdf.type, focu.Topic))
                graph.add((topic_uri, focu.topicName, Literal(topic_name)))
                graph.add((topic_uri, focu.linkedTo, URIRef(wikidata_url)))
                graph.add((topic_uri, focu.provenance, worksheet_uri))

    graph.add((lecture_uri, focu.lectureContent, worksheet_uri))

worksheets = {
    'worksheet01_LinkedEntities.txt': ('COMP474Worksheet01', 'COMP474Lecture02'),
    'worksheet02_LinkedEntities.txt': ('COMP474Worksheet02', 'COMP474Lecture03'),
    'worksheet03_LinkedEntities.txt': ('COMP474Worksheet03', 'COMP474Lecture04'),
    'worksheet04_LinkedEntities.txt': ('COMP474Worksheet04', 'COMP474Lecture05'),
    'worksheet05_LinkedEntities.txt': ('COMP474Worksheet05', 'COMP474Lecture06'),
    'worksheet06_LinkedEntities.txt': ('COMP474Worksheet06', 'COMP474Lecture07'),
}
directory = "COMP474/Worksheets"
for filename, (worksheet_id, lecture_id) in worksheets.items():
    worksheet_uri = ex[worksheet_id]
    lecture_uri = ex[lecture_id]
    file_path = f"{directory}/{filename}"
    process_entities(file_path, worksheet_uri, lecture_uri)
output_file = "TripleWorksheets.ttl"
graph.serialize(destination=output_file, format="turtle")
