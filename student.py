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
        # Check if student already exists
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
        try:
            # Check if student is already taking course
            if course in self.courses:
                print("{} is already taking {}!".format(self.name, course))
            elif len(all_courses[course]) == 30:
                print("ERROR: Course {} is full.".format(course))
            else:
                all_courses[course].append(self.name)
                # Enrols student
                self.courses.append(course)
                print("success!")
                
        except KeyError:
            all_courses[course] = [self.name]
            # Enrols student
            self.courses.append(course)
            print("success!")
            
        print(self.courses)
        print(all_courses[course])
        
    def drop(self, course):
        if not course in all_courses:
            print("course does not exist!")
        elif course in self.courses:
            self.courses.remove(course)
            all_courses[course].remove(self.name)
            print("success!")
        else:
            print("{} not taking {}!".format(self.name, course))
            
        print(self.courses)
        #print(all_courses[course])
        
    def list_courses(self):
        if len(self.courses) == 0:
            print("{} is not taking any courses.".format(self.name))
        else:
            nice_list_of_courses = ', '.join(sorted(self.courses))
            print("{} is taking {}.".format(self.name, nice_list_of_courses))
        
    def common_courses(self, student_2):
        self_courses = self.courses
        student_2_courses = all_students[student_2].courses
        common_courses = list(set(self_courses) & set(student_2_courses))
        print(', '.join(sorted(common_courses)))
        
        
def class_list(course):
    print("Class list!")
        
'''class Course:
    def __init__(self, course_code, student_list, course_size):
        self.course_code = course_code
        self.student_list = student_list
        self.course_size = course_size
    
    def class_list(self):
        print("Class list!")'''