import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('hadoop.db')
cursor = conn.cursor()

def plot_data():
    x = []
    y = []
    true_num = 0
    false_num = 0
    rate_true = 0

    try:
        cursor.execute('SELECT fix FROM data WHERE author_date_flag = %s' % str(1))
        x_tuple = cursor.fetchall()
        cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(1))
        y_tuple = cursor.fetchall()

        for element in range(0, len(y_tuple)):
            if y_tuple[element][0] == 'True':
                true_num += 1

        rate_true = true_num / element

        x.append(len(x_tuple))
        y.append(rate_true)

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

    try:
        for loop_num in range(53, 326):
            cursor.execute('SELECT fix FROM data WHERE author_date_flag = %s' % str(loop_num))
            x_tuple = cursor.fetchall()
            cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(loop_num))
            y_tuple = cursor.fetchall()

            true_num = 0

            for element in range(0, len(y_tuple)):
                if y_tuple[element][0] == 'True':
                    true_num += 1

            if element == 0:
                continue

            rate_true = true_num / element

            x.append(len(x_tuple))
            y.append(rate_true)

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

    plt.scatter(x, y)
    plt.title("This is a title")
    plt.xlabel("number of commit")
    plt.ylabel("contains_bug rate")
    plt.show()

plot_data()

# データベースの中身はいじる予定がないので必要ない？　その他の出力方法が必要になるははず
conn.commit()

# 接続を閉じる
conn.close()