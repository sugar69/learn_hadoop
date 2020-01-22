import sqlite3
from sklearn.linear_model import LogisticRegression as LR
import sklearn.metrics as SKMET
import numpy as np

conn = sqlite3.connect('hadoop.db')
cursor = conn.cursor()

def print_fixes():
    # release1とrelease53
    try:
        fixes_tuple_legal = []
        cursor.execute('SELECT fixes FROM data WHERE author_date_flag = %s' % str(1))
        fixes_tuple = cursor.fetchall()

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

        print('1:\n', fixes_tuple_legal, '\n')

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])


    try:
        fixes_tuple_legal = []
        # 訓練データと検証データに分ける工程も必要？　テストデータは次のリリース区間のコミットで良いはず
        for loop_num in range(53, 326):  # 53, 326  test = 78:85
            fixes_tuple_legal = []
            cursor.execute('SELECT fixes FROM data WHERE author_date_flag = %s' % str(loop_num))
            fixes_tuple = cursor.fetchall()

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

            print(loop_num, ':\n', fixes_tuple_legal, '\n')

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

print_fixes()

# データベースの中身はいじる予定がないので必要ない？　その他の出力方法が必要になるははず
conn.commit()

# 接続を閉じる
conn.close()