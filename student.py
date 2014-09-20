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

all_students = {}
all_courses = {}

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
        if name in all_students:
            print("ERROR: Student {} already exists.".format(name))
        else:
            self.name = name
            self.courses = []
            all_students[name] = self
        
        print(all_students)
        print(all_students[name].name)
        #print(all_students[name].courses)
            
    def enrol(self, course):
        self.courses.append(course)        
        all_courses[course].append(self)
        print("success!")
        print(self.courses)
        print(all_courses)
        
    def drop(self, course):
        self.courses.pop(self.courses.index(course))