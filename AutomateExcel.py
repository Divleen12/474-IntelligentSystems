import pandas as pd
from rdflib import Graph, Literal, URIRef, Namespace

ex = Namespace("http://example.org/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
schema = Namespace("http://schema.org/")
focu = Namespace("http://focu.io/schema#")

# Create RDF graph
g = Graph()

g.bind("ex", ex)
g.bind("rdf", rdf)
g.bind("rdfs", rdfs)
g.bind("foaf", foaf)
g.bind("schema", schema)
g.bind("focu", focu)

# Load the Excel file
df = pd.read_excel("StudentsData.xlsx", engine="openpyxl")

# Iterate over the rows
for index, row in df.iterrows():

    student_uri = ex[f"student_{index + 1}"]

    # Add triples
    g.add((student_uri, rdf.type, ex.Student))
    g.add((student_uri, foaf.givenName, Literal(row["First Name"])))
    g.add((student_uri, foaf.familyName, Literal(row["Last Name"])))
    g.add((student_uri, ex.studentID, Literal(row["ID Number"])))
    g.add((student_uri, foaf.mbox, URIRef(f"mailto:{row['Email']}")))

    course_uri = focu[row["Completed Course"]]
    g.add((student_uri, ex.completedCourse, course_uri))
    g.add((course_uri, rdf.type, focu.Course))
    g.add((course_uri, focu.courseName, Literal(row["Completed Course"])))

    g.add((student_uri, ex.grade, Literal(row["Grade"])))
    if row["Retake Grade"] != row["Grade"]:
        g.add((student_uri, ex.retakeGrade, Literal(row["Retake Grade"])))

# Serialize to Turtle format
turtle = g.serialize(format="turtle")
print(turtle)

with open('students.ttl', 'w', encoding='utf-8') as f:
    f.write(g.serialize(format="turtle"))

# Serialize to N-Triples format
with open('students.nt', 'w', encoding='utf-8') as f:
    f.write(g.serialize(format="nt"))
