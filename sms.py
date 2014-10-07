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
            exit_sms()            
            break
        
        elif split_command[0] == 'undo':
            if len(split_command) == 1:
                undo(1)
            elif len(split_command) == 2:
                try:
                    if int(split_command[1]) > 0:
                        undo(int(split_command[1]))
                    else:
                        print('ERROR: {} is not a positive natural number.'.format(split_command[1]))
                except ValueError:
                    print('ERROR: {} is not a positive natural number.'.format(split_command[1]))
            else:
                print("Unrecognized command!")
                history.push('')
            #print(history.items)
    
        elif len(split_command) == 3:
            if split_command[0] == 'create':
                Student(split_command[2])
                
            elif split_command[0] == 'enrol':
                try:
                    student = all_students[split_command[1]]
                    student.enrol(split_command[2])
                except KeyError:
                    print("ERROR: Student {} does not exist.".format(split_command[1]))
                    history.push('')
                    
            elif split_command[0] == 'drop':
                try:
                    student = all_students[split_command[1]]
                    student.drop(split_command[2])
                except KeyError:
                    print("ERROR: Student {} does not exist.".format(split_command[1]))
                    history.push('')
                
            elif split_command[0] == 'common-courses':
                try:
                    all_students[split_command[1]].common_courses(split_command[2])
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
                    all_students[split_command[1]].list_courses()
                except KeyError:
                    print("ERROR: Student {} does not exist.".format(split_command[1]))
                history.push('')
                    
            elif split_command[0] == 'class-list':
                class_list(split_command[1])
                history.push('')
            
            else:
                print("Unrecognized command!")
                history.push('')
    
        else:
            print("Unrecognized command!")
            history.push('')
    

if __name__ == '__main__':
    run()
