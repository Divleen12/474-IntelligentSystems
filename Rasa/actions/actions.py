# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions


# # This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import query

from collections import defaultdict

class ActionDefaultFallback(Action):
    """Executes the fallback action."""

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Define example messages for each intent
        intent_examples_data = {
            "course_credits": ["How many credits is COMP 474 worth?"],
            "course_resources": ["What additional resources are there for COMP 474?"],
            "University": ["List all courses offered by Concordia University"],
            "university_topics": ["List all courses offered by Concordia University within COMP 474"],
            "topic": ["In which courses is intelligent systems discussed?"],
            "topic_course": ["Which topics are covered in COMP 474 during lecture 01?"],
            "material_topic": ["What slides are recommended for intelligent systems in COMP 474?"],
            "material_describe": ["Detail the content available for Lecture 1 in COMP 474"],
            "readings": ["What reading materials are recommended for studying Alan Turing in COMP 474?"],
            "topic_competency": ["What competencies does a student gain after completing COMP 474?"],
            "grade_course": ["What grades did Jane Doe achieve in COMP 474?"],
            "student_course": ["Which students have completed COMP 474?"],
            "student_transcript": ["Print a transcript for Jane Doe, listing all the course taken with their grades."],
            "course_description_outline": ["What is COMP 474 about?"],
            "topics_course_events": ["Which topics are covered in Lecture 01 of COMP 474?"],
            "material_course": ["Which course events cover Alan Turing?"]
        }

       
        excluded_intents = {"greet", "nlu_fallback", "mood_unhappy","deny","affirm","goodbye","bot_challenge","mood_great"}  # Add all intents to be excluded
        remaining_intents = [(intent['name'], intent['confidence']) for intent in tracker.latest_message['intent_ranking'] if intent['name'] not in excluded_intents]
        dispatcher.utter_message(text=f"{tracker.latest_message.get('text')}")
     
        sorted_intents = sorted(remaining_intents, key=lambda x: x[1], reverse=True)

       
        top_5_intents = sorted_intents[:1]

        
        intent_examples = defaultdict(list)
        for intent, _ in top_5_intents:
            print(intent)
            examples = intent_examples_data.get(intent)
            intent_examples[intent] = examples
        print(intent_examples)
        
        response = "Top 1 intents:\n"
        for intent, confidence in top_5_intents:
            print(intent)
            print(confidence)
            
            response += "Examples:\n"
            for example in intent_examples.get(intent):
                response += f"- {example}\n"
            response += "\n"
            
        print(response)

        # Send the response to the user
        dispatcher.utter_message(text=response)
        return []

class ActionCourseDescribe(Action):

    def name(self) -> Text:
        return "action_course_credits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']
        
        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []

        res = query.get_course_credits(course_name, course_number)
        if res is None or res[0] is None or res[1] is None:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find credits for {course_name} {course_number} ")
            return []

        coursename, course_cred = res
        dispatcher.utter_message(text=f"Here's are the credits for {course_name} {course_number} - {coursename}: {course_cred}\n")
        return []


class ActionAdditionalResources(Action):

    def name(self) -> Text:
        return "action_additional_resources"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']
        
        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []

        resources = query.get_course_resources(course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find resources for {course_name} {course_number}")
            return []

        response = f"Here are the resources I found for {course_name} {course_number}:\n"
        for entry in resources:
            materialType, seeAlso = entry
            response += f"{materialType}: {seeAlso}\n"

        dispatcher.utter_message(text=response)
        return []


class ActionUniversityCoursesInSubject(Action):

    def name(self) -> Text:
        return "action_university_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_name = tracker.slots['course_name']
        university = tracker.slots['university']
        
        if "university" not in university.lower():
            university = university+" university"
        
        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        resources = query.get_university_topics(university, course_name)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find courses for {course_name} at {university}")
            return []

        response = f"Here's what I found about {course_name} at {university}:\n"
        for entry in resources:
            courseName, courseNumber = entry
            response += f"{courseName}: {courseNumber}\n"

        dispatcher.utter_message(text=response)
        return []
    
    
class ActionCoursesInUniversity(Action):

    def name(self) -> Text:
        return "action_university_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        university = tracker.slots['university']
        
        
        resources = query.get_university_courses(university)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find courses at {university}")
            return []

        response = f"Here's are the courses at {university}:\n"
        for entry in resources:
            courseName, courseNumber, courseSubject, courseCredits, courseDescription = entry
            response += f"{courseName}: {courseSubject} {courseNumber}\n Credits: {courseCredits}\n Description: {courseDescription}\n"

        dispatcher.utter_message(text=response)
        return []
    
    
class ActionTopicInCourse(Action):

    def name(self) -> Text:
        return "action_topic_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        topic = tracker.slots['topic']
        
        if topic is None or not topic:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []

        resources = query.get_topic_course(topic)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find courses for {topic}")
            return []

        response = f"Here's what I found about this topic:\n"
        for entry in resources:
            courseName, courseNumber, courseSubject, courseDescription = entry
            response += f"{courseName}: {courseSubject} {courseNumber}\n Description: {courseDescription}\n"

        dispatcher.utter_message(text=response)
        return []
    
class ActionTopicInCourseInLectureNumber(Action):

    def name(self) -> Text:
        return "action_topic_course_lecture"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']
        material = tracker.slots['material']
        material_number = tracker.slots['material_number']
        
        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []

        if material_number is None or not material_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        resources = query.get_topic_course_lecture(course_name, course_number, material, material_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find topics for {course_name} {course_number}")
            return []

        response = f"Here are the topics I found about for {course_name} {course_number}, lecture {material_number}:\n"
        for entry in resources:
            lectureName = entry
            response += f"{course_name}: {course_number}\n Topic: {lectureName}\n"

        dispatcher.utter_message(text=response)
        return []
    
    
class ContentInLectureInCourse(Action):

    def name(self) -> Text:
        return "action_material_describe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']
        material_number = tracker.slots['material_number']
        
        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []

        if material_number is None or not material_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        resources = query.content_lecture_course(material_number, course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find content for {course_name} {course_number}")
            return []

        response = f"Here is the content I found about for {course_name} {course_number}, lecture {material_number}:\n"
        for entry in resources:
            lectureName, contentType, contentLabel, seeAlso = entry
            response += f"{lectureName} {contentLabel}: {contentType}\n"

        dispatcher.utter_message(text=response)
        return []
    
class MaterialTopicCourse(Action):

    def name(self) -> Text:
        return "action_material_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']
        material = tracker.slots['material']
        topic = tracker.slots['topic']
    
        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand")
            return []
        
        resources = query.material_topic(course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find material for {course_name} {course_number}")
            return []

        response = f"Here is the material I found for {course_name} {course_number}:\n"
        for entry in resources:
            lectureName, materialType, materialLabel, seeAlso = entry
            response += f"{lectureName} {materialLabel}: {materialType}\n Here is the link for this material: {seeAlso}\n"

        dispatcher.utter_message(text=response)
        return []
    
class StudentsCourse(Action):

    def name(self) -> Text:
        return "action_students_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']

        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
  
        resources = query.students_course(course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find the students for {course_name} {course_number}")
            return []

        response = f"Here are the students who have completed {course_name} {course_number}:\n"
        for entry in resources:
            studentName,studentID = entry
            response += f"{studentName}: {studentID}\n"

        dispatcher.utter_message(text=response)
        return []
    
    
class TopicCompetency(Action):

    def name(self) -> Text:
        return "action_topic_competency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']

        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
  
        resources = query.get_topic_competency(course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find the students for {course_name} {course_number}")
            return []

        response = f"Here are the student names and the competencies gained by the students who have completed {course_name} {course_number}:\n"
        for entry in resources:
            studentName,courseName = entry
            response += f"{studentName}: {courseName}\n"

        dispatcher.utter_message(text=response)
        return []
    
    
    
class StudentGrade(Action):

    def name(self) -> Text:
        return "action_grade_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']
        givenName = tracker.slots['givenName']
        studentID = tracker.slots['studentID']

        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if studentID is None or not studentID:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
  
        resources = query.get_grade_course(studentID, course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find the grade for this student.")
            return []

        response = f"Here is the grade for the requested student {course_name} {course_number}:\n"
        for entry in resources:
            studentID,courseName, grade= entry
            response += f"Student ID:{studentID}\n Course: {courseName}, Grade: {grade}\n"

        dispatcher.utter_message(text=response)
        return []
    

class StudentTranscript(Action):

    def name(self) -> Text:
        return "action_student_transcript"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']
        givenName = tracker.slots['givenName']
        familyName = tracker.slots['familyName']

        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if givenName is None or not givenName:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if familyName is None or not familyName:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
  
        resources = query.get_student_transcript(givenName, familyName, course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find the grade for this student.")
            return []

        response = f"Here is the transcript for the requested student:\n"
        for entry in resources:
            studentName,courseName, grade, retakeGrade = entry
            response += f"{studentName}\n Course: {courseName}, Grade: {grade}, Retake Grade: {retakeGrade}\n"

        dispatcher.utter_message(text=response)
        return []
    
class CourseDescription(Action):

    def name(self) -> Text:
        return "action_course_description_outline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']

        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
  
        resources = query.get_course_description_outline(course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find the description for this course.")
            return []

        response = f"Here is the course description for {course_name} {course_number}:\n"
        for entry in resources:
            courseName, courseDescription = entry
            response += f"Course Name: {courseName}, Description: {courseDescription}\n"

        dispatcher.utter_message(text=response)
        return []
    
    
class CourseEvents(Action):

    def name(self) -> Text:
        return "action_course_events"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_name = tracker.slots['course_name']
        course_number = tracker.slots['course_number']
        material_number = tracker.slots['material_number']

        if course_name is None or not course_name:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if course_number is None or not course_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
        
        if material_number is None or not material_number:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
  
  
        resources = query.get_course_events(material_number, course_name, course_number)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find the events for this course.")
            return []

        response = f"Here are the topics for this course event:\n"
        for entry in resources:
            topicName, resourceUri = entry
            response += f"Topic Name: {topicName}, Resource URI: {resourceUri}\n"

        dispatcher.utter_message(text=response)
        return []
    
class MaterialCourse(Action):

    def name(self) -> Text:
        return "action_material_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        topic = tracker.slots['topic']
       
        if topic is None or not topic:
            dispatcher.utter_message(text=f"Sorry, I'm not sure I understand.")
            return []
  
  
        resources = query.get_material_course(topic)
        if resources is None or not resources:
            dispatcher.utter_message(text=f"Sorry, I can't seem to find the events for this course.")
            return []

        response = f"Here are the course events that cover this topic:\n"
        for entry in resources:
            topic, course, lecture, resource = entry
            response += f"Topic Name: {topic}, Course: {course}, Lecture: {lecture}, Resource: {resource}\n"

        dispatcher.utter_message(text=response)
        return []