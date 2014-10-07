# Assignment 1 - Sample unit tests
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
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


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.out = StringIO('')
        
        
    def tearDown(self):
        exit_sms()
    
    def test_create_student(self):
        student = Student('nick')
        self.assertEqual(student.name, 'nick')
        
    #def test_create_student_duplicate(self):
        #Student('nina')
        #Student('nina')
        #self.out = StringIO('')
        #sys.stdout = self.out
        #self.assertEqual(self.out.getvalue(), 'ERROR: Student nina already exists.')
        
    def test_enrol(self):
        nina = Student('nina')
        nina.enrol('CSC148')
        self.assertEqual(nina.courses, ['CSC148'])
        
    def test_drop(self):
        nina = Student('nina')
        nina.enrol('CSC148')
        nina.drop('CSC148')
        self.assertEqual(nina.courses, [])
        
class TestEnrol(TestStudent):
    #tests here

if __name__ == '__main__':
    unittest.main(exit=False)
