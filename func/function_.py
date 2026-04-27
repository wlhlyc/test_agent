import ast
import re
import requests
import traceback
from openai import OpenAI


C_N = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'日':7}
P_N = {'南':0,'北':1}


def df1_to_dat(df):
    inf_ = []
    for i in range(len(df)):
        lis = []
        for j in range(len(df[i])):
            try:
                lis.append(ast.literal_eval(df[i][j]))
            except:
                lis.append(df[i][j])
        inf_.append(lis)
    return inf_

def df2_to_dat(df):
    inf_ = []
    for i in range(len(df)):
        lis = []
        try:
            for j in range(len(df[i])):
                st = df[i][j].replace('nan','\'none\'')
                lis.append(ast.literal_eval(st))
        except:
            pass
        inf_.append(lis)
    return inf_

def return_class_lap_w(li, ye, te):

    inf_ = []
    lis_ = []
    for i in range(len(li)):
        if i == 19:
            pass
        lis = []
        try:
            for j in range(len(li[i])):
                st = li[i][j].replace('nan','\'none\'')
                lis.append(ast.literal_eval(st))
        except:
            pass

        if lis[0][4] == '21-22':
            continue

        for j in range(len(lis)):

            inf_ea = []


            #星期
            da = lis[j][3][2:3]
            da_num = C_N[da]
            da_fin = [0 for k in range(7)]
            da_fin[da_num-1] = 1

            #次数
            tims_fin = int(lis[j][1])

            #时间(第几节课)
            ti_be, ti_en = map(int, re.findall(r'\d+', lis[j][3]))
            ti_fin = [0 for k in range(12)]
            for kk in range(ti_be-1,ti_en):
                ti_fin[kk] = 1

            #时间(第几周)
            week_fin = [0 for k in range(18)]
            lis_sp = lis[j][4].split(' ')
            for lis_sp_n in lis_sp:
                if len(re.findall(r'\d+', lis_sp_n)) == 1:
                    try:
                        week_fin[int(lis_sp_n)-1] = 1
                    except:
                        pass
                else:
                    week_be, week_en = map(int,re.findall(r'\d+', lis_sp_n))
                    if lis_sp_n[-1] == '单':
                        for m in range(int((week_en-week_be)/2)+1):
                            week_fin[week_be + m*2 - 1] = 1
                    elif lis_sp_n[-1] == '双':
                        for m in range(int((week_en-week_be)/2)+1):
                            week_fin[week_be + m*2 - 1] = 1
                    else:
                        for m in range(week_en-week_be+1):
                            week_fin[week_be + m - 1]=1


            #年级
            gr_fin = [0 for k in range(4)]
            try:
                gr = lis[j][6].split(",")
                for k in range(len(gr)):
                    gr_no = ye - int(gr[k][0:4])
                    gr_fin[gr_no - 1] = 1
                    # if te == 1:
                    #     gr_no = ye - int(gr[k][0:4]) +1
                    # else:
                    #     gr_no = ye - int(gr[k][0:4])
                    # gr_fin[gr_no-1] = 1
            except:
                gr_fin = [1 for k in range(4)]

            #人数
            num_fin = lis[j][7]

            #地点
            pl_fin = [0 for k in range(7)]
            pl_a = lis[j][8]
            pl_p = P_N[pl_a[0:1]]
            pl_f = int(pl_a[1:2])+1
            pl_fin[pl_p] = 1
            pl_fin[pl_f] = 1
            if pl_a[2:4] == '01' or pl_a[2:4] == '29':
                pl_fin[-1] = 1

            inf_ea.append(da_fin)
            inf_ea.append(tims_fin)
            inf_ea.append(ti_fin)
            inf_ea.append(week_fin)
            inf_ea.append(gr_fin)
            inf_ea.append(num_fin)
            inf_ea.append(hash(str(lis[j][0])+str(lis[j][2])+str(lis[j][6])))
            inf_ea.append(pl_fin)

            inf_.append(inf_ea)
            lis_.append(lis[j])


    class_lap_w = [[[] for j in range(5)] for i in range(7)]
    class_lap_b = [[[] for j in range(5)] for i in range(7)]

    for i in range(len(inf_)):
        class_no = [i for i, x in enumerate(inf_[i][2]) if x != 0]
        tim = list(set(int(i/2) for i in class_no))
        day = [ii for ii in range(len(inf_[i][0])) if inf_[i][0][ii] != 0]
        for j in range(len(tim)):
            if tim[j] == 5 or tim[j] == 6:
                continue
            class_lap_w[day[0]][tim[j]].append(inf_[i])
            class_lap_b[day[0]][tim[j]].append(lis_[i])
            pass
        pass
    pass

    return class_lap_w, class_lap_b, inf_, lis_

def class_week_lap(li):
    inf_ = []
    for i in range(len(li)):
        lis = []
        try:
            for j in range(len(li[i])):
                st = li[i][j].replace('nan', '\'none\'')
                lis.append(ast.literal_eval(st))
        except:
            pass
        inf_.append(lis)
    week_day = [[[[] for k in range(5)] for j in range(7)] for i in range(17)]
    for i in range(len(inf_)):
        for j in range(len(inf_[i])):
            for k in range(len(inf_[i][j])):
                for m in range(len(inf_[i][j][k][3])):
                    if m == 17:
                        continue
                    if inf_[i][j][k][3][m] == 1:
                        class_no = [i for i, x in enumerate(inf_[i][j][k][2]) if x != 0]
                        tim = list(set(int(i / 2) for i in class_no))
                        day = [ii for ii in range(len(inf_[i][j][k][0])) if inf_[i][j][k][0][ii] != 0]
                        for jj in range(len(tim)):
                            if tim[jj] == 5 or tim[jj] == 6:
                                continue
                            week_day[m][day[0]][tim[jj]].append(inf_[i][j][k])

    pass
    return week_day

def class_week_lap_num(inf, lis):
    class_lap_num = [[[]for i in range(5)]for j in range(7)]
    class_lap = [[[]for i in range(5)]for j in range(7)]
    de = ['01', '29']
    for it in range(len(inf)):
        if sum(inf[it][3][0:17]) == 17:
            inf[it][3][-1] = 1

    for i in range(len(inf)):
        if lis[i][-1][2:4] in de:
            continue
        class_no = [j for j, x in enumerate(inf[i][2]) if x != 0]
        tim = list(set(int(j/2) for j in class_no))
        day = [ii for ii in range(len(inf[i][0])) if inf[i][0][ii] != 0]
        for j in range(len(tim)):
            if tim[j] == 5 or tim[j] == 6:
                continue
            if inf[i] not in class_lap_num[day[0]][tim[j]]:
                class_lap_num[day[0]][tim[j]].append(inf[i])
                class_lap[day[0]][tim[j]].append(lis[i])
            pass
        pass
    return class_lap_num, class_lap

def return_class_name(df):
    inf_ = []
    for i in range(len(df)):
        lis = []
        try:
            for j in range(len(df[i])):
                st = df[i][j].replace('nan','\'none\'')
                lis.append(ast.literal_eval(st))
        except:
            pass
        inf_.append(lis)
    class_name_ = []
    for i in range(len(inf_)):
        class_name_.append(inf_[i][0][0])
    return class_name_

# def chat_with_llama(prompt: str) -> str:
#     payload = {
#         "model": "llama3.2:3b-instruct-q5_0",
#         "prompt": prompt,
#         "stream": False,
#         "options": {"temperature": 0.5, "max_tokens": 2000}
#     }
#     try:
#         response = requests.post(OLLAMA_API_URL, json=payload)
#         response.raise_for_status()
#         return response.json().get("response", "")
#     except Exception as e:
#         return f"调用失败: {str(e)}"

def class_begin(class_l_n, class_l, di):
    place = {kk: {jj: [[0 for kk in range(18)], []] for jj in range(16)} for kk in range(8)}
    place[2][16] = [[0 for kk in range(18)], []]
    place[3][16] = [[0 for kk in range(18)], []]
    place[6][16] = [[0 for kk in range(18)], []]
    place[7][16] = [[0 for kk in range(18)], []]
    room_list = [item[-1] for item in class_l]
    for i in range(len(room_list)):
        no = di[int(room_list[i][1:4])]
        if no // 16 == 0:
            a_no = no%16
            f_no = 0
        elif no // 16 == 1:
            a_no = no%16
            f_no = 1
        elif no // 16 == 2 or no / 16 == 3:
            a_no = no%16
            if no == 48:
                a_no = 16
            f_no = 2
        else:
            a_no = no - 49
            f_no = 3
        if room_list[i][0] == '南':
            # class_l_n[i].append('南'+str(f_no)+'/'+str(a_no))
            if class_l_n[i][6] not in place[f_no][a_no][1]:
                place[f_no][a_no][1].append(class_l_n[i][6])
            place[f_no][a_no][0] = [1 if class_l_n[i][3][it] == 1 or place[f_no][a_no][0][it] == 1
                                          else 0 for it in range(len(class_l_n[i][3]))]
            if sum(place[f_no][a_no][0]) == 17:
                place[f_no][a_no][0][-1] = 1
        else:
            # class_l_n[i].append('北'+str(f_no)+'/'+str(a_no))
            if class_l_n[i][6] not in place[f_no+4][a_no][1]:
                place[f_no+4][a_no][1].append(class_l_n[i][6])
            place[f_no+4][a_no][0] = [1 if class_l_n[i][3][it] == 1 or place[f_no+4][a_no][0][it] == 1
                                          else 0 for it in range(len(class_l_n[i][3]))]
            if sum(place[f_no+4][a_no][0]) == 17:
                place[f_no+4][a_no][0][-1] = 1

    pass
    return place, class_l_n

def class_sche(class_l_n, class_l, class_uni_to, ii, jj, mm, nn):
    place = {kk: {jj: [[0 for kk in range(18)], []] for jj in range(16)} for kk in range(8)}
    place[2][16] = [[0 for kk in range(18)], []]
    place[3][16] = [[0 for kk in range(18)], []]
    place[6][16] = [[0 for kk in range(18)], []]
    place[7][16] = [[0 for kk in range(18)], []]
    # class_list_num = class_lap_num[m][n]
    # class_list = class_lap[m][n]
    class_nd = []
    # for q in range(18):
    for p in range(len(class_l_n)):
        # if class_lap_num[m][n][p][3][q] == 1:
        class_nd.append([class_l_n[p], class_l[p]])
    it = 0
    ds = 0

    while it < len(class_nd):
        ds += 1
        if ds >10000:
            return 0
        if class_nd[it][0][6] == class_nd[min(it+1,len(class_nd)-1)][0][6]:
            class_uni = [class_nd[ite] for ite in range(it, min(it+17, len(class_nd))) if class_nd[it][0][6] == class_nd[ite][0][6]]
        else:
            class_uni = [class_nd[it]]
        week = class_nd[it][0][3]
        wk = [1 if any(ia[0][3][ja] == 1 for ia in class_uni) else 0 for ja in range(18)]
        if wk not in class_uni_to:
            class_uni_to.append(wk)
        if sum(wk) == 1:
            pass
        class_hash = class_nd[it][0][6]
        try:
            for item in place:
                bu_item = 0
                for items in place[item]:
                    bu_items = 0
                    if place[item][items][0][17] == 1:
                        continue
                    else:
                        if all(place[item][items][0][ww] == 0 for ww in range(len(wk)) if wk[ww] == 1):
                            place[item][items][0] = [1 if wk[i] == 1 else place[item][items][0][i] for
                                                           i in range(len(wk))]
                            place[item][items][1].append(class_hash)
                            bu_items = 1
                            bu_item = 1
                            for aa in range(len(class_uni)):
                                # class_l_n[it].append('南' + str(item) + '/' + str(items))
                                it += 1
                            if all(place[item][items][0][ww] == 1 for ww in range(17)):
                                place[item][items][0][17] = 1
                        else:
                            continue
                    if bu_items == 1:
                        break
                if bu_item == 1:
                    break
            # if ran == 1:
            #     for item in place_north:
            #         bu_item = 0
            #         for items in place_north[item]:
            #             bu_items = 0
            #             if place_north[item][items][0][17] == 1:
            #                 continue
            #             else:
            #                 if all(place_north[item][items][0][ww] == 0 for ww in
            #                        range(len(wk)) if wk[ww] == 1):
            #                     place_north[item][items][0] = [1 if wk[i] == 1 else place_north[item][items][0][i] for
            #                                                    i in range(len(wk))]
            #                     place_north[item][items][1].append(class_hash)
            #                     bu_items = 1
            #                     bu_item = 1
            #                     for aa in range(len(class_uni)):
            #                         # class_l_n[it].append('北' + str(item) + '/' + str(items))
            #                         it += 1
            #                     if all(place_north[item][items][0][ww] == 1 for ww in range(17)):
            #                         place_north[item][items][0][17] = 1
            #                 else:
            #                     continue
            #             if bu_items == 1:
            #                 break
            #         if bu_item == 1:
            #             break
        except Exception as e:
            traceback.print_exc()
            pass
        pass
    return place, class_l_n, class_uni_to


def nd_fitting_data(li):
    inf_ = []
    for i in range(len(li)):
        lis = []
        try:
            for j in range(len(li[i])):
                st = li[i][j].replace('nan','\'none\'')
                lis.append(ast.literal_eval(st))
        except:
            pass
        inf_.append(lis)
    pass
    return lis