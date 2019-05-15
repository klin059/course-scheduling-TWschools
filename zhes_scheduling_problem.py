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
    
    # populate a list of standard courses
    list_of_Courses = bm.Course.populate_list_of_courses(grade_to_subject_to_nClass_dict, grade_to_nHomeroom_dict)
    # delete G5 英語, 彈性英語 and add 英語5152a, 英語5152b, 英語5152c, 英語5354a, b, c, 英語5556a, b, c
    for i in [1,2,3,4,5,6]:
        for c in list_of_Courses.copy():
            if c.name == "G5_{}_英語_1".format(i):
                list_of_Courses.remove(c)
            elif c.name == "G5_{}_彈性英語_1".format(i):
                list_of_Courses.remove(c)

    
    for homeroom in [1,3,5]:
        # grade, homeroom_number, subject, class_index
        room_no = str(homeroom) + str(homeroom+1)
        course = bm.Course('G5', homeroom, '英語'+room_no+'a',1)
        list_of_Courses.append(course)
        course = bm.Course('G5', homeroom, '彈性英語'+room_no+'a',1)
        list_of_Courses.append(course)
    for homeroom in [2,4,6]:
        room_no = str(homeroom-1) + str(homeroom)
        course = bm.Course('G5', homeroom, '英語'+room_no+'b',1)
        list_of_Courses.append(course)
        course = bm.Course('G5', homeroom, '彈性英語'+room_no+'b',1)
        list_of_Courses.append(course)    
    for room_no in ['12','34','56']:
        course = bm.Course('G5',0,'英語'+room_no+'c',1)
        list_of_Courses.append(course)
        course = bm.Course('G5',0,'彈性英語'+room_no+'c',1)
        list_of_Courses.append(course)
    
    # add in additional courses manually - 課照，族噢，客語，資源班
#    print("need to add in additional courses manually - 課照，族噢，客語，資源班")
    
    # rooms
    # room:subjects allowed in the room
    subjectroom_to_subjects_dict = {'英語教室':['彈性英語'],'音樂教室(高)':['音樂', '彈性音樂'], '音樂教室(中)':['音樂', '彈性音樂'],
                                  '自然教室(五)':['自然','自然實驗'], '自然教室(六)':['自然','自然實驗'], '自然教室(中)':['自然實驗'], '操場-1':['體育'], '操場-2':['體育'], '操場-3':['體育'],
                                  '操場-4':['體育'], '操場-5':['體育'], '操場-6':['體育'], '電腦教室': ['電腦'], '專科教室':['社會']}  #'圖書室':['閱讀']
    
    subjects_allowed_in_homeroom = {'G1':['數', '國', '綜合', '社會', '彈性', '美勞', '英語', '健康', '閩南語', '閱讀', '生活'],
                                    'G2':['數', '國', '綜合', '社會', '彈性', '美勞', '英語', '健康', '閩南語', '閱讀', '生活'],
                                    'G3':['數', '國', '綜合', '社會', '彈性', '美勞', '英語', '健康', '閩南語', '閱讀', '生活'],
                                    'G4':['數', '國', '綜合', '社會', '彈性', '美勞', '英語', '健康', '閩南語', '閱讀', '生活'],
                                    'G5':['數', '國', '綜合', '彈性', '美勞', '英語', '健康', '閩南語', '閱讀', '生活'],
                                    'G6':['數', '國', '綜合', '彈性', '美勞', '英語', '健康', '閩南語', '閱讀', '生活'],
                                    }
    list_of_homerooms = bm.Room.populate_list_of_homeroomes(grade_to_nHomeroom_dict, subjects_allowed_in_homeroom)
    list_of_subject_rooms = bm.Room.populate_list_of_subjectrooms(subjectroom_to_subjects_dict)
    list_of_Rooms = list_of_homerooms + list_of_subject_rooms
    # create an arbitary homeroom for joined classes
    G5_0 = bm.Room('G5_0', [], ('G5','0')) #'英語12c', '彈性英語12c','英語34c', '彈性英語34c', '英語56c', '彈性英語56c'
    list_of_Rooms.append(G5_0)
    
    
    # Teachers
    # subject teachers
    # subject teacher to (grade,subject) tuples
    # only for subject teachers that take a certain subject of all classes of the same grade
    list_of_grade_subject_tuple_dict = {'代理深藍':[('G1', '英語'), ('G2', '英語')],
                                        '玉梅':[('G3', '英語'), ('G3', '彈性英語')],
                                        '代理綠':[('G4', '英語'), ('G4', '彈性英語')],
                                        '英芳':[('G1','音樂')],
                                        '玳儀':[('G3','音樂'), ('G3','彈性音樂'), ('G5','音樂'), ('G5','彈性音樂')],
                                        '依萍':[('G4','音樂'), ('G4','彈性音樂')],
                                        '梁雋':[('G2', '體育'), ('G3', '體育')],
                                        '石龍':[('G4', '體育')],
                                        '代理墨綠':[('G1', '閩南語'), ('G2', '閩南語'), ('G5', '閩南語')],
                                        '代理淺藍':[('G4', '自然'), ('G4', '自然實驗')],
                                        '銘法':[('G3','電腦'), ('G4', '電腦')],
                                        '智瑋':[('G6', '電腦')],
                                        '佩芬':[('G3', '閱讀'), ('G4', '閱讀')],
                                        '錦瑛':[('G2', '美勞')]
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
            'G1':['國', '數', '綜合', '生活', '彈性'],
            'G2':['國', '數', '綜合', '生活', '彈性'],
            'G3':['國', '數', '綜合', '彈性', '社會', '美勞'],
            'G4':['國', '數', '綜合', '彈性', '社會', '美勞'],
            'G5':['國', '數', '綜合', '彈性', '美勞'],
            'G6':['國', '數', '綜合', '彈性', '美勞']
                                               }
    
    # name mapping between homeroom and homeroom teacher names
    
    grade_to_hr_teacher_names = {
                'G1':['嘉珮','貞琇','G1玲宜','文文','代理G15','鴻銀','淑萍'],
                'G2':['琦琳','麗雯','惠玲','瑞桃','淑玫'],
                'G3':['師岑','代理G32','玉菁','代理G34','淑閔'],
                'G4':['翎君','代理G42','美而','代理G44','潔誼'],
                'G5':['容蘋','勝堯','玲宜','純惠','書瑋','代理G56'],
                'G6':['佩紋','瓊瑤','茜茹','梅雪','丹絹','聖懿']
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
    Peter = bm.SubjectTeacher('Peter', [('G5',0,'英語12c'), ('G5',0,'英語34c'), ('G5',0,'英語56c'),
                                 ('G5',0,'彈性英語12c'), ('G5',0,'彈性英語34c'), ('G5',0,'彈性英語56c')])
    list_of_subject_Teachers.append(Peter)
    # remove ('G2',5,綜合) from 淑玫
    for T in list_of_homeroom_Teachers:
        if T.name == '淑玫':
            T.list_of_grade_homeroom_subject_tuple.remove(('G2',5,'綜合'))
    
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
        add_Teacher_to_list("振書", [('G5',class_ind,'體育')], list_of_subject_Teachers, 'subject')
        
    add_Teacher_to_list("英芳", [('G2',i+1,'音樂') for i in range(3)], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("佳綾", [('G2',4,'音樂'), ('G2',5,'音樂')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("依萍", [('G6', 1, '音樂'), ('G6', 3, '音樂'), 
                               ('G6', 4, '音樂'), ('G6', 5, '音樂'), ('G6', 6, '音樂'),
                               ('G6', 1, '彈性音樂'), ('G6', 3, '彈性音樂'), 
                               ('G6', 4, '彈性音樂'), ('G6', 5, '彈性音樂'), ('G6', 6, '彈性音樂')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("志榮", [('G5',6,'體育')], list_of_subject_Teachers, 'subject')    
    add_Teacher_to_list("雅文", [('G6',i,'體育') for i in [1,2,3,4,5]], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("志榮", [('G5',6,'體育')], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("雅文", [('G6',2,'閩南語'), ('G6',3,'閩南語')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("雅文", [('G6',6,'體育')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("雅文", [('G4',2,'閩南語')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("憲良", [('G3',1,'閩南語'),
                               ('G3',2,'閩南語'), ('G3',3,'閩南語'), ('G3',4,'閩南語'),
                               ('G4',1,'閩南語'), ('G4',5,'閩南語'), ('G4',4,'閩南語'), ('G4',3,'閩南語')
                               ], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("素芬", [('G3',i,'自然') for i in [1,2,3]], list_of_subject_Teachers, 'subject') 
    add_Teacher_to_list("素芬", [('G3',i,'自然實驗') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("素芬", [('G3',5,'閩南語')], list_of_subject_Teachers, 'subject')       
    add_Teacher_to_list("錦瑛", [('G6',i,'閩南語') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("銘法", [('G4',2,'閩南語')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("代理墨綠", [('G6',i,'閩南語') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('代理淺藍', [('G3',i,'自然') for i in [4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('代理淺藍', [('G3',i,'自然實驗') for i in [4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('大君', [('G5',i,'自然') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('大君', [('G5',i,'自然實驗') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('秀玲', [('G5',i,'自然') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('秀玲', [('G5',i,'自然實驗') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('芝蘭', [('G6',i,'自然') for i in [1,2,3,4]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('芝蘭', [('G6',i,'自然實驗') for i in [1,2,3,4]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('志榮', [('G6',i,'自然') for i in [5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('志榮', [('G6',i,'自然實驗') for i in [5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('靜宜', [('G5',i,'社會') for i in [1,2,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('靖桂', [('G3',2,'健康'),('G3',4,'健康')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('俐均', [('G6',i,'社會') for i in [2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('鐘點紫', [('G1',i,'體育') for i in [6,7]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('鐘點紫', [('G6',i,'社會') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('鐘點紫', [('G1',i,'健康') for i in [1,2,3,4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('小君', [('G2',i,'健康') for i in [1,2,3,4]], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list('小君', [('G5',i,'健康') for i in [1,2,3,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('秀玲', [('G5',6,'健康')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('小君', [('G6',i,'健康') for i in [1,2,3,4,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('孝元', [('G5',i,'電腦') for i in [4,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('永林', [('G5',i,'電腦') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('旭政', [('G2',5,'綜合')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list('錦瑛', [('G1',i,'美勞') for i in [2,5,6]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("玉梅", [('G5', 1, '英語12a'), ('G5', 3, '英語34a')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("玉梅", [('G5', 1, '彈性英語12a'), ('G5', 3, '彈性英語34a')], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("玉梅", [('G5', i, '彈性英語') for i in [1,2]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("玉梅", [('G6', i, '英語') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("玉梅", [('G6', i, '彈性英語') for i in [1,2,3]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("代理綠", [('G5', 2, '英語12b'),('G5', 4, '英語34b'), ('G5', 6, '英語56b')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("代理綠", [('G5', 2, '彈性英語12b'),('G5', 4, '彈性英語34b'), ('G5', 6, '彈性英語56b')], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("代理綠", [('G6', i, '英語') for i in [4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("代理綠", [('G6', i, '彈性英語') for i in [4,5]], list_of_subject_Teachers, 'subject')
    
    add_Teacher_to_list("梁雋", [('G1', i, '體育') for i in [1,2,3,4,5]], list_of_subject_Teachers, 'subject')
#    add_Teacher_to_list("代理綠*", [('G6', i, '彈性英語') for i in [4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("代理深藍", [('G4', i, '健康') for i in [2,3,4,5]], list_of_subject_Teachers, 'subject')
    add_Teacher_to_list("代理深藍", [('G5', i, '健康') for i in [1,2,3,5]], list_of_subject_Teachers, 'subject')
    
    add_Teacher_to_list("書瑋", [('G5', 5, '英語56a')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("書瑋", [('G5', 5, '彈性英語56a')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("聖懿", [('G6', 6, '英語')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("聖懿", [('G6', 6, '彈性英語')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("瓊瑤", [('G6', 2, '音樂')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list("瓊瑤", [('G6', 2, '彈性音樂')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('玲宜', [('G5',3,'社會')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('純惠', [('G5',4,'社會')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('佩紋', [('G6',1,'社會')], list_of_homeroom_Teachers, 'homeroom')
#    add_Teacher_to_list('文文', [('G1',4,'健康')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('淑萍', [('G1',7,'健康')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('淑玫', [('G2',5,'健康')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('玉菁', [('G3',3,'健康')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('淑閔', [('G3',5,'健康')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('翎君', [('G4',1,'健康')], list_of_homeroom_Teachers, 'homeroom')
#    add_Teacher_to_list('美而', [('G4',3,'健康')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('純惠', [('G5',4,'健康')], list_of_homeroom_Teachers, 'homeroom')
#    add_Teacher_to_list('梅雪', [('G6',4,'健康')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('丹絹', [('G6',5,'健康')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('文文', [('G1',4,'美勞')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('嘉珮', [('G1',1,'美勞')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('G1玲宜', [('G1',3,'美勞')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('淑萍', [('G1',7,'美勞')], list_of_homeroom_Teachers, 'homeroom')
    add_Teacher_to_list('師岑', [('G3',1,'健康')], list_of_homeroom_Teachers, 'homeroom')
    
    list_of_Teachers = list_of_homeroom_Teachers + list_of_subject_Teachers
    
    # add restricted periods for teachers
    for T in list_of_Teachers:
        if T.name == '雅文':
            T.restricted_periods += [('Tuesday', i+1) for i in range(7)]
        elif T.name == "永林":
            T.restricted_periods += [('Wednesday', i+1) for i in range(7)]
        elif T.name == "孝元":
            T.restricted_periods += [('Thursday', i+1) for i in range(7)]
        elif T.name == '靖桂':
            T.restricted_periods += [('Tuesday', i+1) for i in range(7)]
            T.restricted_periods += [('Friday', i+1) for i in range(7)]
        elif T.name == '素芬':
            T.restricted_periods += [('Tuesday', i+1) for i in range(7)]
            T.restricted_periods += [('Friday', i+1) for i in range(7)]
        elif T.name == '大君':
            T.restricted_periods += [('Friday', i+1) for i in range(4)]
        elif T.name == '志榮':
            T.restricted_periods += [('Tuesday', i) for i in [5,6,7]]
        elif T.name == '志榮':
            T.restricted_periods += [('Tuesday', i) for i in [5,6,7]]
        elif T.name == '依萍':
            T.restricted_periods += [(subj, 1) for subj in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
        elif T.name == '玳儀':
            T.restricted_periods += [(subj, 1) for subj in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
        elif T.name == '銘法':
            T.restricted_periods += [('Monday', i+1) for i in range(7)]
            T.restricted_periods += [('Thursday', i) for i in [5,6,7]]
        elif T.name == '玉梅':
            T.restricted_periods += [('Wednesday', i+1) for i in range(7)]
            T.restricted_periods += [('Thursday', 1)]
        elif T.name == 'Peter':
            T.restricted_periods += [('Thursday', 1)]
        elif T.name == '代理綠':
            T.restricted_periods += [('Thursday', 1)]
    
    status =  bm.Status(list_of_Courses, list_of_Teachers, list_of_Rooms)
    
    
    # add restricted periods for Rooms

    for R in list_of_Rooms:
        if R.name == '音樂教室(中)':
            R.restricted_periods += [('Monday', i) for i in [5,6,7]]
            R.allowed_homeroom = [('G1', i+1, '音樂') for i in range(7) ] + [('G2', i+1, '音樂') for i in range(5)] + [('G3', i+1, '音樂') for i in range(5)] +[('G3', i+1, '彈性音樂') for i in range(5)]+ [('G4', i+1, '音樂') for i in range(3)]+[('G4', i+1, '彈性音樂') for i in range(3)]
        elif R.name == '音樂教室(高)':
            R.allowed_homeroom = [('G5', i+1, '音樂') for i in range(6)] + [('G5', i+1, '彈性音樂') for i in range(6)] + [('G6', i+1, '音樂') for i in range(6)] + [('G6', i+1, '彈性音樂') for i in range(6)] + [('G4', i, '音樂') for i in [4,5]] + [('G4', i, '彈性音樂') for i in [4,5]]
        elif R.name == '專科教室':
            R.allowed_homeroom = [('G6', i+1, '社會') for i in range(6)]
            R.restricted_periods += [('Monday', i) for i in [5,6,7]]
        elif R.name == '自然教室(五)':
            R.allowed_homeroom = [('G5', i+1, '自然') for i in range(6)]
            R.allowed_homeroom += [('G5', i+1, '自然實驗') for i in range(6)]
            R.allowed_homeroom += [('G5', i+1, '社會') for i in range(3)]
            R.allowed_homeroom += [('G4', 5, '自然')]
            R.allowed_homeroom += [('G4', 5, '自然實驗')]
        elif R.name == '自然教室(六)':
            R.allowed_homeroom = [('G6', i+1, '自然') for i in range(6)]
            R.allowed_homeroom += [('G6', i+1, '自然實驗') for i in range(6)]
            R.allowed_homeroom += [('G5', i, '社會') for i in [4,5,6]]
        elif R.name == '自然教室(中)':
            R.restricted_periods += [('Monday', i) for i in [5,6,7]]
            R.allowed_homeroom = [('G3', i+1, '自然') for i in range(5)]
            R.allowed_homeroom += [('G3', i+1, '自然實驗') for i in range(5)]
            R.allowed_homeroom += [('G4', i+1, '自然') for i in range(4)]
            R.allowed_homeroom += [('G4', i+1, '自然實驗') for i in range(4)]
        elif R.name == '操場-1':
            R.allowed_homeroom = [('G1', i+1, '體育') for i in range(7)]
        elif R.name == '操場-2':
            R.allowed_homeroom = [('G2', i+1, '體育') for i in range(5)]
        elif R.name == '操場-3':
            R.allowed_homeroom = [('G3', i+1, '體育') for i in range(5)]
        elif R.name == '操場-4':
            R.allowed_homeroom = [('G4', i+1, '體育') for i in range(5)]
        elif R.name == '操場-5':
            R.allowed_homeroom = [('G5', i+1, '體育') for i in range(6)]
        elif R.name == '操場-6':
            R.allowed_homeroom = [('G6', i+1, '體育') for i in range(6)]
    
    
    english_room = bm.Room.get_Room_by_name(status, '英語教室')
    english_room.list_of_subject += ['英語12c', '彈性英語12c', '英語34c', 
                                     '彈性英語34c', '英語56c','彈性英語56c']
    G5_1 = bm.Room.get_Room_by_name(status, 'G5_1')
    G5_1.list_of_subject += ['英語12a', '彈性英語12a']
    G5_2 = bm.Room.get_Room_by_name(status, 'G5_2')
    G5_2.list_of_subject += ['英語12b', '彈性英語12b']
    G5_3 = bm.Room.get_Room_by_name(status, 'G5_3')
    G5_3.list_of_subject += ['英語34a', '彈性英語34a']
    G5_4 = bm.Room.get_Room_by_name(status, 'G5_4')
    G5_4.list_of_subject += ['英語34b', '彈性英語34b']
    G5_5 = bm.Room.get_Room_by_name(status, 'G5_5')
    G5_5.list_of_subject += ['英語56a', '彈性英語56a']
    G5_6 = bm.Room.get_Room_by_name(status, 'G5_6')
    G5_6.list_of_subject += ['英語56b', '彈性英語56b']
    # note should only populate room_to_course_tuples after all allowed_homeroom are set
    status.populate_course_to_teacher_tuples()
    status.populate_room_to_course_tuples()
    # same_period requirements
    
    
    # add not_same_day requirements
    for grade in grade_to_nHomeroom_dict:
        for ind in range(grade_to_nHomeroom_dict[grade]):
            hr = ind + 1
            for subject in grade_to_subject_to_nClass_dict[grade]:
                if (subject not in ['美勞', '自然實驗', '生活','國', '數', '綜合', '彈性']) and (grade_to_subject_to_nClass_dict[grade][subject] > 1): 
                    course_names_for_same_subject_and_same_hr = []
                    for class_ind in range(grade_to_subject_to_nClass_dict[grade][subject]):
                        course_names_for_same_subject_and_same_hr.append("_".join([grade, str(hr), subject, str(class_ind+1)]))
    #                print(course_names_for_same_subject_and_same_hr)
                    bm.Course.add_requirements(status, "not_same_day", course_names_for_same_subject_and_same_hr)

    for grade in ['G3', 'G4', 'G5', 'G6']:
        nHomeroom = grade_to_nHomeroom_dict[grade]
        for ind in range(nHomeroom):
            class_ind = ind+1
            bm.Course.add_requirements(status, 'not_same_day', ['_'.join([grade, str(class_ind), '自然', '1']), '_'.join([grade, str(class_ind), '自然實驗', '1'])])
            bm.Course.add_requirements(status, 'not_same_day', ['_'.join([grade, str(class_ind), '自然', '1']), '_'.join([grade, str(class_ind), '自然實驗', '2'])])
#            print('_'.join([grade, str(class_ind), '自然', '1']))
            bm.Course.add_requirements(status, 'not_same_day', ['_'.join([grade, str(class_ind), '音樂', '1']), '_'.join([grade, str(class_ind), '彈性音樂', '1'])])

    # add consecutive and two days apart requirements
    for grade in ['G3','G4','G5','G6']:
        for ind in range(grade_to_nHomeroom_dict[grade]):
            hr = ind + 1
            for subject in grade_to_subject_to_nClass_dict[grade]:
                if subject in ['自然實驗']:
                    consecutive_courses = []
                    for class_ind in range(grade_to_subject_to_nClass_dict[grade][subject]):
                        consecutive_courses.append("_".join([grade, str(hr), subject, str(class_ind+1)]))
    #                print(consecutive_courses)
                    bm.Course.add_requirements(status, "consecutive", consecutive_courses)
    
    # add two days apart requirements
    for grade in ['G3','G4','G6']:
        for ind in range(grade_to_nHomeroom_dict[grade]):
            hr = ind + 1
            bm.Course.add_requirements(status, "two_days_apart", ["_".join([grade, str(hr), '英語', str(1)]), "_".join([grade, str(hr), '彈性英語', str(1)])])           
    # need two days apart requirements for 'G5_1_英語12a_1', 'G5_1_彈性英語12a_1' and so on
    bm.Course.add_requirements(status, "two_days_apart", ['G5_0_英語12c_1','G5_0_彈性英語12c_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_1_英語12a_1','G5_1_彈性英語12a_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_2_英語12b_1','G5_2_彈性英語12b_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_0_英語34c_1','G5_0_彈性英語34c_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_3_英語34a_1','G5_3_彈性英語34a_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_4_英語34b_1','G5_4_彈性英語34b_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_0_英語56c_1','G5_0_彈性英語56c_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_5_英語56a_1','G5_5_彈性英語56a_1'])
    bm.Course.add_requirements(status, "two_days_apart", ['G5_6_英語56b_1','G5_6_彈性英語56b_1'])    
    # add same_period constraints for 'G5_1_英語12a_1', 'G5_2_英語12b_1', 'G5_0_英語12c_1'
    bm.Course.add_requirements(status, 'same_period', ['G5_1_英語12a_1','G5_2_英語12b_1','G5_0_英語12c_1',])
    bm.Course.add_requirements(status, 'same_period', ['G5_1_彈性英語12a_1','G5_2_彈性英語12b_1','G5_0_彈性英語12c_1',])
    bm.Course.add_requirements(status, 'same_period', ['G5_3_英語34a_1', 'G5_4_英語34b_1', 'G5_0_英語34c_1'])
    bm.Course.add_requirements(status, 'same_period', ['G5_3_彈性英語34a_1', 'G5_4_彈性英語34b_1', 'G5_0_彈性英語34c_1'])
    bm.Course.add_requirements(status, 'same_period', ['G5_5_英語56a_1', 'G5_6_英語56b_1', 'G5_0_英語56c_1'])
    bm.Course.add_requirements(status, 'same_period', ['G5_5_彈性英語56a_1', 'G5_6_彈性英語56b_1', 'G5_0_彈性英語56c_1'])
    
    return status
    
def initate_zhes_status():
    status = create_zhes_scheduling_problem_inputs()
#    n_courses = len(status.list_of_Courses)
    # set 週五第一節彈性
    flex_subject_period = {("Friday", 1)}
    for course in status.list_of_Courses:
        if (course.subject == "彈性") and (course.class_index == 1):
            feasible_periods = course.pick_Teacher_Room_and_get_feasible_periods(status, flex_subject_period)
            if feasible_periods == set():
                print('feasible period == None')
            course.assign_course_period(status, list(feasible_periods)[0])
            # course.assign_course_period(status, period)
    # manually assign teacher, rooms and period for some of the courses
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G6_2_音樂_1', ('Monday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G6_2_彈性音樂_1', ('Thursday', 1))

    # manually assign 資源班 
    #B1
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G1_2_綜合_1', ('Friday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G3_5_綜合_1', ('Friday', 3)) 
    #B2
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G4_4_綜合_1', ('Friday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G5_3_綜合_1', ('Friday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status, 'G5_2_綜合_1', ('Friday', 4))
    #B3
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_2_綜合_1', ('Thursday', 5))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_4_綜合_1', ('Thursday', 5))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_6_綜合_1', ('Thursday', 5))
    #B4
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_1_綜合_1', ('Thursday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_2_綜合_1', ('Thursday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_4_綜合_1', ('Thursday', 4))
    #B5
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_數_1', ('Tuesday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_數_1', ('Tuesday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_數_2', ('Wednesday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_數_2', ('Wednesday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_數_3', ('Thursday', 1))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_數_3', ('Thursday', 1))
    #B6
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_數_1', ('Tuesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_數_1', ('Tuesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_數_2', ('Wednesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_數_2', ('Wednesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_數_3', ('Thursday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_數_3', ('Thursday', 2))
    #B社
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_1_綜合_2', ('Tuesday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_綜合_1', ('Tuesday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G5_2_綜合_2', ('Tuesday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_4_綜合_2', ('Tuesday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_綜合_1', ('Tuesday', 7))
    # A1
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_國_1', ('Monday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_國_2', ('Wednesday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_國_3', ('Thursday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_國_4', ('Friday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_國_1', ('Monday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_國_2', ('Wednesday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_國_3', ('Thursday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_5_國_4', ('Friday', 3))
    # A2
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_國_1', ('Monday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_國_2', ('Tuesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_國_3', ('Wednesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_國_4', ('Thursday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_3_國_5', ('Friday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_國_1', ('Monday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_國_2', ('Tuesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_國_3', ('Wednesday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_國_4', ('Thursday', 2))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_1_國_5', ('Friday', 2))
    # A3
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_1_綜合_2', ('Tuesday', 5))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_2_綜合_2', ('Tuesday', 5))
    # A4
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G1_2_綜合_2', ('Tuesday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_5_綜合_2', ('Tuesday', 4))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G3_4_綜合_2', ('Tuesday', 4))
    # A5
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_4_綜合_2', ('Thursday', 5))
#    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_2_綜合_1', ('Thursday', 5))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G4_3_綜合_1', ('Thursday', 5))
    # A6
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G5_2_綜合_3', ('Friday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G5_3_綜合_2', ('Friday', 7))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_4_綜合_3', ('Friday', 7))
    
    # 特別綁課
    bm.Course.add_requirements(status, "same_period", ['G3_4_閩南語_1', 'G3_5_閩南語_1', 'G4_2_閩南語_1'])
    bm.Course.add_requirements(status, "same_period", ['G4_4_閩南語_1', 'G5_3_閩南語_1'])
        
    # 特別配課
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_4_音樂_1', ('Friday', 2))  #佳綾
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_5_音樂_1', ('Friday', 3))
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_5_綜合_1', ('Monday', 1))  #旭政
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G2_5_綜合_2', ('Monday', 2))
    
    bm.Course.assign_Rooms_Teacher_and_period_to_Course(status,'G6_4_閩南語_1', ('Monday', 4))  # 綁課
        
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

