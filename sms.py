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
    history = Stack()
    
    while True:
        command = input('')
        split_command = command.split()

        if command == 'exit':
            break
        
        elif split_command[0] == 'undo':
            if len(split_command) == 1:
                undo(1, history, all_students, all_courses)
            elif len(split_command) == 2:
                try:
                    undo(int(split_command[1]), history, all_students, all_courses)
                except ValueError:
                    print('ERROR: {} is not a positive natural number.'.format(split_command[1]))
            else:
                print("Unrecognized command!")
                history.push('')
            #print(history.items)
    
        elif len(split_command) == 3:
            if split_command[0] == 'create':
                name = split_command[2]
                
                if name in all_students:
                    print("ERROR: Student {} already exists.".format(name))
                    history.push('')
                else:    
                    all_students[name] = Student(name)
                    history.push('create student {}'.format(name))
                    
            elif split_command[0] == 'enrol':
                student_name = split_command[1]
                course_code = split_command[2]
                try:
                    student_object = all_students[student_name]
                    try:
                        course_object = all_courses[course_code]
                    except KeyError:
                        course_object = Course(course_code)
                        all_courses[course_code] = course_object
                        
                    if course_object.is_full():
                        print('ERROR: Course {} is full.'.format(course_code))
                        history.push('')
                    elif student_object.is_taking_course(course_code):
                        history.push('')
                    else:
                        student_object.enrol(course_code)
                        course_object.enrol(student_name)
                        history.push('enrol {} {}'.format(student_name, course_code))
                        
                except KeyError:
                    print("ERROR: Student {} does not exist.".format(student_name))
                    history.push('')
                    
                #debug                   
                #print(student_object.courses)
                #print(course_object.student_list)
        
            elif split_command[0] == 'drop':
                student_name = split_command[1]
                course_code = split_command[2]
                try:
                    student_object = all_students[student_name]
                        
                    if student_object.is_taking_course(course_code):
                        student_object.drop(course_code)
                        course_object = all_courses[course_code]
                        course_object.drop(student_name)
                        history.push('drop {} {}'.format(student_name, course_code))
                    else:
                        history.push('')
                        
                except KeyError:
                    print("ERROR: Student {} does not exist.".format(student_name))
                    history.push('')
                    
            elif split_command[0] == 'common-courses':
                try:
                    student_1_object = all_students[split_command[1]]
                    student_2_object = all_students[split_command[2]]
                    print(student_1_object.common_courses(student_2_object))
                except KeyError:
                    for i in range(1, 3):
                        if not split_command[i] in all_students:
                            print("ERROR: Student {} does not exist.".format(split_command[i]))
                history.push('')
            
            else:
                print('Unrecognized command!')
                history.push('')
                        
        elif len(split_command) == 2:
            if split_command[0] == 'list-courses':
                try:
                    student_object = all_students[split_command[1]]
                    print(student_object.list_courses())
                except KeyError:
                    print("ERROR: Student {} does not exist.".format(split_command[1]))
                history.push('')
                    
            elif split_command[0] == 'class-list':
                try:
                    course_object = all_courses[split_command[1]]
                    print(course_object.class_list())
                except KeyError:
                    print("No one is taking {}.".format(split_command[1]))
                history.push('')
            
            else:
                print("Unrecognized command!")
                history.push('')
    
        else:
            print("Unrecognized command!")
            history.push('')
    
def undo(n, history, all_students, all_courses):
    if n <= 0:
        raise ValueError
    for i in range(n):
        if history.is_empty():
            print('ERROR: No commands to undo.')
            break
        else:   
            command = history.pop()
            split_command = command.split()
            if command == '':
                pass
            elif split_command[0] == 'create':
                del all_students[split_command[2]]
            else:
                student_object = all_students[split_command[1]]
                course_object = all_courses[split_command[2]]
                if split_command[0] == 'enrol':
                    student_object.drop(split_command[2])
                    course_object.drop(split_command[1])
                elif split_command[0] == 'drop':
                    student_object.enrol(split_command[2])
                    course_object.enrol(split_command[1])
                
if __name__ == '__main__':
    run()
