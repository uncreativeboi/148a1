# Assignment 1 - Managing Students!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
# Nguyen Binh Nguyen, nguye571
#
#
# ---------------------------------------------
"""The back-end data model for the program.

TODO: fill in this doctring with information about your
class(es)!
"""

class Stack:
    def __init__(self):
        '''(Stack) -> NoneType'''
        self.items = []
        
    def is_empty(self):
        '''(Stack) -> bool'''
        return self.items == []
    
    def pop(self):
        '''(Stack) -> object'''
        return self.items.pop()
    
    def push(self, item):
        '''(Stack, object) -> NoneType'''
        self.items.append(item)

class Student:
    '''Represent students with names and the courses they are taking.'''
    def __init__(self, name):
        self.name = name
        self.courses = []
        
    def is_taking_course(self, course_code):
        return course_code in self.courses
            
    def enrol(self, course_code):
        self.courses.append(course_code)
            
    def drop(self, course_code):
        self.courses.remove(course_code)
            
    def list_courses(self):
        if len(self.courses) == 0:
            return "{} is not taking any courses.".format(self.name)
        else:
            nice_list_of_courses = ', '.join(sorted(self.courses))
            return "{} is taking {}".format(self.name, nice_list_of_courses)
        
    def common_courses(self, student_2_object):
        self_courses = self.courses
        student_2_courses = student_2_object.courses
        common_courses = list(set(self_courses) & set(student_2_courses))
        return ', '.join(sorted(common_courses))
        
class Course:
    def __init__(self, course_code):
        self.course_code = course_code
        self.student_list = []
        
    def is_full(self):
        return len(self.student_list) >= 30
    
    def enrol(self, student_name):
        self.student_list.append(student_name)
    
    def drop(self, student_name):
        self.student_list.remove(student_name)
    
    def class_list(self):
        class_list = self.student_list
        if len(class_list) == 0:
            return "No one is taking {}.".format(self.course_code)
        else:
            return ', '.join(sorted(class_list))
