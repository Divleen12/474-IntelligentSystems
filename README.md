# 474-IntelligentSystems
The overall goal of this project is to build Roboprof, an intelligent agent that can
answer university course- and student-related questions, using a knowledge graph and
natural language processing.

---
**Part I**

The first part of this project focuses on constructing the knowledge base.


# RDF Knowledge Base for COMP 474 and COMP 472 Courses

This repository contains the RDF Turtle (TTL) file representing the knowledge base for the COMP 474 "Intelligent Systems" and COMP 472 "Artificial Intelligence" courses at Concordia University. It includes detailed information about the courses, lectures, and additional resources.

## Structure

The knowledge base uses RDF with Turtle syntax. Including:

- Course details (name, number, credits, description)
- Lecture details (name, number, content)
- Slides and worksheets for each lecture
- Readings and other materials related to the lectures

## File
- BaseConstruction.ttl

# Concordia University RDF Knowledge Base

This file in the repository contains RDF data representing information about Concordia University. The data is serialized in both Turtle (TTL) and N-Triples (NT) formats.

## Structure

- University type
- University name
- Links to the university's DBpedia and Wikidata entries

## Files

- `concordia_university.ttl`: The RDF data in Turtle format.
- `concordia_university.nt`: The RDF data in N-Triples format.

# Student Information RDF Knowledge Base

This file contains RDF data representing student information for comp 474 course. The data is serialized in both Turtle (TTL) and N-Triples (NT) formats, created from an Excel sheet of student data using a Python script.

## Data Generation

The RDF data was generated using a Python script that:

1. Creates a sample Excel sheet with random student information.
2. Extracts data from the Excel sheet and converts it into RDF format.

## Structure

The RDF data includes the following information for each student:

- First and Last name
- ID Number
- Email Address
- Completed Course
- Grade
- Retake Grade 

## Files

- `StudentsData.xlsx`: The source Excel file with sample student data.
- `students.ttl`: The RDF data in Turtle format.
- `students.nt`: The RDF data in N-Triples format.

## Execution Steps

In order to generate the RDF data, you can follow the steps below:

### Step 1: Base Construction File

The BaseConstruction.ttl file contains the course information, start by placing it in your working directory.

### Step 2: Generate Concordia University Information

In order to create RDF data for Concordia University, execute automateConcordiaInfo.py. This will produce the RDF data in Turtle and N-Triples formats. 
### Step 3: Generate the Excel Sheet for Student Information

For a sample Excel sheet with student data, execute `makeExcelStudent.py`. It will create an Excel file with random student information.

### Step 4: Generate RDF Data for Student Information
 Convert the student data from the Excel sheet into RDF format by running the AutomateStudentInfo.py script which produces Turtle and N-Triples files.

