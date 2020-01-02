import sqlite3
from sklearn.linear_model import LogisticRegression as LR
import numpy as np

conn = sqlite3.connect('hadoop.db')
cursor = conn.cursor()

def learn_db():
    try:
        # 1と53での比較処理を単発で入れてあげる必要がある
        # 訓練データと検証データに分ける工程も必要？　テストデータは次のリリース区間のコミットで良いはず
        for loop_num in ranage(53, 326):
            learn_tuple = cursor.execute('SELECT ns, nd, nf, entropy, la, ld, lt, fix, ndev, age, nuc, exp, rexp, sexp '
                                         'FROM data WHERE author_data_flag = %s' % str(loop_num))
            answer_tuple = cursor.execute('SELECT contains_bug FROM data WHERE author_data_flag = %s' % str(loop_num))
            clf = LR(random_state=0).fit(learn_tuple, answer_tuple)


    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])


# データベースの中身はいじる予定がないので必要ない？　その他の出力方法が必要になるははず
conn.commit()

# 接続を閉じる
conn.close()