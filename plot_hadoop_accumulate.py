import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('hadoop.db')
cursor = conn.cursor()

def plot_data():
    x_success = []
    y_success = []
    x_failure = []
    y_failure = []
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

        x_success.append(len(x_tuple))
        y_success.append(rate_true)

        sum_x = x_tuple

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

    try:
        for loop_num in range(53, 326):
            cursor.execute('SELECT fix FROM data WHERE author_date_flag = %s' % str(loop_num))
            x_tuple = cursor.fetchall()
            cursor.execute('SELECT contains_bug FROM data WHERE author_date_flag = %s' % str(loop_num))
            y_tuple = cursor.fetchall()
            sum_x += x_tuple

            true_num = 0

            for element in range(0, len(y_tuple)):
                if y_tuple[element][0] == 'True':
                    true_num += 1

            if element == 0:
                continue

            rate_true = true_num / element

            if loop_num == 53 or loop_num == 55 or loop_num == 56 or loop_num == 59 or loop_num == 60 or loop_num == 64 or loop_num == 67 or loop_num == 70 or loop_num == 82 or loop_num == 94 or loop_num == 104 or loop_num == 105 or loop_num == 114 or loop_num == 115 or loop_num == 118 or loop_num == 119 or loop_num == 125 or loop_num == 126 or loop_num == 128 or loop_num == 135 or loop_num == 136 or loop_num == 153 or loop_num == 169 or loop_num == 176 or loop_num == 177 or loop_num == 224 or loop_num == 238 or loop_num == 262 or loop_num == 263 or loop_num == 265 or loop_num == 309 or loop_num == 312:
                x_failure.append(len(sum_x))
                y_failure.append(rate_true)
            else:
                x_success.append(len(sum_x))
                y_success.append(rate_true)



    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

    p1 = plt.scatter(x_success, y_success, c="blue")
    p2 = plt.scatter(x_failure, y_failure, c="red")
    plt.title("all of before release")
    plt.xlabel("number of commit")
    plt.ylabel("contains_bug rate")
    plt.legend([p1, p2], ["success data", "failure data"], fontsize=20, loc=1, title="LABEL NAME", prop={'size': 6})
    plt.show()

plot_data()

# データベースの中身はいじる予定がないので必要ない？　その他の出力方法が必要になるははず
conn.commit()

# 接続を閉じる
conn.close()