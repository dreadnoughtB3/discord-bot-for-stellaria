import csv
import pandas as pd
import os
import sys
from datetime import timezone, timedelta, datetime

sys.path.append(os.path.join(os.path.dirname("data"), ".."))

from module.dice_roll import dice, multi_dice
from module.judge import is_range



# ?prop 財産登録コマンド
def property(id, world, max_money, now_money):
    timecount = "0"
    with open("data/property.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 同一のデータが登録されている
            if int(row["id"]) == id and row["world"] == world:
                return "```既に登録されています```"

    with open("data/property.csv", "a") as f:
        header = [
            "id", "world", "now_money", "max_money"
        ]
        writer = csv.DictWriter(f, header)
        data = {
            "id": id,
            "world": world,
            "now_money": now_money,
            "max_money": max_money
        }
        writer.writerow(data)

    return "```世界:{} 所持金(金庫を含む):{}／{}  | 登録完了```".format(world, now_money,max_money)


# ?mone 財産管理コマンド
def mone(id, world, value):
    result = ""
    with open("data/property.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        # データの探索
        for idx, row in enumerate(data):
            # 操作対象 同じidか判定
            if int(row["id"]) == id and row["world"] == world:
                # 所持金が0を下回る
                if int(row["now_money"]) + value < 0:
                    result = "```所持金が足りません```"
                # 所持金が最大値を超える
                elif int(row["now_money"]) + value > int(row["max_money"]):
                    result = "```所持金上限を超えます```"
                # 所持金を問題なく変動させる
                else:
                    row["now_money"] = str(int(row["now_money"]) + value)
                    data[idx]["now_money"] = str(int(row["now_money"]))
                    
                    # 結果の出力
                    result = "```所持金:{}/{}```".format(int(row["now_money"]),int(row["max_money"]))

                    # データの更新
                    with open("data/property.csv", "w") as f:
                        header = [
                                       "id", "world", "now_money", "max_money"    
                        ]
                        writer = csv.DictWriter(f, header)
                        writer.writeheader()
                        writer.writerows(data)

    return result

