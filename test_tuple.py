import sqlite3

conn = sqlite3.connect('hadoop.db')
cursor = conn.cursor()

def learn_db():

    try:
        for loop_num in range(53, 55):
            fixes_tuple_legal = []
            temp_str = ''

            cursor.execute('SELECT ns, nd, nf, entrophy, la, ld, lt, fix, ndev, age, nuc, exp, rexp, sexp '
                                        'FROM data WHERE author_date_flag = %s' % str(loop_num))
            learn_tuple = cursor.fetchall()
            cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(loop_num))
            answer_tuple = cursor.fetchall()
            cursor.execute('SELECT fixes FROM data WHERE author_date_flag = %s' % str(loop_num))
            fixes_tuple = cursor.fetchall()
            cursor.execute('SELECT commit_hash FROM data WHERE author_date_flag = %s' % str(loop_num))
            hash_tuple = cursor.fetchall()
#            print(fixes_tuple)
#            print(type(fixes_tuple))
#            print(type(fixes_tuple[1]))
#            print(learn_tuple)
#            print(len(learn_tuple))
#           print(type(learn_tuple))
#            print(answer_tuple)
#           print(type(answer_tuple))


            learn_tuple_n = learn_tuple_processing(learn_tuple)
            answer_tuple_n = answer_tuple_processing(answer_tuple)
            learn_tuple_zs = learn_tuple_zscore(learn_tuple_n)

            print('before:', len(learn_tuple_zs))

            # fixesを文字列のリストに変換する
            for loop in range(0, len(fixes_tuple)):
                fixes_tuple_s = []
                temp_tuple = []
                if fixes_tuple[loop][0] == '':
                    fixes_tuple_legal.append(['', ])
                else:
                    fixes_tuple_s.append(fixes_tuple[loop][0].split(", "))
                for element in range(0, len(fixes_tuple_s)):
                    if len(fixes_tuple_s[element]) == 1:
                        temp_str = fixes_tuple_s[element][0]
                        fixes_tuple_legal.append(temp_str[2:-2])
                    elif len(fixes_tuple_s[element]) == 2:
                        temp_str = fixes_tuple_s[element][0]
                        temp_tuple.append(temp_str[2:-1])
                        temp_str = fixes_tuple_s[element][1]
                        temp_tuple.append(temp_str[1:-2])
                        fixes_tuple_legal.append(temp_tuple)
                    else:
                        temp_str = fixes_tuple_s[element][0]
                        temp_tuple.append(temp_str[2:-1])
                        for tuple_len in range(1, len(fixes_tuple_s[element]) - 1):
                            temp_str = fixes_tuple_s[element][tuple_len]
                            temp_tuple.append(temp_str[1:-1])
                        temp_str = fixes_tuple_s[element][len(fixes_tuple_s[element]) - 1]
                        temp_tuple.append(temp_str[1:-2])
                        fixes_tuple_legal.append(temp_tuple)
            #                print('fix s :', fixes_tuple_s)
            #            print('00', fixes_tuple_s[0][0])
            #            print('10', fixes_tuple_s[1][0])
            #            print(fixes_tuple_legal)

            len_tuple = len(answer_tuple_n)
            delete_target = []
            for loop_bugs_check in range(0, len_tuple):
                fix_flag = 0
                if answer_tuple_n[loop_bugs_check] == 1:
                    for loop_fixes in range(0, len(fixes_tuple_legal[loop_bugs_check])):
                        for loop_hash in range(loop_bugs_check, len_tuple):
                            if hash_tuple[loop_hash] == fixes_tuple_legal[loop_bugs_check][loop_fixes]:
                                fix_flag = 1
                    if fix_flag == 0:
                        delete_target.append(loop_bugs_check)

            for delete_num in range(0, len(delete_target)):
                del learn_tuple_zs[delete_target[delete_num]]
                del answer_tuple_n[delete_target[delete_num]]
                for del_loop_num in range(delete_num + 1, len(delete_target)):
                    delete_target[del_loop_num] -= 1


            print('after:', len(learn_tuple_zs))


            print(learn_tuple_n)
            print(learn_tuple_zs)
            print(answer_tuple_n)
            print('---------------split---------------------')

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

# True,Falseを0,1に変換し、数値はfloat型に変換する
def learn_tuple_processing(learn_tuple):
    learn_tuple_n = []
    num_list = len(learn_tuple)
    for loop in range(0, num_list):
        temp_list = []
        for element in range(0, 14):
            if learn_tuple[loop][element] == 'True':
                temp_list.append(1)
            elif learn_tuple[loop][element] == 'False':
                temp_list.append(0)
            else:
                temp_float = float(learn_tuple[loop][element])
                temp_list.append(temp_float)
        learn_tuple_n.append(temp_list)

    return learn_tuple_n

def answer_tuple_processing(answer_tuple):
    answer_tuple_n = []
    num_list = len(answer_tuple)
    for loop in range(0, num_list):
        if answer_tuple[loop][0] == 'True':
            answer_tuple_n.append(1)
        elif answer_tuple[loop][0] == 'False':
            answer_tuple_n.append(0)
    return answer_tuple_n

def learn_tuple_zscore(learn_tuple_n):
    learn_tuple_zs = []
    standard_deviation_list = []
    mean_list = []
    variance_list = []

    # 平均のリストを作成
    for element in range(0, 14):
        temp_mean = 0
        for loop in range(0, len(learn_tuple_n)):
            temp_mean += learn_tuple_n[loop][element]
        mean_list.append(temp_mean / len(learn_tuple_n))

    # 標準偏差のリストを作成
    for element in range(0, 14):
        temp_variance = 0
        for loop in range(0, len(learn_tuple_n)):
            temp_variance += (learn_tuple_n[loop][element] - mean_list[element])**2
        variance_list.append(temp_variance/len(learn_tuple_n))
        standard_deviation_list.append(variance_list[element]**0.5)

    # z-scoreの化
    for loop in range(0, len(learn_tuple_n)):
        temp_list = []
        for element in range(0, 14):
            temp_list.append((learn_tuple_n[loop][element] - mean_list[element]) / standard_deviation_list[element])
        learn_tuple_zs.append(temp_list)


    return learn_tuple_zs

learn_db()

# データベースの中身はいじる予定がないので必要ない？　その他の出力方法が必要になるははず
conn.commit()

# 接続を閉じる
conn.close()