# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 23:24:26 2018

@author: KML
"""

import unittest
#from testing.unittest_inputs_for_zhes_problem import check_problem_input, unittest_scheduling
#from testing.unittest_scoring import check_scoring_functions
import testing.unittest_course_search

def runAllTestsNow():
    theTestSuite = unittest.TestSuite()
#    theTestSuite.addTest(unittest.makeSuite(check_problem_input))
#    theTestSuite.addTest(unittest.makeSuite(unittest_scheduling))
#    theTestSuite.addTest(unittest.makeSuite(check_scoring_functions))
    theTestSuite.addTest(unittest.makeSuite(testing.unittest_course_search.check_course_swapping))
    return theTestSuite

if __name__ == "__main__":
    unittest.main(defaultTest='runAllTestsNow')