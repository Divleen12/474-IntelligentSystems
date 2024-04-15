import csv
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD

ex = Namespace("http://example.org/")
focu = Namespace("http://focu.io/schema#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

graph = Graph()
graph.bind("ex", ex)
graph.bind("focu", focu)
graph.bind("rdf", rdf)
graph.bind("rdfs", rdfs)
graph.bind("xsd", xsd)

with open('CU_SR_OPEN_DATA_CATALOG (4).csv', 'r', encoding='iso-8859-1') as file:
    data = file.read().replace('\0', '')
    reader = csv.reader(data.splitlines(), delimiter=',')
    next(reader)

    for row in reader:
        if len(row) > 10:
            row[7] = ', '.join(row[7:-3])
            row = row[:10]

        try:
            course_id, subject, catalog, long_title, class_units, component_code, component_descr, prereq_description, career, equivalent_courses = row
        except ValueError as e:
            print("Error:", e, "in row:", row)
            continue

        course_uri = URIRef(ex[course_id.strip()])
        graph.add((course_uri, focu.courseId, Literal(course_id.strip())))
        graph.add((course_uri, focu.subject, Literal(subject.strip())))
        graph.add((course_uri, focu.catalogNumber, Literal(catalog.strip())))
        graph.add((course_uri, focu.courseName, Literal(long_title.strip())))
        graph.add((course_uri, focu.classUnits, Literal(class_units.strip())))
        graph.add((course_uri, focu.componentCode, Literal(component_code.strip())))
        graph.add((course_uri, focu.componentDescription, Literal(component_descr.strip())))
        graph.add((course_uri, focu.prerequisiteDescription, Literal(prereq_description.strip())))
        graph.add((course_uri, focu.career, Literal(career.strip())))
        if equivalent_courses.strip():
            graph.add((course_uri, focu.equivalentCourses, Literal(equivalent_courses.strip())))


with open('OpenSourceCourses.ttl', 'w') as file:
    file.write(graph.serialize(format='turtle'))
