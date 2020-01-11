import sqlite3

conn = sqlite3.connect('hadoop.db')
cursor = conn.cursor()

def learn_db():
    try:
        for loop_num in range(53, 55):
            cursor.execute('SELECT ns, nd, nf, entrophy, la, ld, lt, fix, ndev, age, nuc, exp, rexp, sexp '
                                        'FROM data WHERE author_date_flag = %s' % str(loop_num))
            learn_tuple = cursor.fetchall()
            cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(loop_num))
            answer_tuple = cursor.fetchall()
            print(learn_tuple)
#            print(len(learn_tuple))
#           print(type(learn_tuple))
            print(answer_tuple)
#           print(type(answer_tuple))

            learn_tuple_n = learn_tuple_processing(learn_tuple)
            answer_tuple_n = answer_tuple_processing(answer_tuple)
            learn_tuple_zs = learn_tuple_zscore(learn_tuple_n)
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