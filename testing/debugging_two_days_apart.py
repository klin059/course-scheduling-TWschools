# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 11:20:08 2018
test scheduling
@author: zhes
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 10:11:31 2018

@author: zhes
"""
#import solving_zhes_problem1_using_repeated_assignment as solving
import zhes_scheduling_problem
import CourseScheduling as cs
#import BaseModel as bm
#import scoring
import random
#import pickle
import pandas as pd
random.seed()

def output_data(room_dict, teacher_dict, output_folder = 'timetable//'):
        writer = pd.ExcelWriter(output_folder + 'rooms.xlsx', 'xlsxwriter')
        
        for room, df in room_dict.items():
            df.to_excel(writer, sheet_name = room)
            worksheet = writer.sheets[room]
            worksheet.set_column('A:F', 20)
#        for writer in writers:
        writer.save()
            
        teacher_writer = pd.ExcelWriter(output_folder + 'teacher_tb.xlsx','xlsxwriter')
        for teacher, df in teacher_dict.items():
            df.to_excel(teacher_writer, sheet_name = teacher)
            worksheet = teacher_writer.sheets[teacher]
            worksheet.set_column('A:F', 20)
        
        teacher_writer.save()

def put_solution_in_df(best_status):
    room_dict = {}
    for room in best_status.list_of_Rooms:
        room_dict[room.name] = room.get_timetable(best_status)
        
    teacher_dict = {}
    for teacher in best_status.list_of_Teachers:
        teacher_dict[teacher.name] = teacher.get_timetable()
        
    return room_dict, teacher_dict

def solving_zhes_with_sequencial_LNS(seed = None, n_iteration = 500):
        
    random.seed()
    
    subject_set = {'閱讀', '彈性英語', '電腦', '綜合', '數', '彈性', '生活', '音樂', 
        '健康', '閩南語', '英語', '自然', '社會', '彈性音樂', '國', '自然實驗', '體育', '美勞',
        '英語12a', '彈性英語12a','英語12b', '彈性英語12b', '英語12c', '彈性英語12c',
        '英語34a', '彈性英語34a','英語34b', '彈性英語34b', '英語34c', '彈性英語34c',
        '英語56a', '彈性英語56a','英語56b', '彈性英語56b','英語56c', '彈性英語56c'}
    

    best_status = zhes_scheduling_problem.initate_zhes_status()
    
    
    
    def only_keep_subjects(best_status, list_of_subjects):
        for C in best_status.list_of_unassigned_Courses.copy():
            if (C.subject  not in list_of_subjects): #
                best_status.change_unassigned_Course_to_stalled_list(C) 
                
#    only_keep_subjects(best_status, ["自然", "自然實驗"])
#    
#    best_status = cs.sequential_scheduling(best_status, max_iteration = n_iteration)
#    if not best_status.list_of_unassigned_Courses == []:
#        return best_status, None
#    best_status.fix_assigned_Courses()
#    best_status.free_stalled_Courses()
    
    only_keep_subjects(best_status, ['英語12a', '彈性英語12a','英語12b', '彈性英語12b', '英語12c', '彈性英語12c',
        '英語34a', '彈性英語34a','英語34b', '彈性英語34b', '英語34c', '彈性英語34c',
        '英語56a', '彈性英語56a','英語56b', '彈性英語56b','英語56c', '彈性英語56c'])  #, "英語", "彈性英語"
    
    best_status = cs.sequential_scheduling(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        return best_status, None
    best_status.fix_assigned_Courses()
#    best_status.free_stalled_Courses()
    
#    only_keep_subjects(best_status, ["音樂", "彈性音樂", '體育','美勞'])
#    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
#    if not best_status.list_of_unassigned_Courses == []:
#        return best_status, None
#    best_status.fix_assigned_Courses()
#    best_status.free_stalled_Courses()
#    
#    only_keep_subjects(best_status, subject_set - {'國', '數', '綜合', '彈性', '生活'})
#    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
#    if not best_status.list_of_unassigned_Courses == []:
#        print([c.name for c in best_status.list_of_unassigned_Courses])
#        return best_status, None
#    best_status.fix_assigned_Courses()
#    best_status.free_stalled_Courses()
#    
#    
#    best_status, scoring = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
#    if not best_status.list_of_unassigned_Courses == []:
#        print([c.name for c in best_status.list_of_unassigned_Courses])
#        return best_status, None
#    
#    print("not assigned: "+ str([C.name for C in best_status.list_of_unassigned_Courses]))
#    room_dict = {}
#    for room in best_status.list_of_Rooms:
#        room_dict[room.name] = room.get_timetable(best_status)
#        
#    teacher_dict = {}
#    for teacher in best_status.list_of_Teachers:
#        teacher_dict[teacher.name] = teacher.get_timetable()
        
    print('Assigned {} out of {} courses'.format(len(best_status.list_of_assigned_Courses + best_status.list_of_fixed_Courses), 
              len(best_status.list_of_Courses) - len(best_status.list_of_stalled_Courses)))
    
    return best_status, 100

def _two_days_apart_restricted_days(selected_course_day):
    """ input: selected day for one course, set days not available for the other courses """
#        if selected_course_day == 'Wednesday':
#            raise Exception('Cannot have Wednesday for two days apart requirement')
    
    restricted_days = {'Monday':{'Monday', 'Tuesday', 'Wednesday'},
                     'Tuesday':{'Monday', 'Tuesday', 'Wednesday','Thursday'},
                     'Wednesday':{'Tuesday','Wednesday','Thursday'},
                     'Thursday':{'Tuesday', 'Wednesday','Thursday','Friday'},
                     'Friday':{'Wednesday','Thursday','Friday'}
                     }
    return restricted_days[selected_course_day]

def checking_requirements(status):
    for course in status.list_of_assigned_Courses:
        if 'two_days_apart' in course.requirements:
            print("{}:{}".format(course.name, course.period))
            periods = [] 
            courses = []
            for c in course.requirements['two_days_apart']:
                courses.append(c) 
                periods.append(c.period)
            p1 = periods[0]
            p2 = periods[1]
            restricted_days = _two_days_apart_restricted_days(p1[0])
            if p2[0] in restricted_days:
                print('{}: {}, {}:{} not two days apart'.format(courses[0].name, p1, courses[1].name, p2))
        else:
            continue

    
if __name__ == '__main__':
    list_of_solution = []
    list_of_score = []
    
    for i in range(1):
        score = None
        while not score:
            sol, score = solving_zhes_with_sequencial_LNS()
        if sol:
            list_of_solution.append(sol)
            list_of_score.append(score)
            
    ind = list_of_score.index(min(list_of_score))
    best_solution = list_of_solution[ind]
    
    room_dict, teacher_dict = put_solution_in_df(best_solution)
    checking_requirements(sol)
#    with open('room_dict.pkl','wb') as f:
#        pickle.dump(room_dict, f)
#    with open('teacher_dict.pkl','wb') as f:
#        pickle.dump(teacher_dict, f)
#    output_data(room_dict, teacher_dict)
    
        
        