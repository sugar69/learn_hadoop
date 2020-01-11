import sqlite3
from sklearn.linear_model import LogisticRegression as LR
import numpy as np

conn = sqlite3.connect('hadoop.db')
cursor = conn.cursor()


def learn_db():
    candidates_C = [0.001, 0.01, 0.1, 1.0, 2.0]
    best_C = None
    best_C_score = 0
    before_learn_tuple_n = []
    before_answer_tuple_n = []
    before_learn_tuple_zs = []
    combine_flag = 0  # 0 = false, 1 = true

    # release1とrelease53
    try:
        # 訓練データと検証データ
        cursor.execute('SELECT ns, nd, nf, entrophy, la, ld, lt, fix, ndev, age, nuc, exp, rexp, sexp '
                       'FROM data WHERE author_date_flag = %s' % str(1))
        learn_tuple = cursor.fetchall()
        cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(1))
        answer_tuple = cursor.fetchall()

        # テストデータ
        cursor.execute('SELECT ns, nd, nf, entrophy, la, ld, lt, fix, ndev, age, nuc, exp, rexp, sexp '
                       'FROM data WHERE author_date_flag = %s' % str(53))
        test_learn_tuple = cursor.fetchall()
        cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(53))
        test_answer_tuple = cursor.fetchall()

        # 各パラメータを調整する処理
        # 訓練データと検証データ
        learn_tuple_n = learn_tuple_processing(learn_tuple)
        answer_tuple_n = answer_tuple_processing(answer_tuple)
        learn_tuple_zs = learn_tuple_zscore(learn_tuple_n)

        train_learn_tuple = learn_tuple_zs[:int(0.8 * len(learn_tuple_zs))]  # 訓練データの説明変数
        train_answer_tuple = answer_tuple_n[:int(0.8 * len(learn_tuple_zs))]  # 訓練データの正解データ
        valid_learn_tuple = learn_tuple_zs[int(0.8 * len(learn_tuple_zs)):int(1.0 * len(learn_tuple_zs))]  # 検証データの説明変数
        valid_answer_tuple = answer_tuple_n[
                             int(0.8 * len(learn_tuple_zs)):int(1.0 * len(learn_tuple_zs))]  # 検証データの正解データ

        # テストデータ
        test_learn_tuple_n = learn_tuple_processing(test_learn_tuple)
        test_answer_tuple_n = answer_tuple_processing(test_answer_tuple)
        test_learn_tuple_zs = learn_tuple_zscore(test_learn_tuple_n)

        print('challenge 53')

        for candidate in candidates_C:
            clf = LR(random_state=0, C=candidate).fit(train_learn_tuple, train_answer_tuple)
            score = clf.score(valid_learn_tuple, valid_answer_tuple)
            print("candidate: {0}, score: {1}".format(candidate, score))
            if score > best_C_score:
                best_C = candidate
                best_C_score = score

        clf = LR(random_state=0, C=best_C).fit(train_learn_tuple, train_answer_tuple)
        score = clf.score(test_learn_tuple_zs, test_answer_tuple_n)
        print("best score: {0}".format(score))

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

    try:
        # 訓練データと検証データに分ける工程も必要？　テストデータは次のリリース区間のコミットで良いはず
        for loop_num in range(53, 326):  # 53, 326  test = 78:85
            # 訓練データと検証データ
            cursor.execute('SELECT ns, nd, nf, entrophy, la, ld, lt, fix, ndev, age, nuc, exp, rexp, sexp '
                           'FROM data WHERE author_date_flag = %s' % str(loop_num))
            learn_tuple = cursor.fetchall()
            cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(loop_num))
            answer_tuple = cursor.fetchall()

            # テストデータ
            cursor.execute('SELECT ns, nd, nf, entrophy, la, ld, lt, fix, ndev, age, nuc, exp, rexp, sexp '
                           'FROM data WHERE author_date_flag = %s' % str(loop_num+1))
            test_learn_tuple = cursor.fetchall()
            cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(loop_num+1))
            test_answer_tuple = cursor.fetchall()

            # 各パラメータを調整する処理
            # 訓練データと検証データ
            learn_tuple_n = learn_tuple_processing(learn_tuple)
            if len(learn_tuple_n) <= 2:  # 前のリリース区間のデータをトレーニングデータにする
                learn_tuple_n += before_learn_tuple_n
                combine_flag = 1
            answer_tuple_n = answer_tuple_processing(answer_tuple)
            if len(answer_tuple_n) <= 2:  # 前のリリース区間のデータをトレーニングデータにする
                answer_tuple_n += before_answer_tuple_n
                combine_flag = 1
            # もし、answer_tuple_nの中身が全て0か1のとき、前のコミットを足す
            if (sum(answer_tuple_n) == len(answer_tuple_n) or sum(answer_tuple_n) == 0) and combine_flag == 0:
                learn_tuple_n = learn_tuple_n + before_learn_tuple_n
                answer_tuple_n = answer_tuple_n + before_answer_tuple_n
                combine_flag = 1
            learn_tuple_zs = learn_tuple_zscore(learn_tuple_n)

            # もし、正解データの最初から80%までの値全てがTrueかFalseだったら、一つ前のコミットのデータを全て足す
            if (sum(answer_tuple_n[:int(0.8 * len(learn_tuple_zs))]) == len(answer_tuple_n[:int(0.8 * len(learn_tuple_zs))]) or sum(answer_tuple_n[:int(0.8 * len(learn_tuple_zs))]) == 0) and combine_flag == 0:
                learn_tuple_zs = learn_tuple_zs + before_learn_tuple_zs
                answer_tuple_n = answer_tuple_n + before_answer_tuple_n
                combine_flag == 1

            train_learn_tuple = learn_tuple_zs[:int(0.8 * len(learn_tuple_zs))]  # 訓練データの説明変数
            train_answer_tuple = answer_tuple_n[:int(0.8 * len(learn_tuple_zs))]  # 訓練データの正解データ
            valid_learn_tuple = learn_tuple_zs[int(0.8 * len(learn_tuple_zs)):int(1.0 * len(learn_tuple_zs))]  # 検証データの説明変数
            valid_answer_tuple = answer_tuple_n[int(0.8 * len(learn_tuple_zs)):int(1.0 * len(learn_tuple_zs))]  # 検証データの正解データ

            # テストデータ
            test_learn_tuple_n = learn_tuple_processing(test_learn_tuple)
            if len(test_learn_tuple_n) == 0:
                before_learn_tuple_n = learn_tuple_n
                before_answer_tuple_n = answer_tuple_n
                continue
            test_answer_tuple_n = answer_tuple_processing(test_answer_tuple)
            test_learn_tuple_zs = learn_tuple_zscore(test_learn_tuple_n)

            print('training', loop_num, ': testing', loop_num+1)

            # もし、全てTrueかFalseだったら、一つ前のコミットのデータを全て足す(この処理まずいかも)
#            if (sum(train_answer_tuple) == len(train_answer_tuple) or sum(train_answer_tuple) == 0) and combine_flag == 0:
#                train_learn_tuple += before_learn_tuple_n
#                train_answer_tuple += before_answer_tuple_n
#                combine_flag == 1
            for candidate in candidates_C:
                clf = LR(random_state=0, C=candidate).fit(train_learn_tuple, train_answer_tuple)
                score = clf.score(valid_learn_tuple, valid_answer_tuple)
                print("candidate: {0}, score: {1}".format(candidate, score))
                if score > best_C_score:
                    best_C = candidate
                    best_C_score = score

            clf = LR(random_state=0, C=best_C).fit(train_learn_tuple, train_answer_tuple)
            score = clf.score(test_learn_tuple_zs, test_answer_tuple_n)
            print("best score: {0}".format(score))

            if before_learn_tuple_n != learn_tuple_n:
                before_learn_tuple_n = learn_tuple_n
                before_answer_tuple_n = answer_tuple_n
                before_learn_tuple_zs = learn_tuple_zs

            combine_flag = 0

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
            if standard_deviation_list[element] != 0:
                temp_list.append((learn_tuple_n[loop][element] - mean_list[element]) / standard_deviation_list[element])
            elif standard_deviation_list[element] == 0:
                temp_list.append(learn_tuple_n[loop][element] - mean_list[element])
        learn_tuple_zs.append(temp_list)


    return learn_tuple_zs

learn_db()

# データベースの中身はいじる予定がないので必要ない？　その他の出力方法が必要になるははず
conn.commit()

# 接続を閉じる
conn.close()