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
        self.create_nina_with_5_courses = ['create student nina',
                                           'enrol nina HMB420',
                                           'enrol nina ENG444',
                                           'enrol nina MAT133',
                                           'enrol nina CSC148',
                                           'enrol nina RSM423']

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
                       ['nick is taking CSC148, ECO336, RSM321, RSM422, RSM423',
                        ''])        

    def test_drop_and_list_courses(self):
        self.io_tester(self.create_nick_with_5_courses + \
                       ['drop nick ECO336', 'drop nick RSM423',
                        'list-courses nick', 'exit'],
                       ['nick is taking CSC148, RSM321, RSM422',
                        ''])        

    def test_drop_enrol_and_list_courses(self):
        self.io_tester(self.create_nick_with_5_courses + \
                       ['drop nick ECO336', 'drop nick RSM423',
                        'enrol nick MAT157', 'enrol nick CSC120',
                        'list-courses nick', 'exit'],
                       ['nick is taking CSC120, CSC148, MAT157, RSM321, RSM422',
                        ''])

    def test_common_courses_standard(self):
        self.io_tester(self.create_nick_with_5_courses + \
                       self.create_nina_with_5_courses + \
                       ['common-courses nick nina', 'exit'],
                       ['CSC148, RSM423', ''])

    def test_common_courses_no_1(self):
        self.io_tester(['create student nick', 'common-courses nick nina', 'exit'],
                       [self.error_nina, ''])

    def test_common_courses_no_2(self):
        self.io_tester(['create student nina', 'common-courses nick nina', 'exit'],
                       [self.error_nick, ''])

    def test_common_courses_no_common(self):
        self.io_tester(self.create_nick_with_5_courses + \
                       self.create_nina_with_5_courses + \
                       ['drop nick CSC148', 'drop nina RSM423',
                        'common-courses nick nina', 'exit'],
                       ['', ''])
        
    def test_class_list_empty(self):
        self.io_tester(['class-list GymClass', 'exit'],
                       ['No one is taking GymClass.', ''])
        
    def test_class_list_all_dropped(self):
        self.io_tester(self.create_nick_with_5_courses + \
                       ['drop nick CSC148',
                        'class-list CSC148',
                        'exit'],
                       ['No one is taking CSC148.', ''])

    def test_class_list_standard(self):
        self.io_tester(self.create_nick_with_5_courses + \
                       self.create_nina_with_5_courses + \
                       ['create student annie', 'enrol annie CSC148',
                        'create student Annie', 'enrol Annie CSC148',
                        'class-list CSC148', 'exit'],
                       ['Annie, annie, nick, nina', ''])
        
    def test_nothing_to_undo(self):
        self.io_tester(['undo', 'exit'],
                       ['ERROR: No commands to undo.', ''])
        
    def test_nothing_to_undo_4(self):
        self.io_tester(['undo', 'undo', 'undo', 'undo','exit'],
                       ['ERROR: No commands to undo.',
                        'ERROR: No commands to undo.',
                        'ERROR: No commands to undo.',
                        'ERROR: No commands to undo.', ''])
        
    def test_nothing_to_undo_multiple(self):
        self.io_tester(['undo 10', 'exit'],
                       ['ERROR: No commands to undo.', ''])
        
    def test_undo_n_negative(self):
        self.io_tester(['undo -2', 'exit'],
                       ['ERROR: -2 is not a positive natural number.', ''])
        
    def test_undo_n_float(self):
        self.io_tester(['undo 3.14', 'exit'],
                       ['ERROR: 3.14 is not a positive natural number.', ''])
        
    def test_undo_n_str(self):
        self.io_tester(['undo n', 'exit'],
                       ['ERROR: n is not a positive natural number.', ''])
        
    def test_undo_create_student(self):
        self.io_tester(['create student nick', 'undo',
                        'enrol nick abc', 'exit'],
                       [self.error_nick, ''])
        
    def test_undo_enrol(self):
        self.io_tester(['create student nick', 'enrol nick abc',
                        'undo', 'list-courses nick', 'exit'],
                       ['nick is not taking any courses.', ''])
        
    def test_undo_drop(self):
        self.io_tester(['create student nick', 'enrol nick abc',
                        'drop nick abc', 'undo',
                        'list-courses nick', 'exit'],
                       ['nick is taking abc', ''])
    
    def test_undo_non_data_altering_methods(self):
        self.io_tester(['create student nick', 'enrol nick abc',
                        'drop nick abc', 'list-courses nick', 
                        'undo', 'exit'],
                       ['nick is not taking any courses.', ''])
    
    def test_undo_failed_command(self):
        self.io_tester(['create student nick', 'create student nick',
                        'undo', 'list-courses nick', 'exit'],
                       [self.error_nick_2,
                        'nick is not taking any courses.' ,''])
        
    def test_undo_two_commands(self):
        self.io_tester(['create student nick', 'enrol nick abc',
                        'enrol nick def', 'undo 2',
                        'list-courses nick', 'exit'],
                       ['nick is not taking any courses.', ''])
        
    def test_undo_three_commands(self):
        self.io_tester(['create student nick', 'enrol nick abc',
                        'enrol nick def', 'undo 3',
                        'list-courses nick', 'exit'],
                       [self.error_nick, ''])
        
    def test_undo_overflow(self):
        self.io_tester(['create student nick', 'enrol nick abc',
                        'enrol nick def', 'undo 14',
                        'list-courses nick', 'exit'],
                       ['ERROR: No commands to undo.', self.error_nick, ''])
        
    def test_undo_lots_of_commands(self):
        self.io_tester(['create student nick', 'enrol nick abc',
                        'enrol nick def', 'drop nick csc',
                        'drop nick abc', 'undo 3',
                        'list-courses nick', 'exit'],
                       ['nick is taking abc', ''])
        
    def test_unrecognized_command(self):
        self.io_tester(['create student nick nina', 'exit'],
                       ['Unrecognized command!', ''])
    
if __name__ == '__main__':
    unittest.main(exit=False)
