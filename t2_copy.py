import json
import pickle

import numpy as np

np.set_printoptions(suppress=True)


def getPR(A, x_0, min_delta):
    count = 0
    while (True):
        np.set_printoptions(precision=6)
        y = np.dot(A, x_0)
        x_1 = np.dot(1 / max(y), y)
        e = max(np.abs(x_1 - x_0))
        if (e < min_delta):
            return x_0

        x_0 = x_1
        count = count + 1
        if count > 1000:
            return x_0

        # print(e)


def get_PR(file_path):
    dic = []

    # with open(file_path, 'r') as f:
    #     data = f.readlines()
    #
    #     for d in data:
    #         di = []
    #         d1 = list(d.split(' '))
    #         d1.remove('\n')
    #         dic.append(d1)


    with open(file_path, 'rb') as f:
        dic = pickle.load(f)
        # print(data)

    len_total = 0

    for i in dic:
        len_total = len(i)
        # print(len(i), i)
    matrix = np.array(dic)
    matrix = matrix.astype(float)
    # print(matrix)
    M = matrix
    x_0 = np.ones((len_total,))
    # 计算有向图的一般转移矩阵A
    # d = 0.85
    E = np.ones((len_total, len_total))
    A = np.dot(d, M) + np.dot((1 - d) / len_total, E)
    min_delta = 0.0000001  # 精度
    PR = getPR(A, x_0, min_delta)
    return PR


if __name__ == '__main__':

    a_list = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    d_list = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]


    for d in d_list:

        with open('../pkl_data/Math.json', 'r') as rf:
            datas = json.load(rf)
            print("GET JSON FILE FINISHED!", end='\n\n')
        flag = 0
        for data in datas:
            flag += 1

            # if flag < 18:
            #     continue
            data_name = data['proj']
            # if data_name != 'Math26' and data_name != 'Math27':
            #     continue
            method = data['methods']
            lines = data['lines']
            mutation = data['mutation']
            ftest = data['ftest']
            rtest = data['rtest']
            print(data_name)
            len_method = len(data['methods'])
            len_lines = len(data['lines'])
            len_mutation = len(data['mutation'])
            len_ftest = len(data['ftest'])
            len_rtest = len(data['rtest'])



            filepath = f'P_FIN_matrix\Math\{data_name}_matrix.pkl'
            try:
                FIN_matrix_PR = get_PR(filepath)
            except:
                continue

            filepath = f'F_FIN_matrix\Math\{data_name}_matrix.pkl'
            try:
                FIN_matrix_PR2 = get_PR(filepath)
            except:
                continue

            print(FIN_matrix_PR.round(6))
            for a in a_list:
                pr_s = ''
                print(len_method, len_lines, len_mutation, len_rtest, len_ftest)
                pr_s += (str(len_method) + " " + str(len_lines) + " " + str(len_mutation) + " " + str(
                    len_rtest) + " " + str(
                    len_ftest) + '\n')
                for p in range(len_method+len_lines+len_mutation):
                    pr_s += (str(FIN_matrix_PR2[p]-a*FIN_matrix_PR[p]) + ' ')
                # for pr in FIN_matrix_PR.round(6):
                #     pr_s += (str(pr) + ' ')
                pr_s += '\n'




                ans_path = f'FIN_PR\Math\{data_name}_PR_a={a}_d={d}.txt'
                with open(ans_path, 'w') as anf:
                    anf.write(pr_s)
