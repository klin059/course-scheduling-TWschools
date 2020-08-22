# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:23:24 2018
Post processing \ checking requirements are met
@author: KML
"""
import pandas as pd
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

def checking_two_days_apart_requirements(status):
    for course in status.list_of_assigned_Courses:
        if 'two_days_apart' in course.requirements:
#            print("{}:{}".format(course.name, course.period))
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
    
def checking_consecutive_requirements(status):
    for course in status.list_of_Courses:
        if 'consecutive' in course.requirements:
            periods = [] 
            courses = []
            for c in course.requirements['consecutive']:
                courses.append(c) 
                periods.append(c.period)
            p1 = periods[0]
            p2 = periods[1]
            assert p1[0] == p2[0],'{}:{},{}:{} not consecutive'.format(courses[0].name,periods[0],courses[1].name,periods[1])
            assert (p1[1] + 1 == p2[1]) or (p1[1] - 1 == p2[1]), '{}:{},{}:{} not consecutive'.format(courses[0].name,periods[0],courses[1].name,periods[1])
        else:
            continue                

def checking_all_requirements(status):
    checking_two_days_apart_requirements(status)
    checking_consecutive_requirements(status)
        
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