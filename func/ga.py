import numpy as np
import bisect
import random
import copy


def ga_1(population_begin, class_lap_n, class_lap, mut_rate, num_iteration):
    population = population_begin
    best_re = 10000000
    ty_dic = {'liner':[sum([(15-i)/sum(range(16)) for i in range(j)]) for j in range(1,16)], 'exp':[sum([(1/2)**(i+1) for i in range(j)]) for j in range(1,16)]}
    ty_dic['exp'][-1] = 1
    num_choro = [i for i in range(8)]
    for n in range(num_iteration):
        len_pop_chro = len(population)                 # 繁殖
        for i in range(len_pop_chro):                       # population_chro[0][0]南 population_chro[0][1]北
            population_children = copy.deepcopy(population[i])
            ran_times = np.random.randint(1,6)
            for j in range(ran_times):
                ran_ty = np.random.random()
                len_n = len(str(n))
                if ran_ty/len_n > 0.1:
                    ty = 'liner'
                else:
                    ty = 'exp'
                ran_li = ty_dic[ty]
                ran_num_change = np.random.random()
                pos = bisect.bisect_left(ran_li, ran_num_change)
                num = pos + 1
                selected = random.sample(num_choro, 2)
                selected_1 = copy.deepcopy(population_children[selected[0]])
                selected_2 = copy.deepcopy(population_children[selected[1]])
                s_1_no = random.sample([i for i in range(16)],num)
                s_2_no = random.sample([i for i in range(16)],num)
                for se in range(num):
                    population_children[selected[0]][s_1_no[se]] = selected_2[s_2_no[se]]
                    population_children[selected[1]][s_2_no[se]] = selected_1[s_1_no[se]]
                population.append(population_children)
                pass
        population_afmuta = mutation(population, class_lap_n, class_lap, mut_rate)  #变异
    pass

def mutation(population, class_lap_n, class_lap, mua_rate):
    for i in range(1, len(population)):
        mut_rand = [random.random() for ii in range(len(class_lap_n))]
        for j in range(len(mut_rand)):
            if mut_rand[j] < mua_rate:
                class_week = class_lap_n[j][3]
                class_hash = class_lap_n[j][6]
                i_j = ''
                for a in range(len(population[i])):
                    for b in range(len(population[i][a])):
                        if class_hash in population[i][a][b][1]:
                            i_j = (a, b)
                class_change_1 = [(ii, jj) for ii in range(len(population[i])) for jj in range(len(population[i][ii]))
                                  if sum(population[i][ii][jj][0]) == 0]
                class_change_hash = [item[6] for item in class_lap_n if item[3] == class_week]
                class_change_hash.remove(class_hash)
                class_change_2 = []
                for item in class_change_hash:
                    for ii in range(len(population[i])):
                        for jj in range(len(population[i][ii])):
                            if item in population[i][ii][jj][1]:
                                class_change_2.append((ii, jj))
                # class_change_2 = [(ii, jj) for ii in range(len(population[i])) for jj in range(len(population[i][ii])) for item in class_change_hash
                #                       if item in population[i][ii][jj][1]]
                class_change = class_change_1 + class_change_2
                c_c = random.sample(class_change, 1)[0]
                try:
                    if c_c in class_change_1:
                        population[i][c_c[0]][c_c[1]] = population[i][i_j[0]][i_j[1]]
                        population[i][i_j[0]][i_j[1]] = [[0 for i in range(18)],[]]
                    else:
                        ind = class_change_2.index(c_c)
                        class_hash_2 = class_change_hash[ind]
                        week_1 = [1 if any([population[i][c_c[0]][c_c[1]][0][it], class_week[it]]) == 1
                                                            else 0 for it in range(len(class_week))]
                        week_2 = [1 if any([population[i][i_j[0]][i_j[1]][0][it], class_week[it]]) == 1
                                                            else 0 for it in range(len(class_week))]
                        population[i][c_c[0]][c_c[1]][1].append(class_hash)
                        population[i][c_c[0]][c_c[1]][1].remove(class_hash_2)
                        population[i][i_j[0]][i_j[1]][1].append(class_hash_2)
                        population[i][i_j[0]][i_j[1]][1].remove(class_hash)
                        population[i][c_c[0]][c_c[1]][0] = week_1
                        population[i][i_j[0]][i_j[1]][0] = week_2
                except:
                    print('wrong')
                    pass
                pass
    return population


