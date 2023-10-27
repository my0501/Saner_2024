import json
import os
import pickle
import re

import numpy as np



if __name__ == '__main__':

    with open('../pkl_data/Lang.json', 'r') as rf:
        datas = json.load(rf)
        print("GET JSON FILE FINISHED!", end='\n\n')
    num_flag = 0
    calls_msgs = ''
    for data in datas:
        data_name = data['proj']
        method = data['methods']
        lines = data['lines']
        mutation = data['mutation']
        ftest = data['ftest']
        rtest = data['rtest']

        len_method = len(data['methods'])
        len_lines = len(data['lines'])
        len_mutation = len(data['mutation'])
        len_ftest = len(data['ftest'])
        len_rtest = len(data['rtest'])
        print(len_method, len_lines, len_mutation, len_rtest, len_ftest)
        len_total = len_lines + len_rtest + len_ftest + len_mutation + len_method
        print("GET %s MESSAGE FINISHED!" % data_name, end='\n\n')
        print(method)
        method2method = {}
        method2lines = data['edge2']
        mutation2lines = data['edge12']
        lines2rtest = data['edge10']
        lines2ftest = data['edge']
        mutation2rtest = data['edge13']
        mutation2ftest = data['edge14']
        print("GET EDGES FINISHED!", end='\n\n')

        method_msg = []

        for m in method:
            Id = method[m]
            path = m.split('@')[0]
            me = m.split('@')[1]
            method_name = me.split('.')[0]
            method_canshu = list(me.split('.')[1].split(','))
            method_msg.append([Id,path,method_name,method_canshu])
        # print(method_msg)
        calls_msgs += data_name
        calls_msgs += ' * '
        fff = 0
        call_msgs = []
        for m in method:
            # this_call_msg
            this_call_msg = []
            # break
            fff = 0

            this_Id = method[m]
            this_path = m.split('@')[0]
            this_me = m.split('@')[1]
            this_method_name = this_me.split('.')[0]
            this_method_canshu = list(this_me.split('.')[1].split(','))
            # call_msg.append([this_Id])
            this_call_msg.append(this_Id)

            # print(m)
            path = m.split('@')[0]
            me = m.split('@')[1]
            # print(method[m])
            # print(data_name)
            Id = re.sub('\D', '', data_name)
            # print(s1)
            exist = os.path.exists(f'../../../d4j/Lang_code/Lang-{Id}b/src/main/java/{path}')
            if exist:
                try:
                    with open(f'../../../d4j/Lang_code/Lang-{Id}b/src/main/java/{path}', errors='ignore') as code_f:
                        lines = code_f.readlines()
                        # print(lines[0])
                except Exception as e:
                    print(f'../../../d4j/Lang_code/Lang-{Id}b/src/main/java/{path}')
                    fff = 1
                    print(e)
                    break
            else:
                exist = os.path.exists(f'../../../d4j/Lang_code/Lang-{Id}b/src/java/{path}')
                try:
                    with open(f'../../../d4j/Lang_code/Lang-{Id}b/src/java/{path}', errors='ignore') as code_f:
                        lines = code_f.readlines()
                        # print(lines[0])
                except Exception as e:
                    print(f'../../../d4j/Lang_code/Lang-{Id}b/src/java/{path}')
                    fff = 1
                    print(e)
                    break
            # for line in lines:
            this_call = []
            for line_num in range(len(lines)):
                code_line = lines[line_num].replace(' ', '').replace('\n', '')
                code_line = code_line + lines[line_num + 1].replace(' ', '')
                # print()
                m1 = me.split('.')[0]
                m2 = me.split('.')[1]

                if m1 in code_line and m2 in code_line:
                    fff = 2
                    # 找到方法的起始位置：

                    # 使用 括号匹配 方法进行寻找 方法（函数）范围
                    flag_kuohao = 0
                    for line_numm in range(line_num,len(lines)):
                        for c in lines[line_numm]:
                            if c == '{':
                                flag_kuohao = flag_kuohao + 1
                            if c == '}':
                                flag_kuohao = flag_kuohao - 1

                        # 找 其他怀疑方法
                        m_list = method_msg
                        # print(m_list)
                        # m_list = m_list.remove([this_Id,this_path,this_method_name,this_method_canshu])
                        # print(m_list)

                        this_codeline = lines[line_numm]
                        judge = this_codeline.replace(' ', '')
                        if judge[0] == '/' or judge[0] == '*':
                            continue
                        canshu_num = 0
                        for douhao in judge:
                            if douhao == ',':
                                canshu_num += 1
                        for m_l in m_list:
                            if m_l[2] in this_codeline and len(m_l[3]) == canshu_num + 1 and m_l[2] != this_method_name:
                                # 对应方法调用关系
                                # m_l - 被调用方法
                                # this_method - 调用方法
                                if m_l[0] not in this_call:
                                    this_call.append(m_l[0])
                                # print(this_call_msg)
                                print(this_method_name,m_l[2],m_l[3],this_codeline)
                        # call_msgs.append(call_msg)
                        # call_msg.clear()


                        if flag_kuohao == 0 and line_numm != line_num: # 方法结束内语句结束！
                            break



                    # print(code_line)
                    break
            this_call_msg.append(this_call)
            call_msgs.append(this_call_msg)
        calls_msgs = calls_msgs + str(call_msgs) + '\n'

                # print(code_line)
            # calls_msgs += '\n'

        if fff != 2:
            break
        # break
    print(calls_msgs)

    with open('Lang_M2M.txt','w') as f:
        f.write(calls_msgs)
