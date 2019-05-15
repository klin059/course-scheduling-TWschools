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



def solving_zhes_with_sequencial_LNS(seed = None, n_iteration = 2000):
        
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
                
    only_keep_subjects(best_status, ["自然", "自然實驗"])
    
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
    
    only_keep_subjects(best_status, ['英語12a', '彈性英語12a','英語12b', '彈性英語12b', '英語12c', '彈性英語12c',
        '英語34a', '彈性英語34a','英語34b', '彈性英語34b', '英語34c', '彈性英語34c',
        '英語56a', '彈性英語56a','英語56b', '彈性英語56b','英語56c', '彈性英語56c',"英語", "彈性英語"])
    
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
    
    only_keep_subjects(best_status, ['閩南語','社會'])
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        print([c.name for c in best_status.list_of_unassigned_Courses])
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
    
    only_keep_subjects(best_status, ["音樂", "彈性音樂", '體育','美勞'])
    best_status , score = cs.large_neighbourhood_search_with_scoring(best_status, max_iteration = n_iteration)
    if not best_status.list_of_unassigned_Courses == []:
        return best_status, None
    best_status.fix_assigned_Courses()
    best_status.free_stalled_Courses()
       
    
    only_keep_subjects(best_status, subject_set - {'國', '數', '綜合', '彈性', '生活'})
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
        