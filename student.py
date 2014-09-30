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

all_students = {} # {name: std_obj}
all_courses = {'csc': ['a', 'b', 'c']} # {'course_code': [students]}

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

history = Stack()

class Student:
    '''Represent students with names and the courses they are taking.'''
    def __init__(self, name):
        # Check if student already exists
        if name in all_students:
            print("ERROR: Student {} already exists.".format(name))
            history.push('')
        else:
            self.name = name
            self.courses = []
            all_students[name] = self
            history.push('create student {}'.format(name))
        
        #print(all_students)
        #print(all_students[name].name)
        #print(all_students[name].courses)
    
    def delete(self):
        del all_students[self.name]
            
    def enrol(self, course):
        try:
            # Check if student is already taking course
            if course in self.courses:
                history.push('')
            elif len(all_courses[course]) == 30:
                print('ERROR: Course {} is full.'.format(course))
                history.push('')
            else:
                all_courses[course].append(self.name)
                # Enrols student
                self.courses.append(course)
                history.push('enrol {} {}'.format(self.name, course))
                
        except KeyError:
            all_courses[course] = [self.name]
            # Enrols student
            self.courses.append(course)
            history.push('enrol {} {}'.format(self.name, course))
            
        #print(self.courses)
        #print(all_courses[course])
        
    def drop(self, course):
        if not course in all_courses:
            history.push('')
        elif course in self.courses:
            self.courses.remove(course)
            all_courses[course].remove(self.name)
            history.push('drop {} {}'.format(self.name, course))
        else:
            history.push('')
            
        #print(self.courses)
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
    try:    
        class_list = all_courses[course]
        if len(class_list) == 0:
            print("No one is taking {}.".format(course))
        else:
            print(', '.join(sorted(class_list)))
    except KeyError:
        pass
        
        
def undo(n):
    for i in range(n):
        if history.is_empty():
            print('ERROR: No commands to undo.')
            break
        else:   
            command = history.pop()
            if command == '':
                pass
            else:
                split_command = command.split()
                if split_command[0] == 'create':
                    student = all_students[split_command[2]]
                    student.delete()
                elif split_command[0] == 'enrol':
                    student = all_students[split_command[1]]
                    student.drop(split_command[2])
                    history.pop()
                elif split_command[0] == 'drop':
                    student = all_students[split_command[1]]
                    student.enrol(split_command[2])
                    history.pop()
        
'''class Course:
    def __init__(self, course_code, student_list, course_size):
        self.course_code = course_code
        self.student_list = student_list
        self.course_size = course_size
    
    def class_list(self):
        print("Class list!")'''