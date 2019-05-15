# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 20:48:07 2018
unit tests for scoring
@author: KML
"""
import unittest
import scoring
import BaseModel as bm


course1 = bm.Course('G1',1,'fake',1)
course1.type = 'subject'
course2 = bm.Course('G1',1,'fake',2)
course3 = bm.Course('G1',1,'fake',3)

schedule = []  #(day, period, c_name)
schedule += [('Monday',i,'G1_1_fake_1') for i in [2,4]]+ [('Monday',i,'G1_1_fake2_1') for i in [5,6]]  #room penalty 10
schedule += [('Tuesday',i,'G1_1_fake_1') for i in [3,4]] + [('Tuesday',i,'G1_1_fake2_1') for i in [1,2,5]]  
schedule += [('Wednesday',i,'G1_1_fake_1') for i in [2,3,4]] + [('Wednesday',i,'G1_1_fake2_1') for i in [5,6]] 
schedule += [('Thursday',i,'G1_1_fake_1') for i in [2,3,5]] + [('Thursday',i,'G1_1_fake2_1') for i in [1,6,7]]

schedule_dict = {'Monday': [('Monday',i,'G1_1_fake_1') for i in [2,4]]+ [('Monday',i,'G1_1_fake2_1') for i in [5,6]],
                 'Tuesday': [('Tuesday',i,'G1_1_fake_1') for i in [3,4]] + [('Tuesday',i,'G1_1_fake2_1') for i in [1,2,5]],
                 'Wednesday': [('Wednesday',i,'G1_1_fake_1') for i in [2,3,4]] + [('Wednesday',i,'G1_1_fake2_1') for i in [5,6]],
                 'Thursday': [('Thursday',i,'G1_1_fake_1') for i in [2,3,5]] + [('Thursday',i,'G1_1_fake2_1') for i in [1,6,7]],
                 'Friday':[]
                  }

hr_teacher = bm.Teacher('tr_name',schedule)
hr_teacher.schedule_in_tuples = schedule
hr_teacher.type = 'homeroom'

subject_teacher = bm.SubjectTeacher('tr_name',schedule)
subject_teacher.type = 'subject'
subject_teacher.schedule_in_tuples = schedule

subject_teacher2 = bm.SubjectTeacher('tr_name',schedule)
subject_teacher2.type = 'subject'
subject_teacher2.on_hourly_rate = True
subject_teacher2.schedule_in_tuples = schedule

room = bm.Room('G1_1',[],[])
room.schedule_in_tuples += schedule

course1.Teacher = hr_teacher
course2.Teacher = subject_teacher
course3.Teacher = subject_teacher2
course1.homeRoom = room
course2.homeRoom = room
course3.homeRoom = room


status = bm.Status([course1, course2, course3], [hr_teacher,subject_teacher,subject_teacher2], [room])
status.change_Course_to_assigned_list(course1)
status.change_Course_to_assigned_list(course2)


class check_scoring_functions(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass    
    def test_sort_schedules_by_day(self):
        schedule_by_day = scoring.sort_schedules_by_day(schedule)
        for key, item in schedule_by_day.items():
            self.assertEqual(set(item), set(schedule_dict[key]))
    def test_get_Room_timetable_penalty(self):
        self.assertEqual(scoring.get_Room_timetable_penalty(status, room),30)
    def test_count_consecutive_ones(self):
        self.assertEqual(scoring._count_consecutive_ones([1,0,1,1,1,0]), 3)
        self.assertEqual(scoring._count_consecutive_ones([1,1,1,0,1,1,1]), 3)
    def test_homeroom_teacher_penalty_by_day(self):
        self.assertEqual(scoring.homeroom_teacher_penalty_by_day(schedule_dict['Monday']),0)
        self.assertEqual(scoring.homeroom_teacher_penalty_by_day(schedule_dict['Tuesday']),20)
        self.assertEqual(scoring.homeroom_teacher_penalty_by_day(schedule_dict['Wednesday']),10)
        self.assertEqual(scoring.homeroom_teacher_penalty_by_day(schedule_dict['Thursday']),10)
    def test_subject_teacher_penalty_by_day(self):
        self.assertEqual(scoring.subject_teacher_penalty_by_day(schedule_dict['Monday']),25)
        self.assertEqual(scoring.subject_teacher_penalty_by_day(schedule_dict['Tuesday']),120)
        self.assertEqual(scoring.subject_teacher_penalty_by_day(schedule_dict['Wednesday']),45)
        self.assertEqual(scoring.subject_teacher_penalty_by_day(schedule_dict['Thursday']),100)
        
    def test_subject_teacher_penalty_for_consecutive_courses(self):
        penalty = 0
        self.assertEqual(scoring.subject_teacher_penalty_for_consecutive_courses(penalty, schedule_dict['Monday']),0)
        self.assertEqual(scoring.subject_teacher_penalty_for_consecutive_courses(penalty, schedule_dict['Tuesday']),20)
        self.assertEqual(scoring.subject_teacher_penalty_for_consecutive_courses(penalty, schedule_dict['Wednesday']),20)
        self.assertEqual(scoring.subject_teacher_penalty_for_consecutive_courses(penalty, schedule_dict['Thursday']),0)
        self.assertEqual(scoring.subject_teacher_penalty_for_consecutive_courses(penalty, schedule_dict['Friday']),0)
    def test_subject_teacher_penalty_for_changing_grade_subject(self):
        self.assertEqual(scoring.subject_teacher_penalty_for_changing_grade_subject(0,schedule_dict['Monday']), 25)
        self.assertEqual(scoring.subject_teacher_penalty_for_changing_grade_subject(0,schedule_dict['Tuesday']), 100)
        self.assertEqual(scoring.subject_teacher_penalty_for_changing_grade_subject(0,schedule_dict['Wednesday']), 25)
        self.assertEqual(scoring.subject_teacher_penalty_for_changing_grade_subject(0,schedule_dict['Thursday']), 100)
#    def test_get_Teacher_tb_panelty(self):
#        self.assertEqual(scoring.get_Teacher_tb_panelty(hr_teacher), 40)
#        self.assertEqual(scoring.get_Teacher_tb_panelty(subject_teacher), 70)
#        self.assertEqual(scoring.get_Teacher_tb_panelty(subject_teacher2), 40)
    def test_get_status_penalty(self):
        self.assertEqual(scoring.get_status_penalty(status), 1390)
if __name__ == '__main__':
    unittest.main()