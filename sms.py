# Assignment 1 - Managing students!
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
"""Interactive console for assignment.

This module contains the code necessary for running the interactive console.
As provided, the console does nothing interesting: it is your job to build
on it to fulfill all the given specifications.

run: Run the main interactive loop.
"""

from student import *

def run():
    """ (NoneType) -> NoneType

    Run the main interactive loop.
    """

    all_students = {}
    all_courses = {}
    history = History()
    
    while True:
        command = input('')
        split_command = command.split()

        if command == 'exit':
            break
        
        elif command == '':
            print("Unrecognized command!")
            history.push('')
        
        elif split_command[0] == 'undo':
            undo(split_command, all_students, all_courses, history)
                
        elif len(split_command) == 3:
            if split_command[0] == 'create':
                create_student(split_command[2], all_students, history)
                    
            elif split_command[0] == 'enrol':
                enrol(split_command[1], split_command[2], all_students, \
                      all_courses, history)
                
            elif split_command[0] == 'drop':
                drop(split_command[1], split_command[2], all_students, \
                      all_courses, history)
                
            elif split_command[0] == 'common-courses':
                common_courses(split_command, all_students, history)
            
            else:
                print('Unrecognized command!')
                history.push('')
                        
        elif len(split_command) == 2:
            if split_command[0] == 'list-courses':
                list_courses(split_command[1], all_students, history)
                    
            elif split_command[0] == 'class-list':
                class_list(split_command[1], all_courses, history)
            
            else:
                print("Unrecognized command!")
                history.push('')
    
        else:
            print("Unrecognized command!")
            history.push('')
                
def create_student(student_name, all_students, history):
    try:                
        Student(student_name, all_students)
        history.push('create student {}'.format(student_name))
    except DuplicateStudentError:
        print('ERROR: Student {} already exists.'.format(student_name))
        history.push('')    

def enrol(student_name, course_code, all_students, all_courses, history):
    try:
        student_object = all_students[student_name]
        try:
            course_object = all_courses[course_code]
        except KeyError:
            course_object = Course(course_code)
            all_courses[course_code] = course_object
            
        try:
            student_object.enrol(course_code, course_object)
            history.push('enrol {} {}'.format(student_name, course_code))
        except FullCourseError:
            print('ERROR: Course {} is full.'.format(course_code))
            history.push('')
        except AlreadyTakingCourseError: 
            history.push('')
            
    except KeyError:
        print("ERROR: Student {} does not exist.".format(student_name))
        history.push('')

def drop(student_name, course_code, all_students, all_courses, history):
    try:
        student_object = all_students[student_name]
        try:
            course_object = all_courses[course_code]
        except KeyError:
            course_object = Course(course_code)
            all_courses[course_code] = course_object
            
        try:
            course_object = all_courses[course_code]
            student_object.drop(course_code, course_object)
            history.push('drop {} {}'.format(student_name, course_code))
        except NotTakingCourseError:
            history.push('')
            
    except KeyError:
        print("ERROR: Student {} does not exist.".format(student_name))
        history.push('')
        
def list_courses(student_name, all_students, history):
    try:
        student_object = all_students[student_name]
        print(student_object.list_courses())
    except KeyError:
        print("ERROR: Student {} does not exist.".format(student_name))
    history.push('')    

def common_courses(split_command, all_students, history):
    try:
        student_1_object = all_students[split_command[1]]
        student_2_object = all_students[split_command[2]]
        print(student_1_object.common_courses(student_2_object))
    except KeyError:
        for i in range(1, 3):
            if not split_command[i] in all_students:
                print("ERROR: Student {} does not exist.".format(split_command[i]))
    history.push('')
    
def class_list(course_code, all_courses, history):
    try:
        course_object = all_courses[course_code]
        print(course_object.class_list())
    except KeyError:
        print("No one is taking {}.".format(course_code))
    history.push('')
    
def undo(split_command, all_students, all_courses, history):
    try:
        if len(split_command) == 1:
            history.undo(1, all_students, all_courses)
        elif len(split_command) == 2:
            history.undo(split_command[1], all_students, all_courses)
        else:
            print("Unrecognized command!")
            history.push('')

    except ValueError:
        print('ERROR: {} is not a positive natural number.'.format(split_command[1]))
    except EndOfHistoryError:
        print('ERROR: No commands to undo.')    

if __name__ == '__main__':
    run()
