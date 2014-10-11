# Assignment 1 - Sample unit tests
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# Tingting Wang, wangtin8
#
#
#
# ---------------------------------------------
"""Unit tests for student.py

Submit this file, containing *thorough* unit tests
for your code in student.py.
Note that you should not have any tests involving
standard input or output in here.
"""
import unittest
from student import *

# Assignment 1 - Sample unit tests
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Sample unit tests for sms.py.

Because we're the code we're testing interacts
with the console, we need to do a bit of fiddling
to handle standard input and output.
Luckily for you, we've provided a base method
that does all of the work; you just need to provide
the actual test cases.
"""
import unittest
import sys
from io import StringIO
from sms import run


class TestPushStudentDatabase(unittest.TestCase):
# Should database tests go after Student class tests
# because first need to test if Student class methods work?
    def setUp(self):
        self.DB = Database()
        self.std1 = Student('Nick')

    def test_init(self):
        self.database1 = Database()
        self.assertEqual({}, self.database1.student_database)

    def test_push_one_student(self):
        self.DB.push_student('Nick', self.std1)
        #self.assertEqual(self.DB.student_database    <- this here doesn't equal to the dictionary if I put {'Nick': <obj...>}


class TestStudent(unittest.TestCase):

    def test_standard_create(self):
        self.std1 = Student('Nina')
        self.assertEqual(self.std1.student_name, 'Nina')
        self.assertEqual(self.std1.courses, [])


class TestStudentEnrol(unittest.TestCase):

    def setUp(self):
        self.std1 = Student('Nick')
        self.course1 = Course('CSC148')
        self.course2 = Course('ANA300')
        self.course3 = Course('CSB349')
        self.course30 = Course('PSY100')

# this enrols 30 students (Nadeem0, Nadeem1,..etc.)
# into the course PSY100 for testing method when course is full
        for i in range(30):
            self.course30.enrol('Nadeem'+str(i))

    def test_standard_student_enrol(self):
        self.std1.enrol('CSC148', self.course1)
        self.assertEqual(self.std1.courses, ['CSC148'])

    def test_student_enrol_multiple_courses(self):
        self.std1.enrol('CSC148', self.course1)
        self.std1.enrol('ANA300', self.course2)
        self.std1.enrol('CSB349', self.course3)
        self.assertEqual(self.std1.courses, ['CSC148', 'ANA300', 'CSB349'])

    def test_course_full(self):
        self.assertRaises(FullCourseError, self.std1.enrol,
                          'PSY100', self.course30)

    def test_student_already_taking_course(self):
        self.std1.enrol('CSC148', self.course1)
        self.assertRaises(AlreadyTakingCourseError, self.std1.enrol,
                          'CSC148', self.course1)


class TestStudentDrop(unittest.TestCase):

    def setUp(self):
        self.std1 = Student('Nina')
        self.course1 = Course('CSC148')
        self.course2 = Course('ANA300')
        self.course3 = Course('HMB430')
        self.course30 = Course('PSY100')
        self.course4 = Course('GymClass')
        self.std1.enrol('CSC148', self.course1)
        self.std1.enrol('ANA300', self.course2)
        self.std1.enrol('HMB430', self.course3)
        self.std1.enrol('PSY100', self.course4)

    def test_standard_student_drop(self):
        self.std1.drop('CSC148', self.course1)
        self.assertEqual(self.std1.courses, ['ANA300', 'HMB430', 'PSY100'])

    def test_student_drop_multiple(self):
        self.std1.drop('CSC148', self.course1)
        self.std1.drop('ANA300', self.course2)
        self.std1.drop('HMB430', self.course3)
        self.assertEqual(self.std1.courses, ['PSY100'])

    def test_student_drop_all_courses(self):
        self.std1.drop('CSC148', self.course1)
        self.std1.drop('ANA300', self.course2)
        self.std1.drop('HMB430', self.course3)
        self.std1.drop('PSY100', self.course4)
        self.assertEqual(self.std1.courses, [])

    def test_student_drop_course_not_taking(self):
        self.assertRaises(NotTakingCourseError, self.std1.drop,
                          'GymClass', self.course4)


class TestListCourses(unittest.TestCase):

    def setUp(self):
        self.std1 = Student('Nadeem')
        self.std2 = Student('Nick')
        self.course1 = Course('CSC148')
        self.course2 = Course('ANA300')
        self.course3 = Course('CLA160')
        self.course4 = Course('CSC120')
        self.course5 = Course('CSC108')

    def test_standard_list_courses(self):
        self.std1.enrol('CSC148', self.course1)

        self.assertEqual(self.std1.list_courses(), 'Nadeem is taking CSC148')

    def test_list_multiple_courses(self):
        # alphabetical
        self.std1.enrol('CSC148', self.course1)
        self.std1.enrol('ANA300', self.course2)
        self.std1.enrol('CLA160', self.course3)

        self.assertEqual(self.std1.list_courses(),
                         'Nadeem is taking ANA300, CLA160, CSC148')

    def test_list_courses_in_order(self):
        self.std1.enrol('CSC120', self.course4)
        self.std1.enrol('CSC108', self.course5)
        self.std1.enrol('CSC148', self.course1)

        self.assertEqual(self.std1.list_courses(),
                         'Nadeem is taking CSC108, CSC120, CSC148')

    def test_list_courses_none(self):
        self.assertEqual(self.std2.list_courses(),
                         'Nick is not taking any courses.')


class TestCommonCourses(unittest.TestCase):

    def setUp(self):
        self.std1 = Student('Nina')
        self.std2 = Student('Nick')
        self.course1 = Course('CSC148')
        self.course2 = Course('ANA300')
        self.course3 = Course('CLA204')
        self.course4 = Course('CSC120')
        self.course5 = Course('CSC108')
        self.course6 = Course('csc148')

    def test_common_course_one(self):
        self.std1.enrol('CSC148', self.course1)
        self.std2.enrol('CSC148', self.course1)

        self.assertEqual(self.std1.common_courses(self.std2), 'CSC148')

    def test_common_courses_multiple(self):
        self.std1.enrol('CSC148', self.course1)
        self.std1.enrol('ANA300', self.course2)
        self.std1.enrol('CLA204', self.course3)

        self.std2.enrol('CSC120', self.course4)
        self.std2.enrol('ANA300', self.course2)
        self.std2.enrol('CSC148', self.course1)

        self.assertEqual(self.std1.common_courses(self.std2), 'ANA300, CSC148')

    def test_no_common_courses(self):
        self.std1.enrol('CSC108', self.course5)
        self.std1.enrol('ANA300', self.course2)
        self.std1.enrol('CLA204', self.course3)

        self.std2.enrol('CSC120', self.course4)
        self.std2.enrol('CSC148', self.course1)

        self.assertEqual(self.std1.common_courses(self.std2), '')

    def test_common_courses_alphabetical(self):
        self.std1.enrol('CSC120', self.course4)
        self.std1.enrol('CSC108', self.course5)
        self.std1.enrol('CSC148', self.course1)
        self.std1.enrol('csc148', self.course6)

        self.std2.enrol('CSC120', self.course4)
        self.std2.enrol('CSC108', self.course5)
        self.std2.enrol('CSC148', self.course1)
        self.std2.enrol('csc148', self.course6)

        self.assertEqual(self.std1.common_courses(self.std2),
                         'CSC108, CSC120, CSC148, csc148')


class TestGetCourses(unittest.TestCase):

    def setUp(self):
        self.std1 = Student('Nadeem')
        self.course1 = Course('CSC148')
        self.course2 = Course('ANA300')
        self.course3 = Course('CLA204')

    def test_standard_get_courses(self):
        self.std1.enrol('CSC148', self.course1)
        self.assertEqual(self.std1.get_courses(), ['CSC148'])

    def test_get_courses_multiple(self):
        self.std1.enrol('CSC148', self.course1)
        self.std1.enrol('ANA300', self.course2)
        self.std1.enrol('CLA204', self.course3)

        self.assertEqual(self.std1.get_courses(),
                         ['CSC148', 'ANA300', 'CLA204'])


class TestCourse(unittest.TestCase):

    def test_standard_create(self):
        self.course1 = Course('CSC148')
        self.assertEqual(self.course1.course_code, 'CSC148')
        self.assertEqual(self.course1.student_list, [])


class TestCourseEnrol(unittest.TestCase):

    def setUp(self):
        self.course1 = Course('CSC148')

    def test_standard_course_enrol(self):
        self.course1.enrol('Nina')
        self.assertEqual(self.course1.student_list, ['Nina'])

    def test_course_enrol_multiple(self):
        self.course1.enrol('Nina')
        self.course1.enrol('Nick')
        self.course1.enrol('Nadeem')
        self.assertEqual(self.course1.student_list, ['Nina', 'Nick', 'Nadeem'])

    # Don't need to test for enrolling same student twice because method Student enrol already catches this and raises an error if user tries to give such commands.


class TestIsFull(unittest.TestCase):

    def setUp(self):
        self.course1 = Course('CSC148')

    def test_is_full_over_30(self):
        # Enrols 30 students into CSC148
        for i in range(30):
            self.course1.enrol('RotmanDude'+str(i))

        self.assertTrue(self.course1.is_full())

    def test_is_full_less_than_30(self):
        self.assertFalse(self.course1.is_full())


class TestCourseDrop(unittest.TestCase):

    def setUp(self):
        self.course1 = Course('CSC148')

        self.course1.enrol('Nina')
        self.course1.enrol('Nick')
        self.course1.enrol('Nadeem')

    def test_standard_course_drop(self):
        self.course1.drop('Nina')

        self.assertEqual(self.course1.student_list, ['Nick', 'Nadeem'])

    def test_course_drop_multiple(self):
        self.course1.drop('Nina')
        self.course1.drop('Nick')
        self.assertEqual(self.course1.student_list, ['Nadeem'])

    def test_course_drop_all(self):
        self.course1.drop('Nina')
        self.course1.drop('Nick')
        self.course1.drop('Nadeem')
        self.assertEqual(self.course1.student_list, [])


class TestClassList(unittest.TestCase):

    def setUp(self):
        self.course1 = Course('CSC148')
        self.course2 = Course('Food')

    def test_standard_class_list(self):
        self.course1.enrol('Nina')
        self.assertEqual(self.course1.class_list(), 'Nina')

    def test_class_list_multiple_students(self):
        self.course1.enrol('Nina')
        self.course1.enrol('Nick')
        self.course1.enrol('Nadeem')
        self.assertEqual(self.course1.class_list(), 'Nadeem, Nick, Nina')

    def test_class_list_no_students(self):
        self.assertEqual(self.course1.class_list(), 'No one is taking CSC148.')

    def test_clas_list_alphabtical(self):
        self.course2.enrol('Red')
        self.course2.enrol('Velvet')
        self.course2.enrol('Cheesecake')
        self.assertEqual(self.course2.class_list(), 'Cheesecake, Red, Velvet')


if __name__ == '__main__':
    unittest.main(exit=False)