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
# Tingting Wang, wangtin8
# Nadeem Merali, meralina
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

    database = Database()
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
            undo(split_command, database, history)

        elif split_command[0] == 'create' \
           and split_command[1] == 'student'\
           and len(split_command) == 3:
            create_student(split_command[2], database, history)

        elif split_command[0] == 'enrol' and len(split_command) == 3:
            enrol(split_command[1], split_command[2], database, history)

        elif split_command[0] == 'drop' and len(split_command) == 3:
            drop(split_command[1], split_command[2], database, history)

        elif split_command[0] == 'common-courses' \
             and len(split_command) == 3:
            common_courses(split_command, database, history)

        elif split_command[0] == 'list-courses' \
           and len(split_command) == 2:
            list_courses(split_command[1], database, history)

        elif split_command[0] == 'class-list' \
             and len(split_command) == 2:
            class_list(split_command[1], database, history)

        else:
            print("Unrecognized command!")
            history.push('')


def create_student(student_name, database, history):
    '''(str, Database, History) -> NoneType
    Create a student.
    Print an error if student with same name exists.

    Parameters:
    - student_name: the student's name.
    - database: the database to add student to.
    - history: history stack to add command to.
    '''

    try:
        database.get_student_object(student_name)
        print('ERROR: Student {} already exists.'.format(student_name))
        history.push('')
    except NonExistentStudentError:
        database.push_student(student_name, Student(student_name))
        history.push('create student {}'.format(student_name))


def enrol(student_name, course_code, database, history):
    '''(str, str, Database, History) -> NoneType
    Enrol a student into a course, print an error if course is full
    or student does not exist.
    Do nothing if student already enrolled in course.

    Parameters:
    - student_name: the student's name.
    - course_code: the course's code.
    - database: the database to get student and course objects.
    - history: history stack to add command to.
    '''

    try:
        student_object = database.get_student_object(student_name)
        course_object = database.get_course_object(course_code)

        try:
            student_object.enrol(course_code, course_object)
            history.push('enrol {} {}'.format(student_name, course_code))
        except FullCourseError:
            print('ERROR: Course {} is full.'.format(course_code))
            history.push('')
        except AlreadyTakingCourseError:
            history.push('')

    except NonExistentStudentError:
        print("ERROR: Student {} does not exist.".format(student_name))
        history.push('')


def drop(student_name, course_code, database, history):
    '''(str, str, Database, History) -> NoneType
    Drop a student from a course, print error if student doesn't exist.
    Do nothing if student not enrolled in course.

    Parameters:
    - student_name: the student's name.
    - course_code: the course's code.
    - database: the database to get student and course objects.
    - history: history stack to add command to.
    '''

    try:
        student_object = database.get_student_object(student_name)
        course_object = database.get_course_object(course_code)

        try:
            student_object.drop(course_code, course_object)
            history.push('drop {} {}'.format(student_name, course_code))
        except NotTakingCourseError:
            history.push('')

    except NonExistentStudentError:
        print("ERROR: Student {} does not exist.".format(student_name))
        history.push('')


def list_courses(student_name, database, history):
    '''(str, Database, History) -> NoneType
    Print a list of courses student is taking.

    Parameters:
    - student_name: the student's name.
    - database: the database to get student object from.
    - history: history stack to add command to.
    '''

    try:
        student_object = database.get_student_object(student_name)
        print(student_object.list_courses())
    except NonExistentStudentError:
        print("ERROR: Student {} does not exist.".format(student_name))
    history.push('')


def common_courses(split_command, database, history):
    '''(list of str, Database, History) -> NoneType
    Print a list of common courses two students are taking.

    Parameters:
    - split_command: the input by user containing the two students' names.
    - database: the database to get student object from.
    - history: history stack to add command to.
    '''

    try:
        student_1_object = database.get_student_object(split_command[1])
        student_2_object = database.get_student_object(split_command[2])
        print(student_1_object.common_courses(student_2_object))
    except NonExistentStudentError:
        for i in range(1, 3):
            try:
                database.get_student_object(split_command[i])
            except NonExistentStudentError:
                print("ERROR: Student {} does not exist."
                      .format(split_command[i]))
    history.push('')


def class_list(course_code, database, history):
    '''(str, Database, History) -> NoneType
    Print the list of students in a course.

    Parameters:
    - course_code: the course code.
    - database: the database to get data from.
    - history: history stack to add command to.
    '''

    course_object = database.get_course_object(course_code)
    print(course_object.class_list())
    history.push('')


def undo(split_command, database, history):
    '''(list of str, Database, History) -> NoneType
    Undo commands.

    Parameters:
    - split_command: the input by user containing the number of commands
        to undo.
    - database: the database to execute undo commands on.
    - history: history stack to get commands from.
    '''

    try:
        if len(split_command) == 1:
            history.undo(1, database)
        elif len(split_command) == 2:
            history.undo(split_command[1], database)
        else:
            print("Unrecognized command!")
            history.push('')

    except ValueError:
        print('ERROR: {} is not a positive natural number.'
              .format(split_command[1]))
    except EndOfHistoryError:
        print('ERROR: No commands to undo.')


if __name__ == '__main__':
    run()
