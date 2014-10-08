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

# Exceptions

class DuplicateStudentError(Exception):
    def __str__(self, student_name):
        return 'ERROR: Student {} already exists.'.format(student_name)
    
class NonExistentStudentError(Exception):
    pass
    
class FullCourseError(Exception):
    def __str__(self, course_code):
        return 'ERROR: Course {} is full.'.format(course_code)
    
class AlreadyTakingCourseError(Exception):
    pass
    
class NotTakingCourseError(Exception):
    pass
    
class EndOfHistoryError(Exception):
    pass

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
        
class Database:
    def __init__(self):
        self.student_database = {}
        self.courses_database = {}
        
    def push_student(self, student_name, student_object):
        self.student_database[student_name] = student_object
        
    def delete_student(self, student_name):
        del self.student_database[student_name]
        
    def get_student_object(self, student_name):
        try:
            return self.student_database[student_name]
        except KeyError:
            raise NonExistentStudentError
        
    def get_course_object(self, course_code):
        try:
            return self.courses_database[course_code]
        except KeyError:
            course_object = Course(course_code)
            self.courses_database[course_code] = course_object
            return course_object

class Student:
    '''Represent students with names and the courses they are taking.'''
    def __init__(self, student_name, database):
        try:
            database.get_student_object(student_name)
            raise DuplicateStudentError
        except NonExistentStudentError:    
            self.student_name = student_name
            self.courses = []
            database.push_student(self.student_name, self)
        
    def enrol(self, course_code, course_object):
        if course_object.is_full():
            raise FullCourseError
        elif course_code in self.courses:
            raise AlreadyTakingCourseError
        else:
            self.courses.append(course_code)
            course_object.enrol(self.student_name)
            
    def drop(self, course_code, course_object):
        if course_code in self.courses:
            self.courses.remove(course_code)
            course_object.drop(self.student_name)
        else:
            raise NotTakingCourseError
            
    def list_courses(self):
        if len(self.courses) == 0:
            return "{} is not taking any courses.".format(self.student_name)
        else:
            nice_list_of_courses = ', '.join(sorted(self.courses))
            return "{} is taking {}".format(self.student_name, nice_list_of_courses)
        
    def common_courses(self, student_2_object):
        self_courses = self.courses
        student_2_courses = student_2_object.get_courses()
        common_courses = list(set(self_courses) & set(student_2_courses))
        return ', '.join(sorted(common_courses))
    
    def get_courses(self):
        ''' Get courses for common courses. '''
        return self.courses
        
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

class History:
    def __init__(self):
        self.history = Stack()
        
    def push(self, command):
        return self.history.push(command)
        
    def undo(self, n, database):
        if type(n) != int:
            n = int(n)
        if n <= 0:
            raise ValueError
        
        for i in range(n):
            if self.history.is_empty():
                raise EndOfHistoryError
            else:   
                command = self.history.pop()
                split_command = command.split()
                if command == '':
                    pass
                elif split_command[0] == 'create':
                    database.delete_student(split_command[2])
                else:
                    student_object = database.get_student_object(split_command[1])
                    course_code = split_command[2]
                    course_object = database.get_course_object(course_code)
                    if split_command[0] == 'enrol':
                        student_object.drop(course_code, course_object)
                    elif split_command[0] == 'drop':
                        student_object.enrol(course_code, course_object)
                    
