# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 09:54:21 2018
Final scheduling problem
@author: KML
"""
import BaseModel as bm

def create_zhes_scheduling_problem_inputs():
    grade_to_nHomeroom_dict = {'G1':7, 'G2':5, 'G3': 5, 'G4':5,'G5':6, 'G6':6}
    grade_to_subject_to_nClass_dict = {
            'G1':{'Chinese':5, 'Math':3, 'Integrative Activities':2, 'Life':5, 'Flexible':2, 'Art':1, 'Music':1, 'Health':1, 'PE':1, 'Dialect':1, 'English':1},
            'G2':{'Chinese':5, 'Math':3, 'Integrative Activities':2, 'Life':5, 'Flexible':2, 'Art':1, 'Music':1, 'Health':1, 'PE':1, 'Dialect':1, 'English':1},
            'G3':{'Chinese':5, 'Math':3, 'Integrative Activities':2, 'Flexible':1, 'Social':3, 'Art':2, 'Music':1, 'Music(extra)':1, 'Health':1, 'PE':2, 
                  'Dialect':1, 'English':1, 'English(extra)':1, 'Computer':1, 'Science':1, 'Science(lab)':2, "Reading":1},
            'G4':{'Chinese':5, 'Math':3, 'Integrative Activities':2, 'Flexible':1, 'Social':3, 'Art':2, 'Music':1, 'Music(extra)':1, 'Health':1, 'PE':2, 
                  'Dialect':1, 'English':1, 'English(extra)':1, 'Computer':1, 'Science':1, 'Science(lab)':2, "Reading":1},
            'G5':{'Chinese':5, 'Math':4, 'Integrative Activities':3, 'Flexible':2, 'Social':3, 'Art':2, 'Music':1, 'Music(extra)':1, 'Health':1, 'PE':2, 
                  'Dialect':1, 'English':1, 'English(extra)':1, 'Computer':1, 'Science':1, 'Science(lab)':2},
            'G6':{'Chinese':5, 'Math':4, 'Integrative Activities':3, 'Flexible':2, 'Social':3, 'Art':2, 'Music':1, 'Music(extra)':1, 'Health':1, 'PE':2,
                  'Dialect':1, 'English':1, 'English(extra)':1, 'Computer':1, 'Science':1, 'Science(lab)':2}
            }
    
    # populate a list of standard courses
    list_of_Courses = bm.Course.populate_list_of_courses(grade_to_subject_to_nClass_dict, grade_to_nHomeroom_dict)
    # delete G5 English, English(extra) and add English5152a, English5152b, English5152c, English5354a, b, c, English5556a, b, c
    for i in [1,2,3,4,5,6]:
        for c in list_of_Courses.copy():
            if c.name == "G5_{}_English_1".format(i):
                list_of_Courses.remove(c)
            elif c.name == "G5_{}_English(extra)_1".format(i):
                list_of_Courses.remove(c)

    
    for homeroom in [1,3,5]:
        # grade, homeroom_number, subject, class_index
        room_no = str(homeroom) + str(homeroom+1)
        course = bm.Course('G5', homeroom, 'English'+room_no+'a',1)
        list_of_Courses.append(course)
        course = bm.Course('G5', homeroom, 'English(extra)'+room_no+'a',1)
        list_of_Courses.append(course)
    for homeroom in [2,4,6]:
        room_no = str(homeroom-1) + str(homeroom)
        course = bm.Course('G5', homeroom, 'English'+room_no+'b',1)
        list_of_Courses.append(course)
        course = bm.Course('G5', homeroom, 'English(extra)'+room_no+'b',1)
        list_of_Courses.append(course)    
    for room_no in ['12','34','56']:
        course = bm.Course('G5',0,'English'+room_no+'c',1)
        list_of_Courses.append(course)
        course = bm.Course('G5',0,'English(extra)'+room_no+'c',1)
        list_of_Courses.append(course)
    
    # rooms
    # room:subjects allowed in the room
    subjectroom_to_subjects_dict = {'English room':['English(extra)'],'Music room 2':['Music', 'Music(extra)'], 'Music room 1':['Music', 'Music(extra)'],
                                  'Science lab (G5)':['Science','Science(lab)'], 'Science lab (G6)':['Science','Science(lab)'], 'Science lab (G3-G4)':['Science(lab)'], 'Sport field-1':['PE'], 'Sport field-2':['PE'], 'Sport field-3':['PE'],
                                  'Sport field-4':['PE'], 'Sport field-5':['PE'], 'Sport field-6':['PE'], 'Computer room': ['Computer'], 'Resource room':['Social']}  #'圖書室':['Reading']
    
    subjects_allowed_in_homeroom = {'G1':['Math', 'Chinese', 'Integrative Activities', 'Social', 'Flexible', 'Art', 'English', 'Health', 'Dialect', 'Reading', 'Life'],
                                    'G2':['Math', 'Chinese', 'Integrative Activities', 'Social', 'Flexible', 'Art', 'English', 'Health', 'Dialect', 'Reading', 'Life'],
                                    'G3':['Math', 'Chinese', 'Integrative Activities', 'Social', 'Flexible', 'Art', 'English', 'Health', 'Dialect', 'Reading', 'Life'],
                                    'G4':['Math', 'Chinese', 'Integrative Activities', 'Social', 'Flexible', 'Art', 'English', 'Health', 'Dialect', 'Reading', 'Life'],
                                    'G5':['Math', 'Chinese', 'Integrative Activities', 'Flexible', 'Art', 'English', 'Health', 'Dialect', 'Reading', 'Life'],
                                    'G6':['Math', 'Chinese', 'Integrative Activities', 'Flexible', 'Art', 'English', 'Health', 'Dialect', 'Reading', 'Life']
                                    }
    list_of_homerooms = bm.Room.populate_list_of_homeroomes(grade_to_nHomeroom_dict, subjects_allowed_in_homeroom)
    list_of_subject_rooms = bm.Room.populate_list_of_subjectrooms(subjectroom_to_subjects_dict)
    list_of_Rooms = list_of_homerooms + list_of_subject_rooms
    # create an arbitary homeroom for joined classes
    G5_0 = bm.Room('G5_0', [], ('G5','0')) #'English12c', 'English(extra)12c','English34c', 'English(extra)34c', 'English56c', 'English(extra)56c'
    list_of_Rooms.append(G5_0)
    
    
    # Teachers
    # subject teachers
    # subject teacher to (grade,subject) tuples
    # only for subject teachers that take a certain subject of all classes of the same grade
    list_of_grade_subject_tuple_dict = {'Teacher 1':[('G1', 'English'), ('G2', 'English')],
                                        'English teacher 1':[('G3', 'English'), ('G3', 'English(extra)')],
                                        'Teacher 2':[('G4', 'English'), ('G4', 'English(extra)')],
                                        'Music teacher 1':[('G1','Music')],
                                        'Music teacher 2':[('G3','Music'), ('G3','Music(extra)'), ('G5','Music'), ('G5','Music(extra)')],
                                        'Music teacher 3':[('G4','Music'), ('G4','Music(extra)')],
                                        'PE teacher 2':[('G2', 'PE'), ('G3', 'PE')],
                                        'PE teacher 3':[('G4', 'PE')],
                                        'Teacher 3':[('G1', 'Dialect'), ('G2', 'Dialect'), ('G5', 'Dialect')],
                                        'Teacher 4':[('G4', 'Science'), ('G4', 'Science(lab)')],
                                        'Computer teacher 1':[('G3','Computer'), ('G4', 'Computer')],
                                        'Computer teacher 2':[('G6', 'Computer')],
                                        'Teacher 5':[('G3', 'Reading'), ('G4', 'Reading')],
                                        'Teacher 6':[('G2', 'Art')]
                                        }
    def populate_teacher_to_list_of_grade_homeroom_subject_tuple(teacher_to_list_of_grade_homeroom_subject_tuple, teacher_name, grade, homeroom_number, subject):
        if not teacher_name in teacher_to_list_of_grade_homeroom_subject_tuple:
            teacher_to_list_of_grade_homeroom_subject_tuple[teacher_name] = []
        teacher_to_list_of_grade_homeroom_subject_tuple[teacher_name].append((grade, homeroom_number, subject))
        return teacher_to_list_of_grade_homeroom_subject_tuple
    
    subjteacher_to_list_of_grade_homeroom_subject_tuple = {}
    for grade, nClasses in grade_to_nHomeroom_dict.items():
        for ind in range(nClasses):
            homeroom_no = ind+1
            for t_name, list_of_tuples in list_of_grade_subject_tuple_dict.items():
                for grade_subject_tuple in list_of_tuples:
                    if grade_subject_tuple[0] == grade:
                        subjteacher_to_list_of_grade_homeroom_subject_tuple = populate_teacher_to_list_of_grade_homeroom_subject_tuple(
                            subjteacher_to_list_of_grade_homeroom_subject_tuple, t_name, grade, homeroom_no, grade_subject_tuple[1])
    
    # homeroom teachers
    homeroom_teacher_grade_to_list_of_subjects_dict = {
            'G1':['Chinese', 'Math', 'Integrative Activities', 'Life', 'Flexible'],
            'G2':['Chinese', 'Math', 'Integrative Activities', 'Life', 'Flexible'],
            'G3':['Chinese', 'Math', 'Integrative Activities', 'Flexible', 'Social', 'Art'],
            'G4':['Chinese', 'Math', 'Integrative Activities', 'Flexible', 'Social', 'Art'],
            'G5':['Chinese', 'Math', 'Integrative Activities', 'Flexible', 'Art'],
            'G6':['Chinese', 'Math', 'Integrative Activities', 'Flexible', 'Art']
                                               }
    
    # name mapping between homeroom and homeroom teacher names
    
    grade_to_hr_teacher_names = {
                'G1':['G1_1_Teacher','G1_2_Teacher','G1_3_Teacher','G1_4_Teacher','G1_5_Teacher','G1_6_Teacher','G1_7_Teacher'],
                'G2':['G2_1_Teacher','G2_2_Teacher','G2_3_Teacher','G2_4_Teacher','G2_5_Teacher'],
                'G3':['G3_1_Teacher','G3_2_Teacher','G3_3_Teacher','G3_4_Teacher','G3_5_Teacher'],
                'G4':['G4_1_Teacher','G4_2_Teacher','G4_3_Teacher','G4_4_Teacher','G4_5_Teacher'],
                'G5':['G5_1_Teacher','G5_2_Teacher','G5_3_Teacher','G5_4_Teacher','G5_5_Teacher','G5_6_Teacher'],
                'G6':['G6_1_Teacher','G6_2_Teacher','G6_3_Teacher','G6_4_Teacher','G6_5_Teacher','G6_6_Teacher']
            }
    
    
    hr_teacher_to_list_of_teaching_tuple = {}
    for grade, nClasses in grade_to_nHomeroom_dict.items():
        for ind in range(nClasses):
            homeroom_no = ind+1
            for subj in homeroom_teacher_grade_to_list_of_subjects_dict[grade]:
                hr_teacher_to_list_of_teaching_tuple = populate_teacher_to_list_of_grade_homeroom_subject_tuple(
                            hr_teacher_to_list_of_teaching_tuple, grade_to_hr_teacher_names[grade][ind], grade, homeroom_no, subj)
        
    list_of_subject_Teachers = bm.SubjectTeacher.populate_list_of_subject_Teachers(subjteacher_to_list_of_grade_homeroom_subject_tuple)
    list_of_homeroom_Teachers = bm.HomeroomTeacher.populate_list_of_homeroom_Teachers(hr_teacher_to_list_of_teaching_tuple)
    
    # manually create "Peter"
    Peter = bm.SubjectTeacher('Peter', [('G5',0,'English12c'), ('G5',0,'English34c'), ('G5',0,'English56c'),
                                 ('G5',0,'English(extra)12c'), ('G5',0,'English(extra)34c'), ('G5',0,'English(extra)56c')])
    list_of_subject_Teachers.append(Peter)
    # remove ('G2',5,Integrative Activities) from G2_5_Teacher
    for T in list_of_homeroom_Teachers:
        if T.name == 'G2_5_Teacher':
            T.list_of_grade_homeroom_subject_tuple.remove(('G2',5,'Integrative Activities'))
    
    # Manually add in rest of the subject teachers 
    
    # if teacher name found in list of subject teacher, add the course tuple to Teacher
    def add_Teacher_to_list(teacher_name, list_of_course_tuples_to_add, list_of_Teachers, tr_type):
        if not type(list_of_course_tuples_to_add) == list:
            raise Exception('list_of_course_tuples_to_add should be of list type')
        for T in list_of_Teachers:
            if T.name == teacher_name:
                # teacher found in the list
                T.list_of_grade_homeroom_subject_tuple += list_of_course_tuples_to_add
                return
        if tr_type == 'homeroom':
            raise Exception("Teacher name not found in the list of Teachers.")
        elif tr_type == 'subject':
            # cannot find the subject teacher in the list, create one
            teacher = bm.SubjectTeacher(teacher_name, list_of_course_tuples_to_add)
            list_of_Teachers.append(teacher)
        else:
            raise Exception("unknown teacher type")
        
    for i in range(5):
        class_ind = i+1
        add_Teacher_to_list("PE teacher 1", [('G5',class_ind,'PE')], list_of_subject_Teachers, 'subject')
        
    add_Teacher_to_list("Music teacher 1", [('G2',i+1,'Music') for i in range(3)], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 7", [('G2',4,'Music'), ('G2',5,'Music')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Music teacher 3", [('G6', 1, 'Music'), ('G6', 3, 'Music'), 
                               ('G6', 4, 'Music'), ('G6', 5, 'Music'), ('G6', 6, 'Music'),
                               ('G6', 1, 'Music(extra)'), ('G6', 3, 'Music(extra)'), 
                               ('G6', 4, 'Music(extra)'), ('G6', 5, 'Music(extra)'), ('G6', 6, 'Music(extra)')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 8", [('G5',6,'PE')], list_of_subject_Teachers, 'subject')    
    add_Teacher_to_list("Teacher 9", [('G6',i,'PE') for i in [1,2,3,4,5]], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("Teacher 8", [('G5',6,'PE')], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("Teacher 9", [('G6',2,'Dialect'), ('G6',3,'Dialect')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 9", [('G6',6,'PE')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 9", [('G4',2,'Dialect')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 10", [('G3',1,'Dialect'),
                               ('G3',2,'Dialect'), ('G3',3,'Dialect'), ('G3',4,'Dialect'),
                               ('G4',1,'Dialect'), ('G4',5,'Dialect'), ('G4',4,'Dialect'), ('G4',3,'Dialect')
                               ], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 11", [('G3',i,'Science') for i in [1,2,3]], list_of_subject_Teachers, 'subject') 
    add_Teacher_to_list("Teacher 11", [('G3',i,'Science(lab)') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 11", [('G3',5,'Dialect')], list_of_subject_Teachers, 'subject')       
    add_Teacher_to_list("Teacher 6", [('G6',i,'Dialect') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("Computer teacher 1", [('G4',2,'Dialect')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 3", [('G6',i,'Dialect') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 4', [('G3',i,'Science') for i in [4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 4', [('G3',i,'Science(lab)') for i in [4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 12', [('G5',i,'Science') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 12', [('G5',i,'Science(lab)') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 13', [('G5',i,'Science') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 13', [('G5',i,'Science(lab)') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 14', [('G6',i,'Science') for i in [1,2,3,4]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 14', [('G6',i,'Science(lab)') for i in [1,2,3,4]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 8', [('G6',i,'Science') for i in [5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 8', [('G6',i,'Science(lab)') for i in [5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 15', [('G5',i,'Social') for i in [1,2,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 16', [('G3',2,'Health'),('G3',4,'Health')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 17', [('G6',i,'Social') for i in [2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 18', [('G1',i,'PE') for i in [6,7]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 18', [('G6',i,'Social') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 18', [('G1',i,'Health') for i in [1,2,3,4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 19', [('G2',i,'Health') for i in [1,2,3,4]], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list('Teacher 19', [('G5',i,'Health') for i in [1,2,3,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 13', [('G5',6,'Health')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 19', [('G6',i,'Health') for i in [1,2,3,4,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 20', [('G5',i,'Computer') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 21', [('G5',i,'Computer') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 22', [('G2',5,'Integrative Activities')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('Teacher 6', [('G1',i,'Art') for i in [2,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("English teacher 1", [('G5', 1, 'English12a'), ('G5', 3, 'English34a')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("English teacher 1", [('G5', 1, 'English(extra)12a'), ('G5', 3, 'English(extra)34a')], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("English teacher 1", [('G5', i, 'English(extra)') for i in [1,2]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("English teacher 1", [('G6', i, 'English') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("English teacher 1", [('G6', i, 'English(extra)') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 2", [('G5', 2, 'English12b'),('G5', 4, 'English34b'), ('G5', 6, 'English56b')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 2", [('G5', 2, 'English(extra)12b'),('G5', 4, 'English(extra)34b'), ('G5', 6, 'English(extra)56b')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 2", [('G6', i, 'English') for i in [4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 2", [('G6', i, 'English(extra)') for i in [4,5]], list_of_subject_Teachers, 'subject')
    
    add_Teacher_to_list("PE teacher 2", [('G1', i, 'PE') for i in [1,2,3,4,5]], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("Teacher 2*", [('G6', i, 'English(extra)') for i in [4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 1", [('G4', i, 'Health') for i in [2,3,4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("Teacher 1", [('G5', i, 'Health') for i in [1,2,3,5]], list_of_subject_Teachers, 'subject')
    
    add_Teacher_to_list("G5_5_Teacher", [('G5', 5, 'English56a')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("G5_5_Teacher", [('G5', 5, 'English(extra)56a')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("G6_6_Teacher", [('G6', 6, 'English')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("G6_6_Teacher", [('G6', 6, 'English(extra)')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("G6_2_Teacher", [('G6', 2, 'Music')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("G6_2_Teacher", [('G6', 2, 'Music(extra)')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G5_3_Teacher', [('G5',3,'Social')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G5_4_Teacher', [('G5',4,'Social')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G6_1_Teacher', [('G6',1,'Social')], list_of_homeroom_Teachers, 'homeroom')
#    add_Teacher_to_list('G1_4_Teacher', [('G1',4,'Health')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G1_7_Teacher', [('G1',7,'Health')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G2_5_Teacher', [('G2',5,'Health')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G3_3_Teacher', [('G3',3,'Health')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G3_5_Teacher', [('G3',5,'Health')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G4_1_Teacher', [('G4',1,'Health')], list_of_homeroom_Teachers, 'homeroom')
#    add_Teacher_to_list('G4_3_Teacher', [('G4',3,'Health')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G5_4_Teacher', [('G5',4,'Health')], list_of_homeroom_Teachers, 'homeroom')
#    add_Teacher_to_list('G6_4_Teacher', [('G6',4,'Health')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G6_5_Teacher', [('G6',5,'Health')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G1_4_Teacher', [('G1',4,'Art')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G1_1_Teacher', [('G1',1,'Art')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G1_3_Teacher', [('G1',3,'Art')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G1_7_Teacher', [('G1',7,'Art')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G3_1_Teacher', [('G3',1,'Health')], list_of_homeroom_Teachers, 'homeroom')
    
    list_of_Teachers = list_of_homeroom_Teachers + list_of_subject_Teachers
    
    # add restricted periods for teachers
    for T in list_of_Teachers:
        if T.name == 'Teacher 9':
            T.restricted_periods += [('Tuesday', i+1) for i in range(7)]
        elif T.name == "Teacher 21":
            T.restricted_periods += [('Wednesday', i+1) for i in range(7)]
        elif T.name == "Teacher 20":
            T.restricted_periods += [('Thursday', i+1) for i in range(7)]
        elif T.name == 'Teacher 16':
            T.restricted_periods += [('Tuesday', i+1) for i in range(7)]
            T.restricted_periods += [('Friday', i+1) for i in range(7)]
        elif T.name == 'Teacher 11':
            T.restricted_periods += [('Tuesday', i+1) for i in range(7)]
            T.restricted_periods += [('Friday', i+1) for i in range(7)]
        elif T.name == 'Teacher 12':
            T.restricted_periods += [('Friday', i+1) for i in range(4)]
        elif T.name == 'Teacher 8':
            T.restricted_periods += [('Tuesday', i) for i in [5,6,7]]
        elif T.name == 'Teacher 8':
            T.restricted_periods += [('Tuesday', i) for i in [5,6,7]]
        elif T.name == 'Music teacher 3':
            T.restricted_periods += [(subj, 1) for subj in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
        elif T.name == 'Music teacher 2':
            T.restricted_periods += [(subj, 1) for subj in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
        elif T.name == 'Computer teacher 1':
            T.restricted_periods += [('Monday', i+1) for i in range(7)]
            T.restricted_periods += [('Thursday', i) for i in [5,6,7]]
        elif T.name == 'English teacher 1':
            T.restricted_periods += [('Wednesday', i+1) for i in range(7)]
            T.restricted_periods += [('Thursday', 1)]
        elif T.name == 'Peter':
            T.restricted_periods += [('Thursday', 1)]
        elif T.name == 'Teacher 2':
            T.restricted_periods += [('Thursday', 1)]
    
    status =  bm.Status(list_of_Courses, list_of_Teachers, list_of_Rooms)
    
    
    # add restricted periods for Rooms

    for R in list_of_Rooms:
        if R.name == 'Music room 1':
            R.restricted_periods += [('Monday', i) for i in [5,6,7]]
            R.allowed_homeroom = [('G1', i+1, 'Music') for i in range(7) ] + [('G2', i+1, 'Music') for i in range(5)] + [('G3', i+1, 'Music') for i in range(5)] +[('G3', i+1, 'Music(extra)') for i in range(5)]+ [('G4', i+1, 'Music') for i in range(3)]+[('G4', i+1, 'Music(extra)') for i in range(3)]
        elif R.name == 'Music room 2':
            R.allowed_homeroom = [('G5', i+1, 'Music') for i in range(6)] + [('G5', i+1, 'Music(extra)') for i in range(6)] + [('G6', i+1, 'Music') for i in range(6)] + [('G6', i+1, 'Music(extra)') for i in range(6)] + [('G4', i, 'Music') for i in [4,5]] + [('G4', i, 'Music(extra)') for i in [4,5]]
        elif R.name == 'Resource room':
            R.allowed_homeroom = [('G6', i+1, 'Social') for i in range(6)]
            R.restricted_periods += [('Monday', i) for i in [5,6,7]]
        elif R.name == 'Science lab (G5)':
            R.allowed_homeroom = [('G5', i+1, 'Science') for i in range(6)]
            R.allowed_homeroom += [('G5', i+1, 'Science(lab)') for i in range(6)]
            R.allowed_homeroom += [('G5', i+1, 'Social') for i in range(3)]
            R.allowed_homeroom += [('G4', 5, 'Science')]
            R.allowed_homeroom += [('G4', 5, 'Science(lab)')]
        elif R.name == 'Science lab (G6)':
            R.allowed_homeroom = [('G6', i+1, 'Science') for i in range(6)]
            R.allowed_homeroom += [('G6', i+1, 'Science(lab)') for i in range(6)]
            R.allowed_homeroom += [('G5', i, 'Social') for i in [4,5,6]]
        elif R.name == 'Science lab (G3-G4)':
            R.restricted_periods += [('Monday', i) for i in [5,6,7]]
            R.allowed_homeroom = [('G3', i+1, 'Science') for i in range(5)]
            R.allowed_homeroom += [('G3', i+1, 'Science(lab)') for i in range(5)]
            R.allowed_homeroom += [('G4', i+1, 'Science') for i in range(4)]
            R.allowed_homeroom += [('G4', i+1, 'Science(lab)') for i in range(4)]
        elif R.name == 'Sport field-1':
            R.allowed_homeroom = [('G1', i+1, 'PE') for i in range(7)]
        elif R.name == 'Sport field-2':
            R.allowed_homeroom = [('G2', i+1, 'PE') for i in range(5)]
        elif R.name == 'Sport field-3':
            R.allowed_homeroom = [('G3', i+1, 'PE') for i in range(5)]
        elif R.name == 'Sport field-4':
            R.allowed_homeroom = [('G4', i+1, 'PE') for i in range(5)]
        elif R.name == 'Sport field-5':
            R.allowed_homeroom = [('G5', i+1, 'PE') for i in range(6)]
        elif R.name == 'Sport field-6':
            R.allowed_homeroom = [('G6', i+1, 'PE') for i in range(6)]
    
    
    english_room = bm.Room.get_Room_by_name(status, 'English room')
    english_room.list_of_subject += ['English12c', 'English(extra)12c', 'English34c', 
                                     'English(extra)34c', 'English56c','English(extra)56c']
    G5_1 = bm.Room.get_Room_by_name(status, 'G5_1')
    G5_1.list_of_subject += ['English12a', 'English(extra)12a']
    G5_2 = bm.Room.get_Room_by_name(status, 'G5_2')
    G5_2.list_of_subject += ['English12b', 'English(extra)12b']
    G5_3 = bm.Room.get_Room_by_name(status, 'G5_3')
    G5_3.list_of_subject += ['English34a', 'English(extra)34a']
    G5_4 = bm.Room.get_Room_by_name(status, 'G5_4')
    G5_4.list_of_subject += ['English34b', 'English(extra)34b']
    G5_5 = bm.Room.get_Room_by_name(status, 'G5_5')
    G5_5.list_of_subject += ['English56a', 'English(extra)56a']
    G5_6 = bm.Room.get_Room_by_name(status, 'G5_6')
    G5_6.list_of_subject += ['English56b', 'English(extra)56b']
    # note should only populate room_to_course_tuples after all allowed_homeroom are set
    status.populate_course_to_teacher_tuples()
    status.populate_room_to_course_tuples()
    # same_period requirements
    
    
    # add not_same_day requirements
    for grade in grade_to_nHomeroom_dict:
        for ind in range(grade_to_nHomeroom_dict[grade]):
            hr = ind + 1
            for subject in grade_to_subject_to_nClass_dict[grade]:
                if (subject not in ['Art', 'Science(lab)', 'Life','Chinese', 'Math', 'Integrative Activities', 'Flexible']) and (grade_to_subject_to_nClass_dict[grade][subject] > 1): 
                    course_names_for_same_subject_and_same_hr = []
                    for class_ind in range(grade_to_subject_to_nClass_dict[grade][subject]):
                        course_names_for_same_subject_and_same_hr.append("_".join([grade, str(hr), subject, str(class_ind+1)]))
    #                print(course_names_for_same_subject_and_same_hr)
                    bm.Course.add_requirements(status, "not_same_day", course_names_for_same_subject_and_same_hr)

    for grade in ['G3', 'G4', 'G5', 'G6']:
        nHomeroom = grade_to_nHomeroom_dict[grade]
        for ind in range(nHomeroom):
            class_ind = ind+1
            bm.Course.add_requirements(status, 'not_same_day', ['_'.join([grade, str(class_ind), 'Science', '1']), '_'.join([grade, str(class_ind), 'Science(lab)', '1'])])
            bm.Course.add_requirements(status, 'not_same_day', ['_'.join([grade, str(class_ind), 'Science', '1']), '_'.join([grade, str(class_ind), 'Science(lab)', '2'])])
#            print('_'.join([grade, str(class_ind), 'Science', '1']))
            bm.Course.add_requirements(status, 'not_same_day', ['_'.join([grade, str(class_ind), 'Music', '1']), '_'.join([grade, str(class_ind), 'Music(extra)', '1'])])

    # add consecutive and two days apart requirements
    for grade in ['G3','G4','G5','G6']:
        for ind in range(grade_to_nHomeroom_dict[grade]):
            hr = ind + 1
            for subject in grade_to_subject_to_nClass_dict[grade]:
                if subject in ['Science(lab)']:
                    consecutive_courses = []
                    for class_ind in range(grade_to_subject_to_nClass_dict[grade][subject]):
                        consecutive_courses.append("_".join([grade, str(hr), subject, str(class_ind+1)]))
    #                print(consecutive_courses)
                    bm.Course.add_requirements(status, "consecutive", consecutive_courses)
    
    # add two days apart requirements
    for grade in ['G3','G4','G6']:
        for ind in range(grade_to_nHomeroom_dict[grade]):
            hr = ind + 1
            bm.Course.add_requirements(status, "two_days_apart", ["_".join([grade, str(hr), 'English', str(1)]), "_".join([grade, str(hr), 'English(extra)', str(1)])])           
    # need two days apart requirements for 'G5_1_English12a_1', 'G5_1_English(extra)12a_1' and so on
    bm.Course.add_requirements(status, "two_days_apart", ['G5_0_English12c_1','G5_0_English(extra)12c_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_1_English12a_1','G5_1_English(extra)12a_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_2_English12b_1','G5_2_English(extra)12b_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_0_English34c_1','G5_0_English(extra)34c_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_3_English34a_1','G5_3_English(extra)34a_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_4_English34b_1','G5_4_English(extra)34b_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_0_English56c_1','G5_0_English(extra)56c_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_5_English56a_1','G5_5_English(extra)56a_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_6_English56b_1','G5_6_English(extra)56b_1'])    
    # add same_period constraints for 'G5_1_English12a_1', 'G5_2_English12b_1', 'G5_0_English12c_1'
    bm.Course.add_requirements(status, 'same_period', ['G5_1_English12a_1','G5_2_English12b_1','G5_0_English12c_1',])
    bm.Course.add_requirements(status, 'same_period', ['G5_1_English(extra)12a_1','G5_2_English(extra)12b_1','G5_0_English(extra)12c_1',])
    bm.Course.add_requirements(status, 'same_period', ['G5_3_English34a_1', 'G5_4_English34b_1', 'G5_0_English34c_1'])
    bm.Course.add_requirements(status, 'same_period', ['G5_3_English(extra)34a_1', 'G5_4_English(extra)34b_1', 'G5_0_English(extra)34c_1'])
    bm.Course.add_requirements(status, 'same_period', ['G5_5_English56a_1', 'G5_6_English56b_1', 'G5_0_English56c_1'])
    bm.Course.add_requirements(status, 'same_period', ['G5_5_English(extra)56a_1', 'G5_6_English(extra)56b_1', 'G5_0_English(extra)56c_1'])
    
    return status
    
def initate_zhes_status():
    status = create_zhes_scheduling_problem_inputs()
#    n_courses = len(status.list_of_Courses)
    # set 週五第一節Flexible
    flex_subject_period = {("Friday", 1)}
    for course in status.list_of_Courses:
        if (course.subject == "Flexible") and (course.class_index == 1):
            feasible_periods = course.pick_Teacher_Room_and_get_feasible_periods(status, flex_subject_period)
            if feasible_periods == set():
                print('feasible period == None')
            course.assign_course_period(status, list(feasible_periods)[0])
            # course.assign_course_period(status, period)
    # manually assign teacher, rooms and period for some of the courses
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G6_2_Music_1', ('Monday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G6_2_Music(extra)_1', ('Thursday', 1))

    # manually assign 資源班 
    #B1
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G1_2_Integrative Activities_1', ('Friday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G3_5_Integrative Activities_1', ('Friday', 3)) 
    #B2
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G4_4_Integrative Activities_1', ('Friday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G5_3_Integrative Activities_1', ('Friday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G5_2_Integrative Activities_1', ('Friday', 4))
    #B3
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_2_Integrative Activities_1', ('Thursday', 5))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_4_Integrative Activities_1', ('Thursday', 5))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_6_Integrative Activities_1', ('Thursday', 5))
    #B4
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_1_Integrative Activities_1', ('Thursday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_2_Integrative Activities_1', ('Thursday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_4_Integrative Activities_1', ('Thursday', 4))
    #B5
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Math_1', ('Tuesday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_Math_1', ('Tuesday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Math_2', ('Wednesday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_Math_2', ('Wednesday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Math_3', ('Thursday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_Math_3', ('Thursday', 1))
    #B6
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_Math_1', ('Tuesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_Math_1', ('Tuesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_Math_2', ('Wednesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_Math_2', ('Wednesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_Math_3', ('Thursday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_Math_3', ('Thursday', 2))
    #B社
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_1_Integrative Activities_2', ('Tuesday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_Integrative Activities_1', ('Tuesday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G5_2_Integrative Activities_2', ('Tuesday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_4_Integrative Activities_2', ('Tuesday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Integrative Activities_1', ('Tuesday', 7))
    # A1
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_Chinese_1', ('Monday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_Chinese_2', ('Wednesday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_Chinese_3', ('Thursday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_Chinese_4', ('Friday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_Chinese_1', ('Monday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_Chinese_2', ('Wednesday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_Chinese_3', ('Thursday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_Chinese_4', ('Friday', 3))
    # A2
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Chinese_1', ('Monday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Chinese_2', ('Tuesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Chinese_3', ('Wednesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Chinese_4', ('Thursday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_Chinese_5', ('Friday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_Chinese_1', ('Monday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_Chinese_2', ('Tuesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_Chinese_3', ('Wednesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_Chinese_4', ('Thursday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_Chinese_5', ('Friday', 2))
    # A3
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_1_Integrative Activities_2', ('Tuesday', 5))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_2_Integrative Activities_2', ('Tuesday', 5))
    # A4
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G1_2_Integrative Activities_2', ('Tuesday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_5_Integrative Activities_2', ('Tuesday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_4_Integrative Activities_2', ('Tuesday', 4))
    # A5
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_4_Integrative Activities_2', ('Thursday', 5))
#    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_2_Integrative Activities_1', ('Thursday', 5))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_Integrative Activities_1', ('Thursday', 5))
    # A6
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G5_2_Integrative Activities_3', ('Friday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G5_3_Integrative Activities_2', ('Friday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_4_Integrative Activities_3', ('Friday', 7))
    
    # 特別綁課
    bm.Course.add_requirements(status, "same_period", ['G3_4_Dialect_1', 'G3_5_Dialect_1', 'G4_2_Dialect_1'])
    bm.Course.add_requirements(status, "same_period", ['G4_4_Dialect_1', 'G5_3_Dialect_1'])
        
    # 特別配課
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_4_Music_1', ('Friday', 2))  #Teacher 7
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_5_Music_1', ('Friday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_5_Integrative Activities_1', ('Monday', 1))  #Teacher 22
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_5_Integrative Activities_2', ('Monday', 2))
    
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_4_Dialect_1', ('Monday', 4))  # 綁課
        
    # change these courses to fixed list
    status.fix_assigned_Courses()
    
    for course in status.list_of_Courses:
        course.pick_room_assignment(status)
        course.pick_teacher_assignment(status)
    
    return status
    
def check_timetable_correctness(status):
    pass

if __name__ == '__main__':
#    status = create_zhes_scheduling_problem_inputs()
    status = initate_zhes_status()

