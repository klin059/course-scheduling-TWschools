# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 16:08:53 2018
Scoring functions
@author: KML
"""
import BaseModel as bm

# 級任不連續超過4節, penalty += (n_consecutives - 4)*10000
HOMEROOM_CONSECUTIVE_PENALTY = 10000
# 空堂平均分配(半天一節，整天兩節)
NO_EMPTY_PERIOD = 10
# 科任盡量上下午平均，致多連續三節
SUBJECT_CONSECUTIVE_PENALTY = 200
# 盡量同年級同科目排在一起
CHANGING_GRADE_SUBJECT_PENALTY = 5
CHANGING_GRADE_SUBJECT_PENALTY_POWER = 2
# 鐘點教師集中天數
HOURLY_RATE_TEACHER_DAY_PENALTY = 10
UNASSIGNED_COURSE_PENALTY = 100000

def sort_schedules_by_day(schedule_in_tuples):
    """tuple in the form of (day, period_ind, course_name)"""
    
    schedule_dict = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}
    for schedule in schedule_in_tuples:
        schedule_dict[schedule[0]].append(schedule)
    return schedule_dict
        

def Room_timetalbe_penalty_by_day(schedule_in_tuples):
#    schedule_dict = sort_schedules_by_day(room.schedule_in_tuples)
#    for key, item in schedule_dict.items():
#        penalty += Room_timetalbe_penalty_by_day(item)
#        
#    return penalty
    pass

def get_Room_timetable_penalty(status, room):
    penalty = 0
    
    # 低年級第四節盡量不排科任
    if room.grade in ['G1','G2']:
        for schedule in room.schedule_in_tuples:
            if (schedule[1] == 4):
                C = bm.Course.get_Course_by_name(status, schedule[2])
                if C.Teacher.type == "subject":
                    penalty += 10
    
    return penalty


def _count_consecutive_ones(data):
    longest = 0
    current = 0
    for num in data:
        if num == 1:
            current += 1
        else:
            longest = max(longest, current)
            current = 0
    
    return max(longest, current)


def homeroom_teacher_penalty_by_day(day_schedules):
    penalty = 0
    
    occupied_periods = [0] * 7
    for schedule in day_schedules:
        occupied_periods[schedule[1] - 1] = 1
    # 級任不連續超過4節
    n_consecutives = _count_consecutive_ones(occupied_periods)
    if n_consecutives - 4 > 0:
        penalty += (n_consecutives - 4)*HOMEROOM_CONSECUTIVE_PENALTY
    
    # 空堂平均分配(半天一節，整天兩節)
    if sum(occupied_periods[:4]) == 4:
        penalty += NO_EMPTY_PERIOD
    if sum(occupied_periods[4:7]) == 3:
        penalty += NO_EMPTY_PERIOD
        
    return penalty

def subject_teacher_penalty_by_day(day_schedules):
    # 科任盡量上下午平均，致多連續三節
    penalty = 0
    
    penalty = subject_teacher_penalty_for_consecutive_courses(penalty, day_schedules)
        
    # 盡量同年級同科目排在一起
    penalty = subject_teacher_penalty_for_changing_grade_subject(penalty, day_schedules)  
    
    return penalty
def subject_teacher_penalty_for_consecutive_courses(penalty, day_schedules):
    occupied_periods = [0] * 7
    for schedule in day_schedules:
        occupied_periods[schedule[1] - 1] = 1
        
    n_consecutives = _count_consecutive_ones(occupied_periods)
    if n_consecutives - 3 > 0:
        penalty += (n_consecutives - 3)*SUBJECT_CONSECUTIVE_PENALTY
    return penalty
def subject_teacher_penalty_for_changing_grade_subject(penalty, day_schedules):
    # 盡量同年級同科目排在一起
    # put schedules in a list ordered by period
    p = 0
    list_of_grade_subject_tuple = [0]*7
    for schedule in day_schedules:
        course_in_list = schedule[2].split('_')
        list_of_grade_subject_tuple[schedule[1]-1] = (course_in_list[0],course_in_list[2])
        
    current_grade_subject = None
    
    for index, grade_subject in enumerate(list_of_grade_subject_tuple):
        if grade_subject == 0:
            continue
        else:
            if current_grade_subject is None:
                current_grade_subject = grade_subject
            else:
               
                if not current_grade_subject == grade_subject:
                    p += CHANGING_GRADE_SUBJECT_PENALTY  # 5
                    current_grade_subject = grade_subject
    penalty += p**CHANGING_GRADE_SUBJECT_PENALTY_POWER  # 2
    return penalty

def get_Teacher_tb_panelty(teacher):
    penalty = 0
    schedule_dict = sort_schedules_by_day(teacher.schedule_in_tuples)
    
    
    if teacher.type == 'homeroom':
        for key, day_schedule in schedule_dict.items():
            penalty += homeroom_teacher_penalty_by_day(day_schedule)

    
    elif teacher.type == 'subject':
        if not teacher.on_hourly_rate:
            # 科任盡量上下午平均，致多連續三節
            for key, day_schedule in schedule_dict.items():
                penalty += subject_teacher_penalty_by_day(day_schedule)
        else:
            # 鐘點教師集中天數
            for key, day_schedule in schedule_dict.items():
                if not day_schedule == []:
                    penalty += HOURLY_RATE_TEACHER_DAY_PENALTY
    else:
        raise Exception("Undefined teacher type for {}".format(teacher.name))

    return penalty

def get_Teacher_tb_penelty_by_day(teacher, day_schedule):
    
    if teacher.type == 'homeroom':
        penalty = homeroom_teacher_penalty_by_day(day_schedule)

    
    elif teacher.type == 'subject':
        if not teacher.on_hourly_rate:
            # 科任盡量上下午平均，致多連續三節
            penalty = subject_teacher_penalty_by_day(day_schedule)
        else:
            # 鐘點教師集中天數
            penalty = HOURLY_RATE_TEACHER_DAY_PENALTY
    else:
        raise Exception("Undefined teacher type for {}".format(teacher.name))

    return penalty

def get_status_penalty(status):
    penalty = 0
    penalty += len(status.list_of_unassigned_Courses) * UNASSIGNED_COURSE_PENALTY
    for C in status.list_of_assigned_Courses:
        penalty += get_Teacher_tb_panelty(C.Teacher)
        penalty += get_Room_timetable_penalty(status, C.homeRoom)

    return penalty