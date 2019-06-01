# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 10:11:31 2018

@author: zhes
"""
#import solving_zhes_problem1_using_repeated_assignment as solving
import zhes_scheduling_problem
import CourseScheduling as cs
import PostSolution as ps
import random
import pickle

random.seed()



def solving_zhes_with_sequencial_LNS(seed = None, n_iteration = 1000):
        
    random.seed()
    
    subject_set = {'Reading', 'English(extra)', 'Computer', 'Integrative Activities', 'Math', 'Flexible', 'Life', 'Music', 
        'Health', 'Dialect', 'English', 'Science', 'Social', 'Music(extra)', 'Chinese', 'Science(lab)', 'PE', 'Art',
        'English12a', 'English(extra)12a','English12b', 'English(extra)12b', 'English12c', 'English(extra)12c',
        'English34a', 'English(extra)34a','English34b', 'English(extra)34b', 'English34c', 'English(extra)34c',
        'English56a', 'English(extra)56a','English56b', 'English(extra)56b','English56c', 'English(extra)56c'}
    

    best_status = zhes_scheduling_problem.initate_zhes_status()
    
    
    
    def only_keep_subjects(best_status, list_of_subjects):
        for C in best_status.list_of_unassigned_Courses.copy():
            if (C.subject  not in list_of_subjects): #
                best_status.change_unassigned_Course_to_stalled_list(C) 
                
    only_keep_subjects(best_status, ["Science", "Science(lab)"])
    
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
    
    only_keep_subjects(best_status, ['English12a', 'English(extra)12a','English12b', 'English(extra)12b', 'English12c', 'English(extra)12c',
        'English34a', 'English(extra)34a','English34b', 'English(extra)34b', 'English34c', 'English(extra)34c',
        'English56a', 'English(extra)56a','English56b', 'English(extra)56b','English56c', 'English(extra)56c',"English", "English(extra)"])
    
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
    
    only_keep_subjects(best_status, ['Dialect','Social'])
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        print([c.name for c in best_status.list_of_unassigned_Courses])
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
    
    only_keep_subjects(best_status, ["Music", "Music(extra)", 'PE','Art'])
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
       
    
    only_keep_subjects(best_status, subject_set - {'Chinese', 'Math', 'Integrative Activities', 'Flexible', 'Life'})
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        print([c.name for c in best_status.list_of_unassigned_Courses])
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
    
    
    best_status, scoring = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        print([c.name for c in best_status.list_of_unassigned_Courses])
        return best_status, None
    
    print("not assigned: "+ str([C.name for C in best_status.list_of_unassigned_Courses]))

        
    print('Assigned {} out of {} courses'.format(len(best_status.list_of_assigned_Courses + best_status.list_of_fixed_Courses), 
              len(best_status.list_of_Courses) - len(best_status.list_of_stalled_Courses)))
    
    return best_status, score
    
if __name__ == '__main__':
    list_of_solution = []
    list_of_score = []
    
    for i in range(1):
        score = None
        count = 0
        while not (score or count > 20):
            count += 1
            sol, score = solving_zhes_with_sequencial_LNS()
        if sol:
            list_of_solution.append(sol)
            list_of_score.append(score)
            
    ind = list_of_score.index(min(list_of_score))
    best_solution = list_of_solution[ind]
    
    room_dict, teacher_dict = ps.put_solution_in_df(best_solution)
    
    ps.output_data(room_dict, teacher_dict)
    ps.checking_all_requirements(list_of_solution[0])
    
    with open('status.pkl', 'wb') as f:
        pickle.dump(best_solution, f)
        