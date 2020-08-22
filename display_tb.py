# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 20:25:47 2019
contains functions to turn timetable into image
@author: KML
"""
from eduscheduler import PostSolution as ps
import numpy as np
import pickle
#import pandas as pd
import matplotlib.pyplot as plt
import six
from os.path import exists

def timetable_to_image(df):
    
    def _spliting_course_name(series):
        for i in range(len(series)):
    #        print(series.iloc[i])
            if type(series.iloc[i]) is str:
                series.iloc[i] = series.iloc[i].split('_')[2]
            else:
                series.iloc[i] = ""
        return series
    
    def _render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')
    
        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)
    
        for k, cell in  six.iteritems(mpl_table._cells):
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
        return fig, ax

    for col in df.columns:
        df[col] = _spliting_course_name(df[col])
    
    df['Periods'] = df.index
    df = df.reindex(columns = ['Periods','Monday','Tuesday','Wednesday','Thursday','Friday'])
    
    fig, ax = _render_mpl_table(df, header_columns=0, col_width=3.0)
    return fig, ax

def room_tb_to_image(status, room_name, output_f ='images\\test_timetable.png'):
    room_found = False
    for r in status.list_of_Rooms:  
        if r.name == room_name:
            room_found = True
            break
    assert(room_found)
    df = r.get_timetable(status).copy()
    fig, ax = timetable_to_image(df)
    if not exists(output_f):
        fig.savefig(output_f)
    else:
        output_f = output_f[:-4] + '_1.png'
        fig.savefig(output_f)
    plt.close()

if __name__ == "__main__":
    with open("status.pkl", 'rb') as f:
        status = pickle.load(f)
    room_name = 'G3_2'
    room_tb_to_image(status, room_name)
#    # get room object
#    room_found = False
#    for r in status.list_of_Rooms:  
#        if r.name == room_name:
#            room_found = True
#            break
#    assert(room_found)
#    df = r.get_timetable(status).copy()
#        
##    for room in best_status.list_of_Rooms:
##        room_dict[room.name] = room.get_timetable(best_status)
##    room_dict, teacher_dict = ps.put_solution_in_df(status)
##    df = room_dict["G3_2"].copy()
#    fig, ax = timetable_to_image(df)
#    fig.savefig('timetable.png')
    

