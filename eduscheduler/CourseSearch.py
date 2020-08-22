# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 11:22:11 2018
Course schedule fine tuning

- only considered swapping courses of the same homeroom, but swapping courses with 
different homeroom e.g. from teacher's timetable or from subject room timetable should
also be possible
i.e. by swaping in-between two homerooms
e.g. G5_3, (Monday, 2) to (Monday,4) get the score
     G3_3, (Monday, 4) to (Monday, 2)
 for the corresponding schedule and check
the overall penalty

@author: KML
"""
import scoring
import BaseModel as bm

def get_swap_penalty_for_two_Courses(status, course1_name, course2_name):
    """ swapping courses, considering cases when two courses not belonging to the same homeroom
    """
    course1 = bm.Course.get_Course_by_name(status, course1_name)
    course2 = bm.Course.get_Course_by_name(status, course2_name)
    if course1.homeRoom == course2.homeRoom:
        return get_swap_penalty_for_same_homeRoom_Courses(status, course1, course2)
    else:
        # swapping courses of different homeroom
#        period1 = course1.period
        period2 = course2.period
        pass
        # get course at period1 of room1
        course_at_homeroom1_period1 = course1
        # get course at period 2 of room1
        course_at_homeroom1_period2 = None
        for schedule in course1.Room.schedule_in_tuples:
            if (schedule[0], schedule[1]) == period2:
                course_at_homeroom1_period2 = schedule[3]
        assert course_at_homeroom1_period2
        # get swap penalty if feasible
        penalty1 = get_swap_penalty_for_same_homeRoom_Courses(status, course_at_homeroom1_period1, course_at_homeroom1_period2)
        if penalty1 is None:
            return None
        # get course at period2 of room2
        course_at_homeroom2_period2 = course2
        # get course at period 1 of room2
        course_at_homeroom2_period1 = None
        for schedule in course1.Room.schedule_in_tuples:
            if (schedule[0], schedule[1]) == period2:
                course_at_homeroom1_period2 = schedule[3]
        assert course_at_homeroom1_period2
        # get swap penalty if feasible
        penalty2 = get_swap_penalty_for_same_homeRoom_Courses(status, course_at_homeroom2_period1, course_at_homeroom2_period2)        
        if penalty2 is None:
            return None
        # get overall swap penalty
        return ((course1, course2), penalty1[1]+penalty2[1])


def get_swap_penalty_for_same_homeRoom_Courses(status, course1, course2):
    
    c1_period = course1.period
    c2_period = course2.period
    if check_same_homeRoom_course_swap_feasiblity(status, course1, course2):
        penalty = get_change_of_scoring_for_same_homeRoom_course_swap(status, course1, course2, c1_period, c2_period)
        return ((course1, course2), penalty)
    else: 
        print('swap is infeasible')
        return None
            
def check_same_homeRoom_course_swap_feasiblity(status, course1, course2):
    
    c1_period = course1.period
    c2_period = course2.period
    course1.unassign_course(status)
    course2.unassign_course(status)
    
    feasible_periods = bm.Course.populate_set_of_periods()
    feasible_periods = course1.get_feasible_periods_by_requirement(status, feasible_periods)
    if not c2_period in feasible_periods:
        course1.assign_course_period(status, c1_period)
        course2.assign_course_period(status, c2_period)
        return False

    # check if couse2 can be assigned to c1_period
    feasible_periods = bm.Course.populate_set_of_periods()
    feasible_periods = course2.get_feasible_periods_by_requirement(status, feasible_periods)
    if not c1_period in feasible_periods:
        course1.assign_course_period(status, c1_period)
        course2.assign_course_period(status, c2_period)
        return False
    else:
        course1.assign_course_period(status, c1_period)
        course2.assign_course_period(status, c2_period)
        return True
def get_change_of_scoring_for_same_homeRoom_course_swap(status, course1, course2, c1_period, c2_period):
    # teacher penalties
    t1_score_original = get_Teacher_day_score(status, course1, c1_period)
    t1_score_after = get_Teacher_day_score(status, course1, c2_period)
    
    t2_score_original = get_Teacher_day_score(status, course2, c2_period)
    t2_score_after = get_Teacher_day_score(status, course2, c1_period)
    return t1_score_after + t2_score_after - t1_score_original - t2_score_original    
    
def get_Teacher_day_score(status, course, period):
    # get the penalty score of the day
    # period can be the original period or a period of interest for changing
    teacher = course.Teacher
    day = period[0]
    schedule_dict = scoring.sort_schedules_by_day(teacher.schedule_in_tuples)
    day_schedule = schedule_dict[day]
    # schedule already exist
    if (period[0], period[1], course.name) in day_schedule:
        penalty = scoring.get_Teacher_tb_penelty_by_day(teacher, day_schedule)
        return penalty
    else:
        day_schedule.append((period[0], period[1], course.name))
        penalty = scoring.get_Teacher_tb_penelty_by_day(teacher, day_schedule)
        day_schedule.remove((period[0], period[1], course.name))
        return penalty
    
