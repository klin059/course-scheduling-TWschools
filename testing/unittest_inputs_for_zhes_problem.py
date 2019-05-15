# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 00:00:23 2018
test zhes problem inputs
@author: KML
"""
import unittest

import BaseModel as bm
import zhes_scheduling_problem
import CourseScheduling as cs
import random

status = zhes_scheduling_problem.create_zhes_scheduling_problem_inputs()
grade_to_nHomeroom_dict = {'G1':7, 'G2':5, 'G3': 5, 'G4':5,'G5':6, 'G6':6}
grade_to_subject_to_nClass_dict = {
            'G1':{'國':5, '數':3, '綜合':2, '生活':5, '彈性':2, '美勞':1, '音樂':1, '健康':1, '體育':1, '閩南語':1, '英語':1},
            'G2':{'國':5, '數':3, '綜合':2, '生活':5, '彈性':2, '美勞':1, '音樂':1, '健康':1, '體育':1, '閩南語':1, '英語':1},
            'G3':{'國':5, '數':3, '綜合':2, '彈性':1, '社會':3, '美勞':2, '音樂':1, '彈性音樂':1, '健康':1, '體育':2, 
                  '閩南語':1, '英語':1, '彈性英語':1, '電腦':1, '自然':1, '自然實驗':2, "閱讀":1},
            'G4':{'國':5, '數':3, '綜合':2, '彈性':1, '社會':3, '美勞':2, '音樂':1, '彈性音樂':1, '健康':1, '體育':2, 
                  '閩南語':1, '英語':1, '彈性英語':1, '電腦':1, '自然':1, '自然實驗':2, "閱讀":1},
            'G5':{'國':5, '數':4, '綜合':3, '彈性':2, '社會':3, '美勞':2, '音樂':1, '彈性音樂':1, '健康':1, '體育':2, 
                  '閩南語':1, '英語':1, '彈性英語':1, '電腦':1, '自然':1, '自然實驗':2},
            'G6':{'國':5, '數':4, '綜合':3, '彈性':2, '社會':3, '美勞':2, '音樂':1, '彈性音樂':1, '健康':1, '體育':2,
                  '閩南語':1, '英語':1, '彈性英語':1, '電腦':1, '自然':1, '自然實驗':2}
            }
grade_to_hr_teacher_names = {
                'G1':['嘉珮','貞琇','G1玲宜','文文','代理G15','鴻銀','淑萍'],
                'G2':['琦琳','麗雯','惠玲','瑞桃','淑玫'],
                'G3':['師岑','代理G32','玉菁','代理G34','淑閔'],
                'G4':['翎君','代理G42','美而','代理G44','潔誼'],
                'G5':['容蘋','勝堯','玲宜','純惠','書瑋','代理G56'],
                'G6':['佩紋','瓊瑤','茜茹','梅雪','丹絹','聖懿']
            }
class check_problem_input(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass    
    def test_no_repeat_names_in_homeroom_tr(self):
        list_of_names = []
        for g, names in grade_to_hr_teacher_names.items():
            list_of_names+=names
#        print(list_of_names)
        for name in list_of_names:
            self.assertEqual(list_of_names.count(name),1, "teacher name {} repeated".format(name))
    def test_all_courses_are_generated(self):
        total_number_of_Courses = 0
        for grade, subject_to_nClass in grade_to_subject_to_nClass_dict.items():
            n_homeroom = grade_to_nHomeroom_dict[grade]
            n_courses_in_grade = 0
            for sub, n_class in subject_to_nClass.items():
                n_courses_in_grade += n_class
            total_number_of_Courses += (n_homeroom * n_courses_in_grade)
        self.assertEqual(len(status.list_of_Courses), total_number_of_Courses)
    def test_all_teachers_have_a_type(self):
        for teacher in status.list_of_Teachers:
            self.assertTrue(teacher.type in ['subject','homeroom'])
    def test_add_Teacher_to_list1(self):
        # add existing homeroom teacher - added course tuple
        
        
        # add non-existing homeroom should raise exception
        
        # add existing subject teacher should add course tuple
        
        # add non-existing subject teacher should create a subject teacher with the corresponding tuple
        pass
        
    
#    def test_no_repetition_in_teacher_names(self):
#        """ this one doesn't work properly coz courses are appened under same name"""
#        teacher_names = []
#        # if there are more than one teachers with the same name, something is wrong in my code
#        for T in status.list_of_Teachers:
#            teacher_names.append(T.name)
##        print(teacher_names)    
#        for name in teacher_names:
#            self.assertEqual(teacher_names.count(name), 1)
            
    def test_courses_taken_by_teacher(self, teacher_name = '玲宜'):
        for T in status.list_of_Teachers:
            if T.name == '玲宜':
                for course in T.list_of_grade_homeroom_subject_tuple:
                    self.assertEqual(course[0], 'G5')
    def test_all_courses_are_assigned_one_and_only_one_teacher(self):
        list_of_course_tuples = []
        for grade, nHomeroom in grade_to_nHomeroom_dict.items():
            for i in range(nHomeroom):
                class_ind = i+1
                for subject in grade_to_subject_to_nClass_dict[grade]:
                    list_of_course_tuples.append((grade, class_ind, subject))
        self.assertEqual(len(list_of_course_tuples), 494)
#        print(list_of_course_tuples)
        count = 0
        for T in status.list_of_Teachers:
            for course_tuple in T.list_of_grade_homeroom_subject_tuple:
                if course_tuple == ('G5', 1, '英語'):
                    print(T.name)
                if not course_tuple in list_of_course_tuples:
                    raise Exception("Cannot find course {} in {}".format(str(course_tuple), T.name ))
                else:
                    list_of_course_tuples.remove(course_tuple)
                    count +=1
        self.assertEqual(list_of_course_tuples, [], str(list_of_course_tuples))
        self.assertEqual(count, 494)
    
    def test_all_courses_are_assigned_one_and_only_one_room(self):
        pass
        
    def test_added_two_days_apart_requirements(self):
        for C in status.list_of_Courses:
            if C.name == 'G4_3_彈性英語_1':
                self.assertEqual([C.name for C in C.requirements['two_days_apart']], ['G4_3_英語_1', 'G4_3_彈性英語_1'])
                
    def test_pick_room_assignment(self):
        for C in status.list_of_Courses:
            if C.name == 'G4_3_彈性英語_1':
                break
        C.pick_room_assignment(status)
        self.assertEqual(C.homeRoom.name, 'G4_3')
        self.assertEqual(C.Room.name, '英語教室')
        for C in status.list_of_Courses:
            if C.name == 'G4_3_英語_1':
                break
        C.pick_room_assignment(status)
        self.assertEqual(C.homeRoom.name, 'G4_3')
        self.assertEqual(C.Room.name, 'G4_3')
        
    def test_assign_and_unassign_course(self):
        existing_assignment = len(status.list_of_assigned_Courses)
        bm.Course.assign_Rooms_and_Teacher_to_Course(status, 'G1_1_體育_1', '操場-1', 'G1_1', '梁雋')
        bm.Course.assign_Course_period(status, 'G1_1_體育_1', ('Monday', 4))
        
        bm.Course.assign_Rooms_and_Teacher_to_Course(status, 'G1_2_體育_1', '操場-1', 'G1_2', '梁雋')
        bm.Course.assign_Course_period(status, 'G1_2_體育_1', ('Wednesday', 4))   
        
        self.assertEqual(len(status.list_of_assigned_Courses), existing_assignment+2)
        course = None
        for C in status.list_of_Courses:
            if C.name == 'G1_1_體育_1':
                course = C
        self.assertTrue(('Monday', 4, course.name) in course.Room.schedule_in_tuples)
        self.assertTrue(('Monday', 4, course.name) in course.Teacher.schedule_in_tuples)
        self.assertTrue(('Monday', 4, course.name) in course.homeRoom.schedule_in_tuples)
        self.assertEqual(course.period, ('Monday', 4))
        self.assertTrue(course.assigned)
        self.assertEqual(len(status.list_of_assigned_Courses),existing_assignment + 2)
        
        course.unassign_course(status)
        self.assertEqual(len(status.list_of_assigned_Courses),existing_assignment+1)
        self.assertFalse(('Monday', 4, course.name) in course.Room.schedule_in_tuples)
        self.assertFalse(('Monday', 4, course.name) in course.Teacher.schedule_in_tuples)
        self.assertFalse(('Monday', 4, course.name) in course.homeRoom.schedule_in_tuples)
        self.assertEqual(course.period, None)
        self.assertFalse(course.assigned)
        
        bm.Course.unassign_Course(status, 'G1_2_體育_1')
        self.assertEqual(len(status.list_of_assigned_Courses),existing_assignment)
        
class unittest_scheduling(unittest.TestCase):
    def setUp(self):
        self.status = zhes_scheduling_problem.create_zhes_scheduling_problem_inputs()
    def tearDown(self):
        pass
    def test_consecutive_course_scheduleing1(self):
        # when none of the course were assigned
        consecutive_courses = []
        for C in self.status.list_of_unassigned_Courses:
            if C.name in ['G5_5_自然實驗_1','G5_5_自然實驗_2']:
                consecutive_courses.append(C)

        scheduling_results = cs.repeated_course_assignments_until_feasibility(self.status, consecutive_courses, max_count = 1)
        room = consecutive_courses[0].Room
        s1 = room.schedule_in_tuples[0]
        s2 = room.schedule_in_tuples[1]
        self.assertEqual(s1[0],s2[0])
        if s1[1] > s2[1]:
            self.assertTrue(s1[1] == s2[1] + 1)
        else:
            self.assertTrue(s1[1] == s2[1] - 1)
        self.assertTrue(scheduling_results)
        self.assertEqual(consecutive_courses[0].Room.name, consecutive_courses[1].Room.name)
        self.assertEqual(len(consecutive_courses[0].Room.schedule_in_tuples),2)
    def test_consecutive_course_scheduleing2(self):
        # when one of the course were assigned at [1,3,5]
        consecutive_courses = []
        for C in self.status.list_of_unassigned_Courses:
            if C.name in ['G5_5_自然實驗_1','G5_5_自然實驗_2']:
                consecutive_courses.append(C)
                
        bm.Course.assign_Rooms_and_Teacher_to_Course(self.status, consecutive_courses[0].name, '自然教室(五)', 'G5_5', '秀玲')
        bm.Course.assign_Course_period(self.status, consecutive_courses[0].name, ('Monday', 3))
                
        scheduling_results = cs.repeated_course_assignments_until_feasibility(self.status, [consecutive_courses[1]], max_count = 1)
        self.assertEqual(consecutive_courses[1].period, ('Monday', 4))
        
        self.assertTrue(scheduling_results)
        self.assertEqual(consecutive_courses[0].Room.name, consecutive_courses[1].Room.name)
        self.assertEqual(len(consecutive_courses[0].Room.schedule_in_tuples),2)
    def test_consecutive_course_scheduleing3(self):
        # when one of the course were assigned at [2,4]
        consecutive_courses = []
        for C in self.status.list_of_unassigned_Courses:
            if C.name in ['G5_5_自然實驗_1','G5_5_自然實驗_2']:
                consecutive_courses.append(C)
                
        bm.Course.assign_Rooms_and_Teacher_to_Course(self.status, consecutive_courses[0].name, '自然教室(五)', 'G5_5', '秀玲')
        bm.Course.assign_Course_period(self.status, consecutive_courses[0].name, ('Monday', 2))
                
        scheduling_results = cs.repeated_course_assignments_until_feasibility(self.status, [consecutive_courses[1]], max_count = 1)
        self.assertEqual(consecutive_courses[1].period, ('Monday', 1))
        
        self.assertTrue(scheduling_results)
        self.assertEqual(consecutive_courses[0].Room.name, consecutive_courses[1].Room.name)
        self.assertEqual(len(consecutive_courses[0].Room.schedule_in_tuples),2)
    def test_consecutive_course_scheduleing4(self):
        # when one of the course were assigned at [2,4]
        consecutive_courses = []
        for C in self.status.list_of_unassigned_Courses:
            if C.name in ['G5_5_自然實驗_1','G5_5_自然實驗_2']:
                consecutive_courses.append(C)
                
        bm.Course.assign_Rooms_and_Teacher_to_Course(self.status, consecutive_courses[0].name, '自然教室(五)', 'G5_5', '秀玲')
        bm.Course.assign_Course_period(self.status, consecutive_courses[0].name, ('Monday', 6))
                
        scheduling_results = cs.repeated_course_assignments_until_feasibility(self.status, [consecutive_courses[1]], max_count = 1)
        self.assertTrue(consecutive_courses[1].period in [('Monday', 5), ('Monday', 7)])
        
        self.assertTrue(scheduling_results)
        self.assertEqual(consecutive_courses[0].Room.name, consecutive_courses[1].Room.name)
        self.assertEqual(len(consecutive_courses[0].Room.schedule_in_tuples),2)
        
if __name__ == '__main__':
    unittest.main()