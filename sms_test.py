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


class TestSMS(unittest.TestCase):

    # Methods for redirecting input and output
    # Do not change these!
    def setUp(self):
        self.out = StringIO('')
        sys.stdout = self.out
        self.error_nick = 'ERROR: Student nick does not exist.'
        self.error_nick_2 = 'ERROR: Student nick already exists.'
        self.error_nina = 'ERROR: Student nina does not exist.'
        self.create_nick_with_5_courses = ['create student nick',
                                           'enrol nick CSC148',
                                           'enrol nick RSM321',
                                           'enrol nick ECO336',
                                           'enrol nick RSM422',
                                           'enrol nick RSM423']

    def tearDown(self):
        self.out.close()
        self.out = None
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

    def io_tester(self, commands, outputs):
        """ (list of str, list of str) -> NoneType

        Simulate running input sms commands,
        check whether the output corresponds to outputs.
        DO NOT CHANGE THIS METHOD!
        """
        sys.stdin = StringIO('\n'.join(commands))
        run()
        self.assertEqual(self.out.getvalue(), '\n'.join(outputs))


    # YOUR TESTS GO HERE
    def test_simple(self):
        self.io_tester(['exit'], [''])
        
    def test_enrol_error(self):
        self.io_tester(['enrol nick csc', 'exit'],
                       [self.error_nick, ''])
        
    def test_drop_error(self):
        self.io_tester(['drop nick csc', 'exit'],
                       [self.error_nick, ''])        
    
    def test_list_courses_error(self):
        self.io_tester(['list-courses nick', 'exit'],
                       [self.error_nick, ''])
        
    def test_common_courses_error(self):
        self.io_tester(['common-courses nina nick', 'exit'],
                       [self.error_nina, self.error_nick, ''])
        
    def test_duplicate_student(self):
        self.io_tester(['create student nick', 'create student nick', 'exit'],
                       [self.error_nick_2, ''])
        
    def test_case_sensitivity(self):
        self.io_tester(['create student nick', 'create student Nick', 'exit'],
                       [''])
        
    def test_drop_not_taking_course(self):
        self.io_tester(['create student nick', 'drop nick CSC148', 'exit'],
                       [''])        

    def test_enrol_already_taking_course(self):
        self.io_tester(['create student nick',
                        'enrol nick CSC148',
                        'enrol nick CSC148',
                        'exit'],
                       [''])        

    def test_list_courses_empty(self):
        self.io_tester(['create student nick', 
                        'list-courses nick', 'exit'],
                       ['nick is not taking any courses.',
                        ''])        

    def test_list_courses_standard(self):
        self.io_tester(self.create_nick_with_5_courses + \
                       ['list-courses nick', 'exit'],
                       ['nick is taking CSC148, ECO336, RSM321, RSM422, RSM423.',
                        ''])        

    def test_drop_and_list_courses(self):
        self.io_tester(self.create_nick_with_5_courses + \
                       ['drop nick ECO336', 'drop nick RSM423',
                           'list-courses nick', 'exit'],
                       ['nick is taking CSC148, RSM321, RSM422.',
                        ''])        

    def test_drop_not_taking_course(self):
        self.io_tester(['create student nick', 'drop nick CSC148', 'exit'],
                       [''])        


if __name__ == '__main__':
    unittest.main(exit=False)
