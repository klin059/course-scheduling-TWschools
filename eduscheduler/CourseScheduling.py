# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:53:30 2018
scheduling module
@author: KML
"""
from . import BaseModel as bm
from . import scoring
import random

def large_neighbourhood_search_with_scoring(status, max_iteration = 300):
    ''' global solution is the solution with the lowest penalty score
    '''
    n_Courses_to_assign = len(status.list_of_unassigned_Courses)
    global_solution = status.make_copy()
    global_score = scoring.get_status_penalty(global_solution)
    
    local_solution = status.make_copy()
    n_samples_remove = int(len(local_solution.list_of_assigned_Courses)/3)
    n_samples_addon = int(len(local_solution.list_of_unassigned_Courses)/3)
    
    iteration = 0
    while not iteration > max_iteration:
        # decide the fraction of courses to be rescheduled
        fraction = 3
        if len(local_solution.list_of_unassigned_Courses) < 10:
            fraction = 1
        n_samples_remove = int(len(local_solution.list_of_assigned_Courses)/3)
        n_samples_addon = int(len(local_solution.list_of_unassigned_Courses)/fraction)
        
        Courses_to_remove = random.sample(local_solution.list_of_assigned_Courses, n_samples_remove)
        Courses_to_add = random.sample(local_solution.list_of_unassigned_Courses, n_samples_addon)
        removed_Courses = []
        # unassign courses
        for course in Courses_to_remove:
            if "same_period" in course.requirements:
                for C in course.requirements["same_period"]:
                    if C.assigned is True:
                        C.unassign_course(local_solution)
                    removed_Courses.append(C)
            else:
                course.unassign_course(local_solution)
                removed_Courses.append(course)
        
        # assign courses
        Courses_to_add = Courses_to_add + removed_Courses
        for course in Courses_to_add:
            feasible_periods = bm.Course.populate_set_of_periods()
            feasible_periods = course.get_feasible_periods_by_requirement(local_solution, feasible_periods) 
            
            # if same_period requirement, get feasible_periods for courses with the same requriement
            course_assigned = False
            if "same_period" in course.requirements:
                for C in course.requirements["same_period"]:
                    # any one of the related course is assigned, skip the course
                    if C.assigned is True:
                        course_assigned = True
                        break
                    feasible_periods = C.get_feasible_periods_by_requirement(local_solution, feasible_periods)
            if feasible_periods == set() or course_assigned:
                continue    
            period = random.sample(feasible_periods, 1)[0]
            if "same_period" in course.requirements:
                for C in course.requirements["same_period"]:
                    C.assign_course_period(local_solution, period)  
            else:
                course.assign_course_period(local_solution, period)
#            # for same_period requirement, need to assign all the relevant courses in the same iteration loop
#            if "same_period" in course.requirements:
##                # assign period to all courses that have this requirement
##                for C in course.requirements["same_period"]:
##                    if C.assigned is True:
##                        continue
##                    else:
##                        C.assign_course_period(local_solution, period)                    
#                                # assign period to all courses that have this requirement
#                for C in course.requirements["same_period"]:
#                    if C.assigned is True:
#                        continue
#                    feasible_periods = C.get_feasible_periods_by_requirement(local_solution, feasible_periods)
#                for C in course.requirements["same_period"]:
#                    C.assign_course_period(local_solution, period)  
#            else:
#                course.assign_course_period(local_solution, period)
                
        # update global solution
        local_score = scoring.get_status_penalty(local_solution)
        if  local_score < global_score:
            global_solution = local_solution.make_copy()
            global_score = local_score
           
        iteration += 1
    n_Courses_to_assign = len(global_solution.list_of_Courses) - len(global_solution.list_of_stalled_Courses) - len(global_solution.list_of_fixed_Courses)
    print('Assigned {} out of {} courses'.format(len(global_solution.list_of_assigned_Courses), str(n_Courses_to_assign)))
    return global_solution, global_score

def sequential_scheduling(status, max_iteration = 300):
    ''' randomly assign course sequentially without removing the courses
    '''
    local_solution = status.make_copy()

    for course in local_solution.list_of_unassigned_Courses:

        local_solution.assert_status()
        feasible_periods = bm.Course.populate_set_of_periods()
        feasible_periods = course.get_feasible_periods_by_requirement(local_solution, feasible_periods) 
        if feasible_periods == set():
            continue
        period = random.sample(feasible_periods, 1)[0]
        # for same_period requirement, need to assign all the relevant courses in the same iteration loop
        if "same_period" in course.requirements:
            # assign period to all courses that have this requirement
#            print("same_period:{}".format([C.name for C in course.requirements["same_period"]]))
            for C in course.requirements["same_period"]:
                if C.assigned is True:
                    continue
                else:
                    C.assign_course_period(local_solution, period)
        else:
            course.assign_course_period(local_solution, period)
    print('inFunc: Assigned {} out of {} courses'.format(len(local_solution.list_of_assigned_Courses + local_solution.list_of_fixed_Courses), 
          len(local_solution.list_of_Courses) - len(local_solution.list_of_stalled_Courses)))
    return local_solution
    
                