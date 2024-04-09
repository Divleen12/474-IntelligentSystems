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


def process_entities(filename, content_uri, lecture_uri, content_type):
    with open(filename, "r") as file:
        for line in file:
            entity = eval(line.strip())
            topic_name, entity_type, wikidata_id, wikidata_url, _ = entity

            if not (re.match(r'^[^a-zA-Z0-9]+$', topic_name) or len(topic_name) < 4):
                topic_uri = ex[f"{content_type}_{re.sub(r'[^a-zA-Z0-9]', '', topic_name)}Topic"]
                graph.add((topic_uri, rdf.type, focu.Topic))
                graph.add((topic_uri, focu.topicName, Literal(topic_name)))
                graph.add((topic_uri, focu.linkedTo, URIRef(wikidata_url)))
                graph.add((topic_uri, focu.provenance, content_uri))

    graph.add((lecture_uri, focu.lectureContent, content_uri))


#worksheets 474
worksheets_directory = "COMP474/Worksheets"
worksheets = {
    'worksheet01_LinkedEntities.txt': ('COMP474Worksheet01', 'COMP474Lecture02'),
    'worksheet02_LinkedEntities.txt': ('COMP474Worksheet02', 'COMP474Lecture03'),
    'worksheet03_LinkedEntities.txt': ('COMP474Worksheet03', 'COMP474Lecture04'),
    'worksheet04_LinkedEntities.txt': ('COMP474Worksheet04', 'COMP474Lecture05'),
    'worksheet05_LinkedEntities.txt': ('COMP474Worksheet05', 'COMP474Lecture06'),
    'worksheet06_LinkedEntities.txt': ('COMP474Worksheet06', 'COMP474Lecture07'),
}

for filename, (content_id, lecture_id) in worksheets.items():
    content_uri = ex[content_id]
    lecture_uri = ex[lecture_id]
    file_path = f"{worksheets_directory}/{filename}"
    process_entities(file_path, content_uri, lecture_uri, "Worksheet")

#slides 474
slides_directory = "COMP474/Slides"
slides = {
    'Slide_01_LinkedEntities.txt': ('COMP474Slides01', 'COMP474Lecture01'),
    'Slide_02_LinkedEntities.txt': ('COMP474Slides02', 'COMP474Lecture02'),
    'Slide_03_LinkedEntities.txt': ('COMP474Slides03', 'COMP474Lecture03'),
    'Slide_04_LinkedEntities.txt': ('COMP474Slides04', 'COMP474Lecture04'),
    'Slide_05_LinkedEntities.txt': ('COMP474Slides05', 'COMP474Lecture05'),
    'Slide_06_LinkedEntities.txt': ('COMP474Slides06', 'COMP474Lecture06'),
    'Slide_07_LinkedEntities.txt': ('COMP474Slides07', 'COMP474Lecture07'),
}

for filename, (content_id, lecture_id) in slides.items():
    content_uri = ex[content_id]
    lecture_uri = ex[lecture_id]
    file_path = f"{slides_directory}/{filename}"
    process_entities(file_path, content_uri, lecture_uri, "Slide")

output_file = "TripleContent.ttl"
graph.serialize(destination=output_file, format="turtle")
