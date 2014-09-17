# Assignment 1 - Managing Students!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
#
#
#
# ---------------------------------------------
"""The back-end data model for the program.

TODO: fill in this doctring with information about your
class(es)!
"""

class Student:
    '''Represent students with names and the courses they are taking.'''
    def __init__(self, name, courses):
        '''(Student, str, list) -> NoneType
        
        Create new Student object with name and courses currently enrolled
        in.'''        
        
        self.name = name
        self.courses = []
        
    def create(self):
        return Student(self, [])
    
    def enrol(self, course):
        course.names.append(self.name)
        self.courses.append(course.code)
        
    
class Course:
    '''Represent courses '''
    def __init__(self, code, names):
        '''(Course, str, list) -> NoneType
        
        Create a new Course object with the names of students enrolled.'''
        
        self.code = code
        self.names = []        
        
    def create(self):
        return Course(self, [])