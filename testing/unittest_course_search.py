# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 15:51:57 2018
unittest for CourseSearch
@author: zhes
"""

import unittest
import pickle
import BaseModel as bm
import CourseSearch as CS
import scoring
#import solving_zhes_using_sequential_LNS as solving
import random
import copy
import os
random.seed(100)

with open('testing//status.pkl','rb') as f:
    status_original = pickle.load(f)
status_original.free_fixed_Courses()
#status = copy.deepcopy(status_original)
#print([C.name for C in status.list_of_assigned_Courses])
class check_course_swapping(unittest.TestCase):
    def setUp(self):
        self.status = copy.deepcopy(status_original)
    def tearDown(self):
        self.status = copy.deepcopy(status_original)    
    def test_check_same_homeRoom_course_swap_feasiblity(self):
        course1 = bm.Course.get_Course_by_name(self.status, 'G3_2_彈性英語_1')
        course2 = bm.Course.get_Course_by_name(self.status, 'G3_2_電腦_1')
        self.assertFalse(CS.check_same_homeRoom_course_swap_feasiblity(self.status, course1, course2))
        
        course1 = bm.Course.get_Course_by_name(self.status, 'G3_2_數_2')
        course2 = bm.Course.get_Course_by_name(self.status, 'G3_2_電腦_1')
        self.assertTrue(CS.check_same_homeRoom_course_swap_feasiblity(self.status, course1, course2))
        
        course1 = bm.Course.get_Course_by_name(self.status, 'G3_2_自然_1')
        course2 = bm.Course.get_Course_by_name(self.status, 'G3_2_美勞_2')
        self.assertFalse(CS.check_same_homeRoom_course_swap_feasiblity(self.status, course1, course2))
        
        course1 = bm.Course.get_Course_by_name(self.status, 'G3_2_數_3')
        course2 = bm.Course.get_Course_by_name(self.status, 'G3_2_國_4')
        self.assertTrue(CS.check_same_homeRoom_course_swap_feasiblity(self.status, course1, course2))
        
    def test_get_Teacher_day_score(self):
        course1 = bm.Course.get_Course_by_name(self.status, 'G6_2_英語_1')
        period1 = course1.period
        course2 = bm.Course.get_Course_by_name(self.status, 'G6_2_綜合_3')
        period2 = course2.period
        self.assertTrue(CS.check_same_homeRoom_course_swap_feasiblity(self.status, course1, course2))
        
        score1_orig = CS.get_Teacher_day_score(self.status, course1, period1)
        score1_after = CS.get_Teacher_day_score(self.status, course1, period2)
        print("1 orig {}, after {}".format(score1_orig, score1_after))
        self.assertTrue(score1_orig < score1_after)
        
        score2_orig = CS.get_Teacher_day_score(self.status, course2, period2)
        score2_after = CS.get_Teacher_day_score(self.status, course2, period1)
        print("2 orig {}, after {}".format(score2_orig, score2_after))
        self.assertTrue(score2_orig > score2_after)
        
        total_score = CS.get_change_of_scoring_for_same_homeRoom_course_swap(self.status, course1, course2, period1, period2)
        self.assertEqual(total_score, score1_after+score2_after-score1_orig-score2_orig)
        print(total_score)
        
    def test_get_swap_penalty_for_two_Courses1(self):
        # same homeroom
        self.assertEqual(CS.get_swap_penalty_for_two_Courses(self.status, 'G3_2_自然_1', 'G3_2_美勞_2'), None)
        c_tuple, penalty = CS.get_swap_penalty_for_two_Courses(self.status, 'G6_2_英語_1', 'G6_2_綜合_3')
        print(c_tuple[0].name, c_tuple[1].name)
        self.assertEqual(penalty, 765)

    def test_get_swap_penalty_for_two_Courses2(self):
        # different homeroom
        pass
    
    
if __name__ == '__main__':
    unittest.main()