import pandas as pd
from rdflib import Graph, Literal, URIRef, Namespace

ex = Namespace("http://example.org/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
schema = Namespace("http://schema.org/")
focu = Namespace("http://focu.io/schema#")

# Create check for better Grade
def letterToNumber(grade):
    if grade == "A":
        numberGrade = 5
    if grade == "B":
        numberGrade = 4
    if grade == "C":
        numberGrade = 3
    if grade == "D":
        numberGrade = 2
    if grade == "E":
        numberGrade = 1
    if grade == "F":
        numberGrade = 0
    return numberGrade

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

    course_name = row["Completed Course"].replace(' ', '_')
    course_uri = focu[course_name]
    g.add((student_uri, ex.completedCourse, course_uri))
    g.add((course_uri, rdf.type, focu.Course))
    g.add((course_uri, focu.courseName, Literal(row["Completed Course"])))

    userGrade = ex[Literal(row["Grade"])]
    userRetakeGrade = ex["Retake_" + Literal(row["Retake Grade"])]


    if letterToNumber(row["Retake Grade"]) > letterToNumber(row["Grade"]):
        g.add((student_uri, userGrade, course_uri))
        g.add((student_uri, userRetakeGrade, course_uri))
    else:
        g.add((student_uri, userGrade, course_uri))

# Turtle format
turtle_filename = "students.ttl"
with open(turtle_filename, 'w', encoding='utf-8') as turtle_file:
    turtle_file.write(g.serialize(format="turtle"))

# N-Triples format
nt_filename = "students.nt"
with open(nt_filename, 'w', encoding='utf-8') as nt_file:
    nt_file.write(g.serialize(format="nt"))
