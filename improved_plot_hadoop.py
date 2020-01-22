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

            if loop_num == 62 or loop_num == 72 or loop_num == 79 or loop_num == 91 or loop_num == 99 or loop_num == 132 or loop_num == 138 or loop_num == 139 or loop_num == 148 or loop_num == 155 or loop_num == 156 or loop_num == 158 or loop_num == 162 or loop_num == 164 or loop_num == 165 or loop_num == 172 or loop_num == 173 or loop_num == 180 or loop_num == 193 or loop_num == 194 or loop_num == 201:
                x_success.append(len(x_tuple))
                y_success.append(rate_true)
            else:
                x_failure.append(len(x_tuple))
                y_failure.append(rate_true)



    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

    p1 = plt.scatter(x_success, y_success, c="blue")
    p2 = plt.scatter(x_failure, y_failure, c="red")
    plt.title("every release")
    plt.xlabel("number of commit")
    plt.ylabel("contains_bug rate")
    plt.legend([p1, p2], ["success data", "failure data"], fontsize=20, loc=1, title="LABEL NAME", prop={'size': 6})
    plt.show()

plot_data()

# データベースの中身はいじる予定がないので必要ない？　その他の出力方法が必要になるははず
conn.commit()

# 接続を閉じる
conn.close()