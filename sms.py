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
    
    while True:
        command = input('')
        split_command = command.split()

        if command == 'exit':
            break
        
        elif split_command[0] == 'create':
            Student(split_command[2])
            
        elif split_command[0] == 'enrol':
            try:
                student = all_students[split_command[1]]
                student.enrol(split_command[2])
            except KeyError:
                print("ERROR: Student {} does not exist.".format(student_name))
                
        elif split_command[0] == 'drop':
            try:
                student = all_students[split_command[1]]
                student.drop(split_command[2])
            except KeyError:
                print("ERROR: Student {} does not exist.".format(student_name))
                
        elif split_command[0] == 'list-courses':
            try:
                all_students[split_command[1]].list_courses()
            except KeyError:
                print("ERROR: Student {} does not exist.".format(student_name))
                
        else:
            print("Unrecognized command!")
            pass
    

if __name__ == '__main__':
    run()
