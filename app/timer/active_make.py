import csv
import numpy as np
import matplotlib.pyplot as plt
import discord
import japanize_matplotlib
import os
import sys

sys.path.append(os.path.join(os.path.dirname("data"), ".."))

from datetime import timezone, timedelta, datetime


# アクティブ更新
def active_update(members, now):
    message_num = 0
    user_num = 0
    # メッセージ数の読み込み
    with open("data/message", "r") as f:
        message_num = int(f.read())
    # メッセージ数の初期化
    with open("data/message", "w") as f:
        f.write("0")
    # ユーザー数の読み込み
    for member in members:
        user_num += 1
    # アクティブ情報読み込み
    with open("data/active.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    # アクティブ情報更新
    with open("data/active.csv", "w") as f:
        header = [
            "00:00", "01:00", "02:00", "03:00", "04:00",
            "05:00", "06:00", "07:00", "08:00", "09:00",
            "10:00", "11:00", "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00", "18:00", "19:00",
            "20:00", "21:00", "22:00", "23:00"
        ]
        # 新しい日付である
        if now == "00:00":
            for h in header:
                data[0][h] = "0"
                data[1][h] = "0"
        # 現在時刻のデータの更新    
        data[0][now] = str(message_num)
        data[1][now] = str(user_num)
        # データの書き込み
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(data)


# アクティブ表示
def active_make():
    # アクティブ情報読み込み
    with open("data/active.csv") as f:
        reader = csv.DictReader(f)
        data_str = [row for row in reader]
        message_list = [int(value) for value in data_str[0].values()]
        user_list = [int(value) for value in data_str[1].values()]
    # グラフの初期化
    fig, message_ax = plt.subplots(figsize=(9, 5))
    user_ax = message_ax.twinx()
    x = np.linspace(0, 23, 24)
    # メッセージ数グラフの描画
    message_ax.plot(x, message_list, label="メッセージ数", color="green")
    message_ax.fill_between(x, message_list, color="lightgreen", alpha=0.5)
    # ユーザー数グラフの描画
    user_ax.plot(x, user_list, label="ユーザー数", color="red")
    # 横軸の目盛りの設定
    message_ax.set_xticks(np.linspace(0, 24, 25))
    message_ax.set_xlim(0, 24)
    # 縦軸の目盛りの設定
    message_ax.tick_params(axis="y", colors="green")
    _, y_max = message_ax.get_ylim()
    message_ax.set_ylim(0, y_max)
    user_ax.tick_params(axis="y", colors="red")
    _, y_max = user_ax.get_ylim()
    user_ax.set_ylim(0, y_max)
    # グリッドの設定
    message_ax.grid()
    # 余白の調整
    plt.subplots_adjust(left=0.05, right=0.9, bottom=0.07, top=0.9)
    # タイトルの描画
    plt.title("Active Users and Messages", fontsize=20, x=0.4, y=1)
    # 凡例の描画
    h1, l1 = message_ax.get_legend_handles_labels()
    h2, l2 = user_ax.get_legend_handles_labels()
    plt.legend(h1 + h2,
               l1 + l2,
               bbox_to_anchor=(0.9, 1.13),
               loc="upper left",
               fontsize=10)
    # 日時の描画
    now = datetime.now(timezone(timedelta(hours=+9),
                                'JST')).strftime("%Y/%m/%d")
    plt.text(5, 155, now)
    # グラフの保存
    fig.savefig('output/active.jpg')

    # メモリの解放
    plt.clf()
    plt.close()

    # 埋め込みメッセージの作成
    embed = discord.Embed(title="Active User Report:" + now)
    embed.add_field(name="```アクティブユーザー数:```",
                    value=sum(user_list),
                    inline=True)
    embed.add_field(name="```ユーザーメッセージ数:```",
                    value=sum(message_list),
                    inline=True)

    return embed