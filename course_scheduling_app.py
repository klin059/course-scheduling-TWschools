# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 09:58:20 2018
scheduling app - providing GUI for reviewing the courses
@author: zhes
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import PostSolution as ps
#from dash.dependencies import Input, Output
import BaseModel as bm
import zhes_scheduling_problem as problem 
import webbrowser

status = problem.initate_zhes_status()
def get_data_dictionary(status_input):
    room_dict, teacher_dict = ps.put_solution_in_df(status_input)
    return {**room_dict, **teacher_dict}
status.all_dict = get_data_dictionary(status)

dropdown_list = []
# merge two dictionaries
for key in status.all_dict:
    dropdown_list.append({'label': key, 'value': key})

def list_to_dropdown_options(list_of_names):
    return [{'label':name, 'value':name} for name in list_of_names]
    

def get_unassigned_course_names_as_dropdown_options(status_input):
    list_of_course_name = [c.name for c in status_input.list_of_unassigned_Courses]
    return list_to_dropdown_options(list_of_course_name)

def generate_table_div(df_table_id, df_dropdown):
    return html.Div([
        dcc.Dropdown(
            id = df_dropdown,
            options=dropdown_list 
        ),
        html.Div(id = df_table_id)
            ], className = 'one-half column')
        
def get_list_of_teacher_names_as_dropdown_options(status_input):
    return list_to_dropdown_options([tr.name for tr in status_input.list_of_Teachers])

def get_list_of_room_names_as_dropdown_options(status_input):
    return list_to_dropdown_options([room.name for room in status_input.list_of_Rooms])

app = dash.Dash()
app.layout = html.Div([
    generate_table_div('df_table1', 'df_dropdown1'),
    generate_table_div('df_table2', 'df_dropdown2'),

    html.Div([
#        html.Div(id='invis_div', children = all_dict, style={'display': 'none'}),
        html.H6('新增課堂:', className = 'one-third column'),
        dcc.Dropdown(
                id = 'add_teacher_filter',
                placeholder = '指定老師',
                options = get_list_of_teacher_names_as_dropdown_options(status)
                ),
        dcc.Dropdown(
                id = 'add_room_filter',
                placeholder = '指定班級',
                options = get_list_of_room_names_as_dropdown_options(status)
                ),
        dcc.Dropdown(
                id = 'add_course_dropdown',
                placeholder = '選課',
                options = get_unassigned_course_names_as_dropdown_options(status)
                ),
        dcc.Dropdown(
                id = 'available_period_dropdown',
                placeholder = '選擇課堂',
#                options = []
                ),
        html.Button('新增課堂', id = 'add_course_button')        
            ], className = 'one-third column'),
        html.Div(id = "print_actions_div")
], className = "row")

# decorator for including var as one of the input
def input_wrapper(var):
    def input_function_wrapper(func):
        def function_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return input_function_wrapper
    return input_wrapper

for df_table, df_dropdown in [('df_table1', 'df_dropdown1'), ('df_table2', 'df_dropdown2')]:
    @input_wrapper(status)
    @app.callback(Output(component_id= df_table, component_property= 'children'), 
                  [Input(component_id= df_dropdown, component_property='value')])
    def generate_table(input_value):
        # expensive operation... change to update only the relevant df in the future
#        all_dict = get_data_dictionary(status)
        if input_value is None:
            return None
        max_rows=10
        dataframe = status.all_dict[input_value]
        return html.Table(
            # Header
            [html.Tr([html.Td(" ")] + [html.Th(col) for col in dataframe.columns])] +
    
            # Body
            [html.Tr([html.Td(i+1)] + [
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))]
        )

    # reload all_dict  when course are added
    @app.callback(Output(df_dropdown, 'value'),
        [Input('print_actions_div', 'children')],
        [State(df_dropdown, 'value')])
    def reload_df_table(children, input_value):
        return input_value

#@input_wrapper(status)
#@app.callback(Output('invis_div', 'children'),
#    [Input('print_actions_div', 'children')])
#def reload_df_table(children):
#    return get_data_dictionary(status)
    
def _mapping_weekday_to_chinese(period):
    mapping = {"Monday":"星期一", 'Tuesday':'星期二' , 'Wednesday':'星期三', 'Thursday':'星期四', 'Friday':'星期五'
               }
    return "{}, {}".format(mapping[period[0]], str(period[1]))

# select course from drop down callback
@input_wrapper(status)
@app.callback(Output(component_id = 'available_period_dropdown', component_property = 'options'), 
              [Input(component_id = 'add_course_dropdown', component_property = 'value')])
def get_feasible_periods_as_dropdown_option(course_name):
    print('get_feasible_periods_as_dropdown_option')
    if course_name in ["", None]:
        print("course_name is none")
        return [{'label': None, 'value': None}]
    course = bm.Course.get_Course_by_name(status, course_name)
    print("selected {}".format(course.name))
    feasible_periods = bm.Course.populate_set_of_periods()
    feasible_periods = course.get_feasible_periods_by_requirement(status, feasible_periods) 
#    print(feasible_periods)
    if feasible_periods == set():
        return [{'label': "無可用課堂", 'value': ""}]
    fp = list(feasible_periods)
    fp.sort()
    solution = [{'label': _mapping_weekday_to_chinese(p), 'value': "_".join([str(p[0]), str(p[1])])} for p in fp]
    return solution

@app.callback(
    Output('available_period_dropdown', 'value'),
    [Input('available_period_dropdown', 'options')])   
def clear_available_period_dropdown_options(options):
    print("clear_available_period_dropdown_options")
    return None
# click add course -> clears add_course_dropdown
    
# assign course and print out action
@input_wrapper(status)
@app.callback(
    Output('print_actions_div', 'children'),
    [Input('add_course_button', 'n_clicks')],
    [State('add_course_dropdown', 'value'), 
     State('available_period_dropdown', 'value')])  
def assign_course_to_period(n_clicks, course_name, period_in_string):
#    print("{} unassigned courses".format(len(status.list_of_unassigned_Courses)))
    #course.assign_course_period(local_solution, period)
    if (course_name is None) or (period_in_string is None):
        return "請先選課及選節"
    if period_in_string is None:
        return "No available period"
    p = period_in_string.split("_")
    print(p)    
    course = bm.Course.get_Course_by_name(status, course_name)
    course.assign_course_period(status, (p[0],int(p[1])))
    print("assigned {} to period {}".format(course.name, p))
    status.all_dict = get_data_dictionary(status)
    if course.Room == course.homeRoom:
        return "分發 {} 至 {} 於 {}".format(course.name, course.Room.name, course.period)
    else:
        return "分發 {} 至 {} (以及{}) 於 {}".format(course.name, course.Room.name, course.homeRoom.name, course.period)

# reload dropdown
@input_wrapper(status)
@app.callback(
    Output('add_course_dropdown', 'options'),
    [Input('print_actions_div', 'children'), Input('add_room_filter', 'value'), Input('add_teacher_filter', 'value')])
def reload_course_dropdown_options(string, room_name, teacher_name):
    if (room_name is None) and (teacher_name is None):
        return get_unassigned_course_names_as_dropdown_options(status)
    elif teacher_name is None:
        return list_to_dropdown_options([course.name for course in status.list_of_unassigned_Courses if course.Room.name == room_name])
    elif room_name is None:
        return list_to_dropdown_options([course.name for course in status.list_of_unassigned_Courses if course.Teacher.name == teacher_name])
    else:
        list_of_course_name = []
        for course in status.list_of_unassigned_Courses:
            if (course.Room.name == room_name) and (course.Teacher.name == teacher_name):
                list_of_course_name.append(course.name)
        return list_to_dropdown_options(list_of_course_name)
# clear add course dropdown value
@app.callback(
    Output('add_course_dropdown', 'value'),
    [Input('add_course_dropdown', 'options')],
    [State('print_actions_div', 'children'), State('add_course_dropdown', 'value')])
def clear_add_course_dropdown(options, string, value):
    if string == "No available period":
        print(value)
        return value
    return None
    
app.css.append_css({
        'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
    
webbrowser.open(r'http://127.0.0.1:8050', new = 0, autoraise = True)

if __name__ == '__main__':
    app.run_server(debug=False)
    

