# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 09:07:08 2018

Defines classes for the scheduling problem

@author: KML
"""
import pandas as pd
import copy
class Course(object):
    def __init__(self, grade, homeroom_number, subject, class_index):
        # e.g. courses for class 503, grade = 5, homeroom_number = 3
        self.id = id(self)
        self.name = "_".join([str(grade), str(homeroom_number), subject, str(class_index)])
        self.subject = subject  
        self.grade = grade
        # nth class of the subject for the week
        self.class_index = class_index 
        self.homeroom_number = homeroom_number
#        self.type = course_type  # used to decide if this course is taught by homeroom or subject teacher
        self.assigned = False
        self.Teacher = None
        self.potential_teachers = None
        self.period = None  # (day, period_ind)
        self.homeRoom = None  # used to record the corrosponding homeroom
        self.Room = None
        self.potential_rooms = None
        self.available_periods = None
        self.requirements = {}
        self.priority = None
        
    @staticmethod    
    def get_Course_by_name(status, course_name):
        for C in status.list_of_Courses:
            if C.name == course_name:
                return C
        raise Exception("Cannot find course {}".format(course_name))
                    
        
    @classmethod
    def populate_list_of_courses(cls, grade_to_subjects_dict, grades_to_nClasses_dict):
        list_of_courses = []
        for grade, subject_dict in grade_to_subjects_dict.items():
            for subject, Classes_per_week in subject_dict.items():
                for nth_calss in range(Classes_per_week):
                    for homeroom_number in range(grades_to_nClasses_dict[grade]):
                        c = cls(grade, homeroom_number+1, subject, nth_calss+1)
                        list_of_courses.append(c) 
        return list_of_courses
    
    def get_potential_teacher_assignment(self, course_to_teacher_tuples):
#        print('getting potential teacher for {}'.format(self.name))
        potential_teachers = []
        
        for course, teacher in course_to_teacher_tuples:
            if course == self.name:
                potential_teachers.append(teacher)
        if potential_teachers == []:
            raise Exception("cannot find a teacher for {}".format(course))
        return potential_teachers
    
    def pick_teacher_assignment(self, status):
        """ pick teacher from list of potential ones and assign teacher to the course
        """
        if not self.potential_teachers is None:
            potential_teacher = self.potential_teachers
        else:
            potential_teacher = self.get_potential_teacher_assignment(status.course_to_teacher_tuples)
            
        # pick a teacher that's eligible to teach the course
        assert(len(potential_teacher) == 1)
        selected_teacher = potential_teacher[0]
        
        for T in status.list_of_Teachers:
            if T.name == selected_teacher:
                self.Teacher = T
                return T
        raise Exception("cannot find a teacher with the same name")
    
    def get_potential_room_assignment(self, room_to_course_tuples):
        """get a series of feasible room assignment
        """
        potential_rooms = []
        for room, course in room_to_course_tuples:
            if course == self.name:
                potential_rooms.append(room)
        self.potential_rooms = potential_rooms 
        if potential_rooms == []:
            raise Exception("No feasible potential room for {}".format(self.name))
        return potential_rooms
    

    def pick_room_assignment(self, status):
        """pick a feasible room assignment and assign to course.Room
            also assign homeRoom if possible
        """
        if not self.potential_rooms is None:
            potential_rooms = self.potential_rooms
        else:
            potential_rooms = self.get_potential_room_assignment(status.room_to_course_tuples)
        if (len(potential_rooms) != 1):
            print("debugging - {}".format(potential_rooms))
        assert(len(potential_rooms) == 1)
        room_name = potential_rooms[0]
        for R in status.list_of_Rooms:
            if R.name == room_name:
                self.Room = R
                break
            
        if self.homeRoom is None:
            hr_name = '_'.join([self.grade, str(self.homeroom_number)])
            if self.Room.name == hr_name:
                self.homeRoom = self.Room
            else:
                # get homeroom object and add
                room_found = False
                for R in status.list_of_Rooms:
                    if R.name == hr_name:
                        self.homeRoom = R
                        room_found = True
                        break
                if not room_found:
                    raise Exception('Cannot find homeRoom for the course')
        return self.Room

    @staticmethod
    def assign_Rooms_Teacher_and_period_to_Course(status, course_name, period):
       
        course = Course.get_Course_by_name(status, course_name)
        course.pick_room_assignment(status)
        course.pick_teacher_assignment(status)
        course.assign_course_period(status, period)
        
    

        
    @staticmethod
    def populate_set_of_periods():
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        period_ind = [i+1 for i in range(7)]
        set_of_periods = set()
        for day in days:
            for ind in period_ind:
                set_of_periods.add((day, ind))
        set_of_periods -= {('Monday', 7), ('Wednesday', 5), ('Wednesday', 6), ('Wednesday', 7)}
        
        return set_of_periods
        
    def get_feasible_periods_by_grade_and_subject(self, status, set_of_periods):
        # based on the Grade and the Subject, derive available periods
#           set_of_periods = Course.populate_set_of_periods()        
#        restricted_periods = set()
        if self.grade in ['G1', 'G2']:
            set_of_periods -= {('Monday', 5), ('Monday', 6), ('Thursday', 5),('Thursday', 6), ('Thursday', 7),
                                        ('Friday', 5),('Friday', 6), ('Friday', 7)} 
#            restricted_periods.update([('Monday', 5), ('Monday', 6), ('Thursday', 5),('Thursday', 6), ('Thursday', 7)
#                                        ('Friday', 5),('Friday', 6), ('Friday', 7)])
        elif self.grade in ['G3', 'G4']:
            set_of_periods -= {('Monday', 5), ('Monday', 6)}
#            restricted_periods.update([('Monday', 5), ('Monday', 6)])
        # subjects not allowed near noon
        periods_to_remove = set()
        if self.subject in ['PE', '體育']:
            for period in set_of_periods:
                if period[1] in [4, 5]:
                    periods_to_remove.add(period)
        set_of_periods -= periods_to_remove
                    
        return set_of_periods
    

    
    def pick_Teacher_Room_and_get_feasible_periods(self, status, feasible_periods):
            # pick Teacher, Room 
            teacher = self.pick_teacher_assignment(status)
            room = self.pick_room_assignment(status)
            # get feasible periods from Room and Teacher
            feasible_periods = get_feasible_periods_for_Room_homeRoom_and_Teacher(room, self.homeRoom, teacher, feasible_periods)
            # get feasible periods for the course (grade and subject)
            feasible_periods = self.get_feasible_periods_by_grade_and_subject(status, feasible_periods)
            return feasible_periods
    @staticmethod
    def _two_days_apart_restricted_days(selected_course_day):
        """ input: selected day for one course, set days not available for the other courses """
        
        restricted_days = {'Monday':{'Monday', 'Tuesday', 'Wednesday'},
                         'Tuesday':{'Monday', 'Tuesday', 'Wednesday','Thursday'},
                         'Wednesday':{'Tuesday','Wednesday','Thursday'},
                         'Thursday':{'Tuesday', 'Wednesday','Thursday','Friday'},
                         'Friday':{'Wednesday','Thursday','Friday'}
                         }
        return restricted_days[selected_course_day]
    
    def get_feasible_periods_by_requirement(self, status, feasible_periods):
        
        # None, "same_period", "not_same_day", "after_course"
        if self.requirements == {}:
            feasible_periods = self.pick_Teacher_Room_and_get_feasible_periods(status, feasible_periods)        
        else:
            if "same_period" in self.requirements:
                for c in self.requirements["same_period"]:
                    feasible_periods = c.pick_Teacher_Room_and_get_feasible_periods(status, feasible_periods)
                                        
            if "not_same_day" in self.requirements:
                feasible_periods = self.pick_Teacher_Room_and_get_feasible_periods(status, feasible_periods) 
                restricted_days = set()
                for list_of_Courses in self.requirements["not_same_day"]:
                    for c in list_of_Courses:
                        # get days restricted
                        if c == self:
                            continue
                        else:
                            if c.assigned == True:
                                restricted_days.add(c.period[0])
                # get feasible periods in restricted days
                periods_to_remove = []
                for p in feasible_periods:
                    if p[0] in restricted_days:
                        periods_to_remove.append(p)
                # remove those restricted periods
                for p in periods_to_remove:
                    feasible_periods.remove(p)
            if "consecutive" in self.requirements:
                feasible_periods = self.pick_Teacher_Room_and_get_feasible_periods(status, feasible_periods) 
                for C in self.requirements["consecutive"]:
                    if C == self:
                        continue
                    else:
                        if C.assigned == True:
                            # if the other course is assigned, one can only pick the period before or after the course
                            # depending on the period of the assigned course
                            if C.period[1] in [1,3,5]:
                                feasible_periods = {(C.period[0], C.period[1]+1)} & feasible_periods
                            elif C.period[1] in [2,4]:
                                feasible_periods = {(C.period[0], C.period[1]-1)} & feasible_periods
                            elif C.period[1] == 6:
                                feasible_periods = {(C.period[0], C.period[1]-1), (C.period[0], C.period[1]+1)} & feasible_periods
                            elif C.period[1] == 7:
                                feasible_periods = {(C.period[0], C.period[1]-1)} & feasible_periods
                        else:
                            # otherwise, find periods (day, i), i in {1, 3, 5, 6}, where (day, i+1) is also feasible
                            periods_to_remove = set()
                            for p in feasible_periods:
                                if not p[1] in [1, 3, 5, 6]:
                                    periods_to_remove.add(p)
                                else:
                                    if not (p[0], p[1]+1) in feasible_periods:
                                        periods_to_remove.add(p)
                            for p in periods_to_remove:
                                feasible_periods.remove(p)
                                
            if "two_days_apart" in self.requirements:
                feasible_periods = self.pick_Teacher_Room_and_get_feasible_periods(status, feasible_periods) 
                restricted_days = set()
                for C in self.requirements["two_days_apart"]:
                    # get days restricted
                    if C == self:
                        continue
                    else:
                        if C.assigned == True:
                            restricted_days.update(Course._two_days_apart_restricted_days(C.period[0]))
                # get feasible periods in restricted days
                               
#                periods_to_remove = []
                for p in feasible_periods.copy():
                    if p[0] in restricted_days:
                        feasible_periods.remove(p)

        return feasible_periods
        
       
    
    @staticmethod            
    def add_requirements(status, requirement_type, list_of_affected_course_names):
        # args would be one or more courses
        # only add one requirement at a time
        
        #define allowed requirement types first
        if not requirement_type in ["same_period", "not_same_day", "consecutive", "two_days_apart"]:
            raise Exception("Requirement not defined.")
        
        affected_Courses = []
        for course_name in list_of_affected_course_names:
            grade, homeroom_number, subject, class_index = course_name.split("_")
            C = Course.get_Course_by_name(status, course_name)
            affected_Courses.append(C)
        
        for C in affected_Courses:
            if requirement_type == "not_same_day":
                if not requirement_type in C.requirements:
                    C.requirements[requirement_type] = []
                C.requirements[requirement_type].append(affected_Courses)
            else:
                if requirement_type in C.requirements:                
                    raise Exception("{} Requirement exists for course {}".format(requirement_type, C.name))
                C.requirements[requirement_type] = affected_Courses

        
        
        

    
    
    def assign_course_period(self, status, period):
        assert(not period == set())
            
        # check if the period is occupied (maybe so if force assignment)
        for schedule in self.Teacher.schedule_in_tuples:
            if (schedule[0], schedule[1]) == period:
                raise Exception("Assigning {}: {} period {} occupied by {}".format(self.name,
                                self.Teacher.name, period, schedule[2]))
        for schedule in self.Room.schedule_in_tuples:
            if (schedule[0], schedule[1]) == period:
                raise Exception("Assigning {}: {} period {} occupied by {}".format(self.name, 
                                self.Room.name, period, schedule[2]))
        if not self.Room == self.homeRoom:
            for schedule in self.homeRoom.schedule_in_tuples:
                if (schedule[0], schedule[1]) == period:
                    raise Exception("Assigning {}: {} period {} occupied by {}".format(self.name, 
                                    self.homeRoom.name, period, schedule[2]))
        
        if self.assigned:
            raise Exception("{} is already assigned".format(self.name))
        self.assigned = True

        self.period = period

        status.change_Course_to_assigned_list(self)
        self.Teacher.schedule_in_tuples.append((period[0], period[1], self.name))
        self.Room.schedule_in_tuples.append((period[0], period[1], self.name))
        if not self.Room == self.homeRoom:
            self.homeRoom.schedule_in_tuples.append((period[0], period[1], self.name))
                    
    @staticmethod
    def assign_Course_period(status, course_name, period):
        course = None
        for C in status.list_of_Courses:
            if C.name == course_name:
                course = C
        course.assign_course_period(status, period)
        
    def unassign_course(self, status):
#        print('removing {}'.format(self.name))

        # assume room, homeroom and teacher stays the same
        if not self.assigned:
            raise Exception("{} is not assigned yet".format(self.name))
        self.assigned = False
        
        self.Room.schedule_in_tuples.remove((self.period[0], self.period[1], self.name))
        if not self.Room == self.homeRoom:
            self.homeRoom.schedule_in_tuples.remove((self.period[0], self.period[1], self.name))
        self.Teacher.schedule_in_tuples.remove((self.period[0], self.period[1], self.name))
        
        self.period = None
           
        status.change_Course_to_unassigned_list(self)
    @staticmethod
    def unassign_Course(status, course_name):
        course = None
        for C in status.list_of_Courses:
            if C.name == course_name:
                course = C
        course.unassign_course(status)
    


    
    def check_valid_assignment(self, Teacher, period, Room):
        NotImplementedError  
    
    def random_assignment(self, list_of_Teachers, list_of_Periods, list_of_rooms):
        NotImplementedError
        
    
        
class Teacher(object):
    def __init__(self, name, list_of_grade_hr_subject_tuple):
        self.id = id(self)
        self.name = name
#        self.list_of_specilized_subjects = list_of_specilized_subjects
        self.type = None
        # list of grade, homeroom, subject the teacher is allowed to teach
        self.list_of_grade_homeroom_subject_tuple = list_of_grade_hr_subject_tuple
        # List of assigned courses
        self.schedule_in_tuples = []  # e.g. ('Wednesday', 3, course.name)
        self.restricted_periods = []
    def add_schedule(self, day, period, course_name):
        self.schedule_in_tuples.append((day, period, course_name))
    @staticmethod
    def get_Teacher_by_name(status, tr_name):
        for T in status.list_of_Teachers:
            if T.name == tr_name:
                return T
        raise Exception("Cannot find Teacher named".format(tr_name))
        
    def get_timetable(self):
        df = get_empty_timetable()
        for schedule in self.schedule_in_tuples:
            assert(pd.isnull(df.loc[schedule[1], schedule[0]]))
            df.loc[schedule[1], schedule[0]] = schedule[2]
        return df


class SubjectTeacher(Teacher):
    def __init__(self, name, list_of_grade_hr_subject_tuple):
        super(SubjectTeacher, self).__init__(name, list_of_grade_hr_subject_tuple)
        self.type = 'subject'
        self.on_hourly_rate = None
    
    @classmethod
    def populate_list_of_subject_Teachers(cls, list_of_grade_hr_subject_tuple):
        list_of_subject_tr = []
        for t_name, list_of_grade_hr_subject_tuple in list_of_grade_hr_subject_tuple.items():
            list_of_subject_tr.append(cls(t_name, list_of_grade_hr_subject_tuple))
        return list_of_subject_tr

class HomeroomTeacher(Teacher):
    def __init__(self, name, grade, room_number, list_of_grade_hr_subject_tuple):
        super(HomeroomTeacher, self).__init__(name, list_of_grade_hr_subject_tuple)
        self.type = 'homeroom'
        self.grade = grade
        self.room_number = room_number
        
    @classmethod
    def populate_list_of_homeroom_Teachers(cls, hr_teacher_to_list_of_teaching_tuple):
        
        list_of_hr_tr = []
        
        for tr_name, list_of_teaching_tuple in hr_teacher_to_list_of_teaching_tuple.items():
            info = list_of_teaching_tuple
            grade = info[0]
            homeroom_no = info[1]
            HR_tr = cls(tr_name, grade, homeroom_no, list_of_teaching_tuple)
            list_of_hr_tr.append(HR_tr)
        return list_of_hr_tr
    
        
class Room(object):
    def __init__(self, name, list_of_subject, allowed_homeroom):
        self.id = id(self)
        self.name = name
        self.grade = name.split('_')[0]
        # ('all,'all) for all homerooms and allowed subject
        # list of (grade, homeroom, subject) tuples
        # string for one homerorom e.g. 'G4_1' for G4_1 allowed subjects in the room
        self.allowed_homeroom = allowed_homeroom  
        # list of subjects that the room can be used for
        self.list_of_subject = list_of_subject
        self.schedule_in_tuples = []
        self.restricted_periods = []
    @classmethod    
    def populate_list_of_homeroomes(cls, grades_to_nClasses_dict, subjects_allowed_in_homeroom):
        list_of_homerooms = []
        for grade, n_homerooms in grades_to_nClasses_dict.items():
            for ind in range(n_homerooms):
                hm = cls("_".join([grade, str(ind+1)]), subjects_allowed_in_homeroom[grade], 
                         (grade, ind+1))
                list_of_homerooms.append(hm)
        return list_of_homerooms
    @classmethod
    def populate_list_of_subjectrooms(cls, subjectroom_to_subject_dict):
        """
        
        """
        list_of_subjectrooms = []
        for subjectroom , list_of_subjects in subjectroom_to_subject_dict.items():
            room = cls(subjectroom, list_of_subjects, ('all','all'))
            list_of_subjectrooms.append(room)
        return list_of_subjectrooms
    
    def add_schedule(self, day, period, course_name):
        self.schedule_in_tuples.append((day, period, course_name))
    @staticmethod
    def get_Room_by_name(status, room_name):
        for R in status.list_of_Rooms:
            if R.name == room_name:
                return R
        raise Exception("Cannot find a Room named".format(room_name))
        
    def get_timetable(self, status):
        df = get_empty_timetable()
        
        for schedule in self.schedule_in_tuples:
            assert(pd.isnull(df.loc[schedule[1], schedule[0]]))
            course = Course.get_Course_by_name(status, schedule[2])
            df.loc[schedule[1], schedule[0]] = "_".join([schedule[2], course.Teacher.name])
        if df is None:
            raise Exception("df is None")
        return df
    
            
class Status(object):
    def __init__(self, list_of_Courses, list_of_Teachers, list_of_Rooms):
        self.list_of_Courses = list_of_Courses
        self.list_of_fixed_Courses = []
        self.list_of_unassigned_Courses = list_of_Courses.copy()
        self.list_of_assigned_Courses = []
        self.list_of_stalled_Courses = []
        self.list_of_Teachers = list_of_Teachers
        self.list_of_Rooms = list_of_Rooms
        self.course_to_teacher_tuples = []  # records feasible course to teacher assignment
        self.room_to_course_tuples = []  # records feasible room to course assignment
#        self.grade_to_hr_teacher_names = None
    def change_Course_to_assigned_list(self, Course):
        assert(Course in self.list_of_unassigned_Courses)
        self.list_of_unassigned_Courses.remove(Course)
        self.list_of_assigned_Courses.append(Course)
    
    def change_Course_to_unassigned_list(self, Course):
        assert(Course in self.list_of_assigned_Courses)
        self.list_of_unassigned_Courses.append(Course)
        self.list_of_assigned_Courses.remove(Course)

    def fix_assigned_Courses(self):
        courses = [C for C in self.list_of_assigned_Courses]
        for C in courses:
            self.change_Course_to_fixed_list(C)
    def free_fixed_Courses(self):
        courses = self.list_of_fixed_Courses.copy()
        for C in courses:
            assert(C in self.list_of_fixed_Courses)
            self.list_of_assigned_Courses.append(C)
            self.list_of_fixed_Courses.remove(C)
    
    def free_stalled_Courses(self):
        # change all courses in stalled list to unassigned list
        courses = self.list_of_stalled_Courses.copy()
        for C in courses:
            assert(C in self.list_of_stalled_Courses)
            self.list_of_unassigned_Courses.append(C)
            self.list_of_stalled_Courses.remove(C)
    
    def change_Course_to_fixed_list(self, Course):
        # can only move Course from assigned list to fixed list
        assert(Course in self.list_of_assigned_Courses)
        self.list_of_assigned_Courses.remove(Course)
        self.list_of_fixed_Courses.append(Course)
        
    def change_unassigned_Course_to_stalled_list(self, course):
        assert(course in self.list_of_unassigned_Courses)
        self.list_of_unassigned_Courses.remove(course)
        self.list_of_stalled_Courses.append(course)
        
    def change_stalled_Course_to_unassigned_list(self, course):
        assert(course in self.list_of_stalled_Courses)
        self.list_of_stalled_Courses.remove(course)
        self.list_of_unassigned_Courses.append(course)
            
    def populate_course_to_teacher_tuples(self):
        for course in self.list_of_Courses:
            for teacher in self.list_of_Teachers:
                if (course.grade, course.homeroom_number, course.subject) in teacher.list_of_grade_homeroom_subject_tuple:
                    self.course_to_teacher_tuples.append((course.name, teacher.name))
    def populate_room_to_course_tuples(self):
        for room in self.list_of_Rooms:
            # for subject room allowing all homerooms
            if room.allowed_homeroom == ('all','all'):
                for course in self.list_of_Courses:
                    if course.subject in room.list_of_subject:
                        self.room_to_course_tuples.append((room.name, course.name))
            elif type(room.allowed_homeroom) == list:  # where room.allowed_homeroom = [(grade, homeroom, subject)...]
                for course in self.list_of_Courses:
                    if (course.grade, course.homeroom_number, course.subject) in room.allowed_homeroom:
                        self.room_to_course_tuples.append((room.name, course.name))
            else:
                for course in self.list_of_Courses:
                    if (course.subject in room.list_of_subject) and (course.grade, course.homeroom_number) == room.allowed_homeroom:
                        self.room_to_course_tuples.append((room.name, course.name))
    def print_unassigned_course_names(self):
        return [C.name for C in self.list_of_unassigned_Courses]
    @classmethod
    def _copy(cls, status):

        return copy.deepcopy(status)
    
    def make_copy(self):
        return Status._copy(self)
    
    def assert_status(self):
        assert(not False in [C.assigned for C in self.list_of_assigned_Courses])
        assert(not False in [C.assigned for C in self.list_of_fixed_Courses])
        assert(not True in [C.assigned for C in self.list_of_unassigned_Courses])
            

def get_empty_timetable():
    period_ind = [i+1 for i in range(7)]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    df = pd.DataFrame(index = period_ind, columns = days)
    return df


def get_teacher_timetable(Teacher, list_of_Courses):
    """ TestCase1
    """
    df = get_empty_timetable()
    for course in list_of_Courses:
        if (course.Teacher == Teacher):
            df.loc[course.period[1], course.period[0]] = course.name
    return df



def get_feasible_periods_for_Room_homeRoom_and_Teacher(room, homeRoom, teacher, set_of_feasible_period_tuples):
#    set_of_period_tuples = Course.populate_set_of_periods()
    restricted_periods = set(room.restricted_periods + teacher.restricted_periods + homeRoom.restricted_periods)
    for (day, period) in restricted_periods:
        if (day, period) in set_of_feasible_period_tuples:
            set_of_feasible_period_tuples.remove((day, period))
        
    for day, period, course in room.schedule_in_tuples:
        if (day, period) in set_of_feasible_period_tuples:
            set_of_feasible_period_tuples.remove((day, period))
            
    for day, period, course in homeRoom.schedule_in_tuples:
        if (day, period) in set_of_feasible_period_tuples:
            set_of_feasible_period_tuples.remove((day, period))
            
    for day, period, course in teacher.schedule_in_tuples:
        if (day, period) in set_of_feasible_period_tuples:
            set_of_feasible_period_tuples.remove((day, period))
    return set_of_feasible_period_tuples
    

        
