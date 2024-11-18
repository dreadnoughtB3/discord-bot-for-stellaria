import matplotlib.pyplot as plt
import japanize_matplotlib
import os
import sys

sys.path.append(os.path.join(os.path.dirname("module"), ".."))
sys.path.append(os.path.join(os.path.dirname("output"), ".."))

from module.dice_roll import dice
from datetime import timezone, timedelta, datetime


# 交易表の生成
def trade_make():
    # 金額表
    data = [[
        str(dice(300)),
        str(dice(300)),
        str(dice(300)),
        str(dice(300)),
        str(dice(300)),
        str(dice(300))
    ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300)),
                str(dice(300))
            ],
            [
                "○" if dice(100) > 30 else "×", "○" if dice(100) > 30 else "×",
                "○" if dice(100) > 30 else "×", "○" if dice(100) > 30 else "×",
                "○" if dice(100) > 30 else "×", "○" if dice(100) > 30 else "×"
            ]]
    # 行ラベル
    col = ["AIL", "AME", "L.L.L", "INA", "RUZ", "N.U"]
    # 列ラベル
    row = [
        ">衣類", ">酒類", ">機械", ">資源", ">武器", ">装飾", ">食料", ">書籍", ">絵画", ">宝石",
        "[ギャング]"
    ]
    # グラフの初期化
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.axis("off")
    # 株価グラフの描画
    ax.table(
        cellText=data,
        colLabels=col,
        rowLabels=row,
        loc="center",
        cellLoc="center",
        colColours=["gold", "gold", "gold", "gold", "gold", "gold"])
    # 余白の調整
    plt.subplots_adjust(left=0.18, right=0.97, bottom=0, top=0.93)
    # タイトルの描画
    plt.title("ノクターン - 国際市場:", fontsize=20, color="red", x=0.35, y=0.94)
    # 日時の描画
    now = datetime.now(timezone(timedelta(hours=+10),
                                'JST')).strftime("%Y/%m/%d")
    plt.text(0.75, 0.96, now, transform=ax.transAxes)
    # グラフの保存
    fig.savefig("output/trade.jpg")

    # メモリの解放
    plt.clf()
    plt.close()