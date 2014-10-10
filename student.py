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
    pass


class NonExistentStudentError(Exception):
    pass


class FullCourseError(Exception):
    pass


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
    '''A database for students and classes.

    The class represents a database to store student and course objects.
    Since the students and courses can be referred to by their names
    and course codes, dictionaries will be used to reference objects.

    It handles database transactions like adding objects to and
    getting objects from the database.

    Attributes:
    - self.student_database (dictionary): database of student objects
    - self.course_database (dictionary): database of course objects
    '''

    def __init__(self):
        '''(Database) -> NoneType
        Create a database with two dictionaries to store students and courses.
        '''

        self.student_database = {}
        self.courses_database = {}

    def push_student(self, student_name, student_object):
        '''(Database, str, Student) -> NoneType
        Push a student into the database.

        Paramaters:
        - student_name: the name to be used as dictionary key.
        - student_object: the actual Student object
        '''

        self.student_database[student_name] = student_object

    def delete_student(self, student_name):
        '''(Database, str) -> NoneType
        Delete a student from the database. Used for undoing the create
        command.

        Paramaters:
        - student_name: name of student, the key containing this name
            will be deleted.
        '''

        del self.student_database[student_name]

    def get_student_object(self, student_name):
        '''(Database, str) -> Student
        Return the Student object with the given name.

        Parameters:
        - student_name: name of student, the key containing this name
            will be returned.
        '''

        try:
            return self.student_database[student_name]
        except KeyError:
            raise NonExistentStudentError

    def get_course_object(self, course_code):
        '''(Database, str) -> Course
        Return the Course object with the given course code.

        If there is no Course object with the given course code,
        create and return one.

        Parameters:
        - course_code: course code, the key containing this course code
            will be returned.
        '''

        try:
            return self.courses_database[course_code]
        except KeyError:
            course_object = Course(course_code)
            self.courses_database[course_code] = course_object
            return course_object


class Student:
    '''A student object with student information.

    The class represents a student with their name and the courses they are
    enrolled in.

    Supports enrolling and dropping courses, listing courses student is
    enrolled in, and courses taking with another student.

    Attributes:
    - self.student_name (str): the student's name.
    - self.courses (list): the list of courses (stored as course codes)
        the student is enrolled in.'''

    def __init__(self, student_name):
        '''(Student, str) -> NoneType
        Create a Student with given name and empty course list.

        Parameters:
        - student_name: the name of the student.
        '''

        self.student_name = student_name
        self.courses = []

    def enrol(self, course_code, course_object):
        '''(Student, str, Course) -> NoneType
        Enrol student into a course.
        Raise errors if course is full or already enrolled.

        Parameters:
        - course_code: the course code to be added to the list of courses.
        - course_object: the Course object, enrol() will be called on
            this object.
        '''

        if course_object.is_full():
            raise FullCourseError
        elif course_code in self.courses:
            raise AlreadyTakingCourseError
        else:
            self.courses.append(course_code)
            course_object.enrol(self.student_name)

    def drop(self, course_code, course_object):
        '''(Student, str, Course) -> NoneType
        Drop student from a course.

        Parameters:
        - course_code: the course code to be removed from list of courses.
        - course_object: the Course object, drop() will be called on
            this object.
        '''

        if course_code in self.courses:
            self.courses.remove(course_code)
            course_object.drop(self.student_name)
        else:
            raise NotTakingCourseError

    def list_courses(self):
        '''(Student) -> str
        Return the list of courses student is enrolled in.'''

        if len(self.courses) == 0:
            return "{} is not taking any courses.".format(self.student_name)
        else:
            nice_list_of_courses = ', '.join(sorted(self.courses))
            return "{} is taking {}" \
                   .format(self.student_name, nice_list_of_courses)

    def common_courses(self, student_2_object):
        '''(Student, Student) -> str
        Return the list of common courses student and the other student
            are taking.

        Parameters:
        - student_2_object: the other Student object to get courses from.'''

        self_courses = self.courses
        student_2_courses = student_2_object.get_courses()
        common_courses = list(set(self_courses) & set(student_2_courses))
        return ', '.join(sorted(common_courses))

    def get_courses(self):
        '''(Student) -> list
        Return the list of courses for common_courses().'''

        return self.courses


class Course:
    '''A course with enrolment information.

    The class represents a course with its code and the students
    enrolled in it.

    Attributes:
    - self.course_code (str): the course code.
    - self.student_list (list): the list of students enrolled (by name).'''

    def __init__(self, course_code):
        '''(Course, str) -> NoneType
        Create a Course object with course code and student list.

        Parameters:
        - course_code: the course code
        '''

        self.course_code = course_code
        self.student_list = []

    def is_full(self):
        '''(Course) -> bool
        Return whether the course is full or not.'''

        return len(self.student_list) >= 30

    def enrol(self, student_name):
        '''(Course, str) -> NoneType
        Enrol a student into the course.

        Parameters:
        - student_name: the name of the student to be added to the class list.
        '''

        self.student_list.append(student_name)

    def drop(self, student_name):
        '''(Course, str) -> NoneType
        Drop a student from the course.

        Parameters:
        - student_name: the name of the student to be removed from
            the class list.
        '''

        self.student_list.remove(student_name)

    def class_list(self):
        '''(Course) -> str
        Return the list of students enrolled in the course.'''

        class_list = self.student_list
        if len(class_list) == 0:
            return "No one is taking {}.".format(self.course_code)
        else:
            return ', '.join(sorted(class_list))


class History:
    ''' A class that stores the program's history.

    The class stores the commands entered in the front end and allows
    undoing of those commands.

    Attributes:
    - self.history (Stack): a stack with the commands entered.'''

    def __init__(self):
        '''(History) -> NoneType
        Create a History object with a command stack.'''

        self.history = Stack()

    def push(self, command):
        '''(History, str) -> NoneType
        Push a command into the command stack.

        Parameters:
        - command: the command to be pushed.'''

        self.history.push(command)

    def undo(self, n, database):
        '''(History, object, Database) -> NoneType
        Undo the last n command(s) in the history.
        Raise ValueError if n isn't a positive natural number.

        Parameters:
        - n: number of commands to undo.
        - database: the database to execute undo commands on.
        '''

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
                    student_object = \
                        database.get_student_object(split_command[1])
                    course_code = split_command[2]
                    course_object = database.get_course_object(course_code)
                    if split_command[0] == 'enrol':
                        student_object.drop(course_code, course_object)
                    elif split_command[0] == 'drop':
                        student_object.enrol(course_code, course_object)
