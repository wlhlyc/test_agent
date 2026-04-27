import pandas as pd
from func import function_, ga
import numpy as np
import traceback


df_nd_com = pd.read_excel('./data/data_nd_per.xlsx')
dat_nd = df_nd_com.values.tolist()
class_to = []
for i in range(10):
    for j in range(2):
        year_ = 2016+i
        team_ = 1+j
        she_name = str(year_)+'_'+str(team_)
        df_num = pd.read_excel("./data/data_num.xlsx", sheet_name=she_name)
        dat_num = df_num.values.tolist()
        da_num = function_.df1_to_dat(dat_num)
        df_name = pd.read_excel('./data/data_num_b.xlsx', sheet_name=she_name)
        dat_name = df_name.values.tolist()
        da_name = function_.df1_to_dat(dat_name)
        df_hash = pd.read_excel('./data/data_num_hash.xlsx', sheet_name=she_name)
        dat_hash = df_hash.values.tolist()
        da_hash = function_.df2_to_dat(dat_hash)
        class_lap_num, class_lap = function_.class_week_lap_num(da_num, da_name)
        room = [(j+1)*100+i for i in range(5, 22) if i%2 == 1 for j in range(4)]
        room.extend([(j+1)*100+i for i in range(8, 23) if i%2 == 0 for j in range(4)])
        room.remove(113)
        room.remove(213)
        room = sorted(room)
        di = {item:i for i,item in enumerate(room)}
        for m in range(7):
            for n in range(5):
                class_l_n = class_lap_num[m][n]
                class_l = class_lap[m][n]
                place_b, class_lap_n_b = function_.class_begin(class_l_n, class_l, di)
                place, class_lap_n, class_to = function_.class_sche(class_l_n, class_l, class_to, i, j, m, n)
                population_begin = [place,place_b]
                mut_rate, num_iteration = 0.5, 3
                ttt = ga.ga_1(population_begin, class_lap_n, class_lap, mut_rate, num_iteration)
                pass
    pass
print(class_to)
dd = pd.DataFrame(class_to)
with pd.ExcelWriter('dd.xlsx', engine='openpyxl') as writer:
    dd.to_excel(writer, sheet_name='1', index=False)

