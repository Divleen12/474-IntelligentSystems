import requests
import json
import logging


from constants import FUSEKI_BASE_URL

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.plugins.sparql import prepareQuery

FOCU = Namespace("http://focu.io/schema#")

namespaces = (
    "PREFIX focu: <http://focu.io/schema#>"
    "PREFIX focudata: <http://focu.io/data#>"
    "PREFIX dbo: <http://dbpedia.org/ontology/>"
    "PREFIX dbp: <http://dbpedia.org/property/>"
    "PREFIX dce: <http://purl.org/dc/elements/1.1/>"
    "PREFIX vivo: <http://vivoweb.org/ontology/core#>"
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns>"
)

def make_query(query):
    try:
        rows = requests.post(FUSEKI_BASE_URL, data={'query': query})
        rows.raise_for_status()

        return rows
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def extract_bindings(query_result):
    results = query_result.get("results", None)
    if results is None:
        return None

    bindings = results.get("bindings", None)
    if bindings is None or not bindings:
        return None

    return bindings

def get_course_credits(course_name, course_number):
    """
    Query 6
    """

    # course = URIRef(FOCU + f"{'_'.join(course.split()).upper()}")
    # print(course)
    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>

            SELECT ?courseName ?courseCredits
            WHERE {{
            ?course a focu:Course ;
                    focu:courseNumber "{course_number}" ; 
                    focu:courseSubject "{course_name}" ;
                    focu:courseName ?courseName;
                    focu:courseCredits ?courseCredits .
            }}"""
    print(course_name, course_number)
    rows = make_query(q)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    bindings = bindings[0]
    course_name = bindings.get("courseName", None)
    course_cred = bindings.get("courseCredits", None)

    if course_name is None or course_cred is None:
        return None

    return course_name.get("value", None), course_cred.get("value", None)


def get_course_resources(course_name, course_number):
    """
    Query 7
    """

    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>

            SELECT ?materialType ?seeAlso
            WHERE {{
            ?course a focu:Course;
                    focu:courseNumber "{course_number}" ;
                    focu:courseSubject "{course_name}" . 
            ?lecture focu:lectureContent ?material .
            ?material focu:seeAlso ?seeAlso .
            BIND(IF(EXISTS {{ ?material a focu:Slides }}, "Slides", 
                    IF(EXISTS {{ ?material a focu:Readings }}, "Readings",
                    IF(EXISTS {{ ?material a focu:Worksheets }}, "Worksheets",
                    IF(EXISTS {{?material a focu:OtherMaterial }}, "OtherMaterial", "Unknown")))) AS ?materialType)
            }}"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        materialType = result.get("materialType", {}).get("value", None)
        seeAlso = result.get("seeAlso", {}).get("value", None)

        if materialType is not None and seeAlso is not None:
            resources.append((materialType, seeAlso))

    return resources


def get_university_topics(university, course_name):
    """
    Query the graph for courses in a university within a given suject
    """

    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            SELECT ?course ?courseName ?courseNumber
            WHERE {{
                ?university ex:universityName ?uniName .
                FILTER(UCASE(?uniName) = UCASE("{university}"))
                ?course a focu:Course ;
                    focu:courseName ?courseName ;
                    focu:courseNumber ?courseNumber ;
                    focu:courseSubject "{course_name}"  .
            }}"""
            
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        courseName = result.get("courseName", {}).get("value", None)
        courseNumber = result.get("courseNumber", {}).get("value", None)

        if courseName is not None and courseNumber is not None:
            resources.append((courseName, courseNumber))

    return resources


def get_university_courses(university):
    """
    Query the graph for courses in a university within a given suject
    """

    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>

            SELECT ?courseName ?courseNumber ?courseCredits ?courseDescription ?courseSubject
            WHERE {{
                ?university ex:universityName "{university}" .
                ?course a focu:Course ;
                        focu:courseName ?courseName ;
                        focu:courseNumber ?courseNumber ;
                        focu:courseCredits ?courseCredits ;
                        focu:courseDescription ?courseDescription ;
                        focu:courseSubject ?courseSubject .
            }}"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        print(result)
        courseSubject = result.get("courseSubject", {}).get("value", None)
        courseNumber = result.get("courseNumber", {}).get("value", None)
        courseName = result.get("courseName", {}).get("value", None)
        courseCredits = result.get("courseCredits", {}).get("value", None)
        courseDescription = result.get("courseDescription", {}).get("value", None)

        if courseSubject is not None and courseNumber is not None and courseName is not None and courseCredits is not None and courseDescription is not None:
            resources.append((courseName, courseNumber,courseSubject, courseCredits, courseDescription ))
    print(resources)
    return resources

def get_topic_course(topic):
    """
    Query the graph for courses in a university within a given suject
    """

    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX bif: <http://www.openlinksw.com/schema/sparql/extensions#>

            SELECT DISTINCT ?course ?courseSubject ?courseNumber ?courseName ?courseDescription
            WHERE {{
            ?course a focu:Course ;
                    focu:courseName ?courseName ;
                    focu:courseSubject ?courseSubject ;
                    focu:courseNumber ?courseNumber ;
                    focu:courseDescription ?courseDescription .
            FILTER CONTAINS(LCASE(?courseDescription), "{topic}")
            }}"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        courseSubject = result.get("courseSubject", {}).get("value", None)
        courseNumber = result.get("courseNumber", {}).get("value", None)
        courseName = result.get("courseName", {}).get("value", None)
        courseDescription = result.get("courseDescription", {}).get("value", None)

        if courseSubject is not None and courseNumber is not None and courseName is not None and courseDescription is not None:
            resources.append((courseName, courseNumber,courseSubject, courseDescription ))

    return resources


def get_topic_course_lecture(course_name, course_number, material, material_number):
    """
    Query the graph for topics covered in a particular course in a particular lecture.
    """

    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?lectureName ?contentLabel ?seeAlso
            WHERE {{
            ?lecture a focu:Lecture ;
                    focu:lectureNumber "{material_number}" ;
                    focu:lectureName ?lectureName .
            OPTIONAL {{
                ?lecture focu:lectureContent ?content .
                ?content rdfs:label ?contentLabel .
                OPTIONAL {{ ?content focu:seeAlso ?seeAlso . }}
            }}
            }}"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        lectureName = result.get("lectureName", {}).get("value", None)
        contentLabel = result.get("contentLabel", {}).get("value", None)

        if lectureName is not None and lectureName:
            resources.append((lectureName, contentLabel ))

    return resources


def content_lecture_course(lecture_number, course_name, course_number):
    """
    Query 8
    """

    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?lectureName ?contentType ?contentLabel ?seeAlso
            WHERE {{
            ?course a focu:Course ;
                    focu:courseSubject "{course_name}" ;
                    focu:courseNumber "{course_number}" . 
            ?lecture a focu:Lecture ;
                    focu:lectureNumber "{lecture_number}" ; 
                    focu:lectureName ?lectureName ;
                    focu:lectureContent ?content .
            ?content a ?contentType ;
                    rdfs:label ?contentLabel .
            OPTIONAL {{ ?content focu:seeAlso ?seeAlso . }}
            FILTER ( ?contentType IN (focu:Slides, focu:Worksheets, focu:Readings) )
            }}"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        lectureName = result.get("lectureName", {}).get("value", None)
        contentType = result.get("contentType", {}).get("value", None)
        contentLabel = result.get("contentLabel", {}).get("value", None)
        seeAlso = result.get("seeAlso", {}).get("value", None)

        if lectureName is not None and lectureName:
            resources.append((lectureName,contentType,contentLabel,seeAlso ))

    return resources


def material_topic(course_name, course_number):
    """
    Query 5
    """

    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?lectureName ?materialType ?materialLabel ?seeAlso
            WHERE {{
            ?course a focu:Course ;
                    focu:courseNumber "{course_number}" ;
                    focu:courseSubject "{course_name}" .
            ?lecture focu:lectureContent ?material ;
                    focu:lectureName ?lectureName .
            ?material a ?materialType ;
                        rdfs:label ?materialLabel .
            OPTIONAL {{ ?material focu:seeAlso ?seeAlso . }}
            FILTER ( ?materialType IN (focu:Slides, focu:Readings) )
            }}"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        lectureName = result.get("lectureName", {}).get("value", None)
        materialType = result.get("materialType", {}).get("value", None)
        materialLabel = result.get("materialLabel", {}).get("value", None)
        seeAlso = result.get("seeAlso", {}).get("value", None)

        if lectureName is not None and lectureName:
            resources.append((lectureName,materialLabel,materialType,seeAlso ))

    return resources


def students_course(course_name, course_number):
    """
    Query 12
    """

    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?studentName ?studentID
            WHERE {{
            ?student a ex:Student ;
                    foaf:familyName ?familyName ;
                    foaf:givenName ?givenName ;
                    ex:completedCourse focu:{course_name}_{course_number} ;  
                    ex:studentID ?studentID .
            BIND(CONCAT(?givenName, " ", ?familyName) AS ?studentName)
            }}
            ORDER BY ?familyName ?givenName"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        studentName = result.get("studentName", {}).get("value", None)
        studentID = result.get("studentID", {}).get("value", None)

        if studentName is not None and studentName and studentID is not None and studentID:
            resources.append((studentName,studentID))

    return resources


def get_topic_competency(course_name, course_number):
    """
        Query 10
    """
    
    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?studentName ?courseName
            WHERE {{
            ?student a ex:Student ;
                    foaf:givenName ?studentName ;
                    ex:completedCourse focu:{course_name}_{course_number} .
            focu:COMP_474 a focu:Course ;
                    focu:courseName ?courseName .
            }}"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        studentName = result.get("studentName", {}).get("value", None)
        courseName = result.get("courseName", {}).get("value", None)

        if studentName is not None and studentName and courseName is not None and courseName:
            resources.append((studentName,courseName))

    return resources


def get_grade_course(studentID, course_name, course_number):
    """
        Query 11
    """
    
    q = f"""
            PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?studentID ?courseName ?grade
            WHERE {{
            ?student a ex:Student ;
                    ex:studentID ?studentID ;
                    ?grade focu:COMP_474 .
            
            focu:{course_name}_{course_number} a focu:Course ;
                            focu:courseName ?courseName .
                FILTER (?studentID = {studentID})  	
                FILTER (?grade != ex:completedCourse)
            }}
            """
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        studentID = result.get("studentID", {}).get("value", None)
        courseName = result.get("courseName", {}).get("value", None)
        grade = result.get("grade", {}).get("value", None)

        if studentID is not None and studentID and courseName is not None and courseName and grade is not None and grade:
            resources.append((studentID,courseName, grade))

    return resources


def get_student_transcript(givenName, familyName):
    """
        Query 13
    """
    
    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?studentName ?courseName ?grade ?retakeGrade
            WHERE {{
            
            ?student a ex:Student ;
                    foaf:givenName  "{givenName}" ; 
                    foaf:familyName  "{familyName}" ; 
                    ex:completedCourse ?course ;
                    ex:grade ?grade .
            OPTIONAL {{ ?student ex:retakeGrade ?retakeGrade . }}
            ?course a focu:Course ;
                    focu:courseName ?courseName .
            BIND(CONCAT(?givenName, " ", ?familyName) AS ?studentName)
            }}
            ORDER BY ?courseName"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        studentName = result.get("studentName", {}).get("value", None)
        courseName = result.get("courseName", {}).get("value", None)
        grade = result.get("grade", {}).get("value", None)
        retakeGrade = result.get("retakeGrade", {}).get("value", None)

        if studentName is not None and studentName and courseName is not None and courseName and grade is not None and grade and retakeGrade is not None and retakeGrade:
            resources.append((studentName,courseName, grade, retakeGrade))

    return resources


def get_course_description_outline(course_name, course_number):
    """
        Query 1 - Assignment 2
    """
    
    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>


            SELECT ?courseName ?courseDescription
            WHERE {{
            ?course a focu:Course ;
                    focu:courseNumber "{course_number}" ; 
                    focu:courseSubject "{course_name}" ;  
                    focu:courseName ?courseName ;
                    focu:courseDescription ?courseDescription .
            }}
            """
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        courseName = result.get("courseName", {}).get("value", None)
        courseDescription = result.get("courseDescription", {}).get("value", None)
    

        if courseName is not None and courseName and courseDescription is not None and courseDescription:
            resources.append((courseName, courseDescription))

    return resources


def get_course_events(material_number, course_name, course_number):
    """
        Query 2 - Assignment 2
    """
    
    q = f"""PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>


            SELECT DISTINCT ?topicName ?resourceUri
            WHERE {{
            ?lecture a focu:Lecture ;
                    focu:lectureContent ?resource .
            ?topic focu:provenance ?resource ;
                    focu:topicName ?topicName .

            BIND (STR(?resource) AS ?resourceUri)
            FILTER (STR(?lecture) = "http://example.org/{course_name}{course_number}Lecture{material_number}")
            }}"""
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        topicName = result.get("topicName", {}).get("value", None)
        resourceUri = result.get("resourceUri", {}).get("value", None)

        if topicName is not None and topicName and resourceUri is not None and resourceUri:
            resources.append((topicName, resourceUri))

    return resources


def get_material_course(topic):
    """
        Query 3 - Assignment 2
    """
    
    q = f"""
            PREFIX ex: <http://example.org/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?courseEvent ?topicName (COUNT(?resource) AS ?frequency)
            WHERE {{
            ?topic a focu:Topic ;
                    focu:topicName "{topic}" .
            ?topic focu:provenance ?resource ;
                    focu:topicName ?topicName .
            ?courseEvent focu:lectureContent ?resource .

            BIND (STR(?courseEvent) AS ?eventUri)
            }}
            GROUP BY ?courseEvent ?topicName
            ORDER BY DESC(?frequency)

            """
    rows = make_query(q)
    print(rows)
    if rows is None:
        return None
    print(rows.json())
    bindings = extract_bindings(rows.json())
    if bindings is None:
        return None

    resources = []
    for result in bindings:
        topicName = result.get("topicName", {}).get("value", None)
        courseEvent = result.get("courseEvent", {}).get("value", None)
        frequency = result.get("frequency", {}).get("value", None)

        if topicName is not None and topicName and courseEvent is not None and courseEvent and frequency is not None and frequency:
            resources.append((topicName, courseEvent, frequency))

    return resources