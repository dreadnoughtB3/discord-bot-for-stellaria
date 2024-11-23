import csv
import numpy as np
import matplotlib.pyplot as plt
import discord
import japanize_matplotlib


from modules.dice_roll import dice
from datetime import timezone, timedelta, datetime


# 株価更新
def stock_make():
    embed_f = stock_module(
        "data/stock_f.csv",
        "Asgaria Stock Exchange - Report",
        "アスガリア証券取引所:",
        "ファンタジア - アスガリア証券取引所",
        "outputs/stock_f.jpg",
    )
    embed_n = stock_module(
        "data/stock_n.csv",
        "New Saint City Stock Exchange - Report",
        "NCSE総合指数:",
        "ノクターン - NCSE総合指数",
        "outputs/stock_n.jpg",
    )

    return embed_f, embed_n


# 株価グラフと付加情報の生成
def stock_module(data_path, emb_title, emb_description, graph_title, output_path):
    # 株グラフの作成
    x = np.linspace(24, 0, 25)
    stock_y = []
    economy_y = []
    # データ読み込み data_path: data/stock_f.csv
    with open(data_path) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i == 0:
                stock_y = [int(item) for item in row]
            else:
                economy_y = [int(item) for item in row]
            i += 1
            count = economy_y[-3:-1]

        # 通常
        if economy_y[-1] == 50:
            today_stock = dice(100) + 20
            today_cost = "±0%"
            # 不景気
            if today_stock <= 40:
                today_economy = 25
            # 好景気
            elif today_stock >= 100:
                today_economy = 75
            # 通常
            else:
                today_economy = 50
        # 不景気
        if economy_y[-1] == 25:
            today_stock = dice(100) - 30
            today_cost = "-10%"
            # 恐慌
            if today_stock <= 30:
                today_economy = 0
            # 通常
            elif today_stock >= 60:
                today_economy = 50
            else:
                # 不景気
                today_economy = 25
        # 恐慌
        if economy_y[-1] == 0:
            today_stock = dice(100) - 40
            today_cost = "-20%"
            # 3日間継続
            if economy_y[-2] == 0 and economy_y[-3] == 0:
                # 通常
                if today_stock >= 35:
                    today_economy = 50
                # 大恐慌
                elif today_stock <= 20:
                    today_economy = -25
            else:
                # 恐慌継続
                today_economy = 0

        # 大恐慌
        if economy_y[-1] == -25:
            today_stock = dice(100) - 50
            today_cost = "-30%"
            # 3日間継続
            if economy_y[-2] == -25 and economy_y[-3] == -25:
                # 通常
                if today_stock >= 30:
                    today_economy = 50
                # 大恐慌
                else:
                    today_economy = -25
            else:
                today_economy = -25
        # 好景気
        if economy_y[-1] == 75:
            today_stock = dice(100) + 30
            today_cost = "+30%"

            # 3日間継続
            if economy_y[-2] == 75 and economy_y[-3] == 75:
                # 通常
                today_economy = 50
            else:
                # バブル景気
                if today_stock >= 120:
                    today_economy = 100
                else:
                    # 好景気
                    today_economy = 75

        # バブル景気
        if economy_y[-1] == 100:
            today_stock = dice(100) + 50
            today_cost = "+50%"

            # 3日間継続
            if economy_y[-2] == 100 and economy_y[-3] == 100:
                # 通常
                today_economy = 50
            else:
                # 恐慌
                if today_stock <= 70:
                    today_economy = 0
                else:
                    # バブル景気
                    today_economy = 100

        # 景気の更新
        stock_y = stock_y[1:]
        stock_y.append(today_stock)
        # 景気の更新
        economy_y = economy_y[1:]
        economy_y.append(today_economy)
        # 本日の株価情報の埋め込みを出力
        embed = discord.Embed(title=emb_title, description=emb_description)

        if economy_y[-2] == -25:
            economy = "大恐慌 (" + str(count.count(-25) + 1) + "日目)"
        elif economy_y[-2] == 0:
            economy = "恐慌(" + str(count.count(0) + 1) + "日目)"
        elif economy_y[-2] == 25:
            economy = "不景気"
        elif economy_y[-2] == 50:
            economy = "通常"
        elif economy_y[-2] == 75:
            economy = "好景気 (" + str(count.count(75) + 1) + "日目)"
        elif economy_y[-2] == 100:
            economy = "バブル (" + str(count.count(100) + 1) + "日目)"
        if today_economy == -25:
            tomorrow_economy = "大恐慌"
        elif today_economy == 0:
            tomorrow_economy = "恐慌"
        elif today_economy == 25:
            tomorrow_economy = "不景気"
        elif today_economy == 50:
            tomorrow_economy = "通常"
        elif today_economy == 75:
            tomorrow_economy = "好景気"
        elif today_economy == 100:
            tomorrow_economy = "バブル"
        embed.add_field(
            name="", value="```――――――――――📊経済情報――――――――――```", inline=False
        )
        embed.add_field(name="```経済状況:```", value=economy, inline=True)
        embed.add_field(
            name="```次回の経済情勢:```", value=tomorrow_economy, inline=True
        )
        embed.add_field(
            name="", value="```―――――――🪙株価・物価情報―――――――```", inline=False
        )
        embed.add_field(
            name="```現在株価:```", value=str(today_stock) + "G", inline=True
        )
        embed.add_field(name="```物価変動:```", value=today_cost, inline=True)

    # データ更新
    with open(data_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(stock_y)
        writer.writerow(economy_y)
    # グラフの初期化
    fig, ax = plt.subplots(figsize=(9, 5))
    # 株価グラフの描画
    ax.plot(x, stock_y, label="株価")
    ax.fill_between(x, stock_y, color="lightblue", alpha=0.5)
    # 経済グラフの描画
    ax.plot(x, economy_y, marker=".", markersize=10, label="経済")
    # 横軸の目盛りの設定
    ax.set_xticks(np.linspace(24, 0, 25))
    ax.set_xlim(24, 0)
    # 縦軸の目盛りの設定
    ax.set_yticks(np.linspace(-75, 150, 10))
    ax.tick_params(axis="y", colors="red")
    ax.set_ylim(-75, 150)
    # グリッドの設定
    ax.grid()
    # 余白の調整
    plt.subplots_adjust(left=0.05, right=0.9, bottom=0.07, top=0.9)
    # タイトルの描画
    plt.title(graph_title, fontsize=20, color="red", x=0.4, y=1)
    # 経済グラフの目盛りの描画
    plt.text(-0.3, 98, "バブル", fontsize=10)
    plt.text(-0.3, 73, "好景気", fontsize=10)
    plt.text(-0.3, 48, "通常", fontsize=10)
    plt.text(-0.3, 23, "不景気", fontsize=10)
    plt.text(-0.3, -2, "恐慌", fontsize=10)
    plt.text(-0.3, -27, "大恐慌", fontsize=10)
    # 凡例の描画
    plt.legend(bbox_to_anchor=(1, 1.13), loc="upper left", fontsize=10)
    # 日時の描画
    now = datetime.now(timezone(timedelta(hours=+9), "JST")).strftime("%Y/%m/%d")
    plt.text(5, 155, now)
    # グラフの保存
    fig.savefig(output_path)

    # メモリの解放
    plt.clf()
    plt.close()

    # 出力
    return embed
