import csv
import os
import sys
from datetime import timezone, timedelta, datetime

sys.path.append(os.path.join(os.path.dirname("data"), ".."))


# ?weapon 登録コマンド
def weapons(id, weapons_name, max_ammunition, now_ammunition, max_durability, now_durability):
    with open("data/weapons.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 同一のデータが登録されている
            if int(row["id"]) == id:
                return "```既に登録されています```"

    with open("data/weapons.csv", "a") as f:
        header = [
            "id", "weapons_name", "max_ammunition", "now_ammunition", "max_durability", "now_durability"
        ]
        writer = csv.DictWriter(f, header)
        data = {
            "id": id,
            "weapons_name": weapons_name,
            "max_ammunition": max_ammunition,
            "now_ammunition": now_ammunition,
            "max_durability": max_durability,
            "now_durability": now_durability
        }
        writer.writerow(data)

    return "```メインウェポン:{} 弾数:{}／{} 耐久:{}／{} | 登録完了```".format(weapons_name, now_ammunition, max_ammunition, now_durability, max_durability)

# ?check 武器チェックコマンド
def check(id):
    result = ""
    with open("data/weapons.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        # データの探索
        for idx, row in enumerate(data):
            # 操作対象 同じidか判定
            if int(row["id"])==id:

                return "```メインウェポン:{} 弾数:{}／{} 耐久:{}／{} ```".format(row["weapons_name"], row["now_ammunition"], row["max_ammunition"], row["now_durability"], row["max_durability"])


# ?amm 弾数管理 
def amm(id, value):
    result = ""
    with open("data/weapons.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        # データの探索
        for idx, row in enumerate(data):
            # 操作対象 同じidか判定
            if int(row["id"]) == id:
                # 弾薬減少が0を下回る
                if int(row["now_ammunition"]) + value < 0:
                    result = "```弾薬が足りません```"
                # 弾薬増加が最大値を超える
                elif int(row["now_ammunition"]) + value > int(row["max_ammunition"]):
                    result = "```弾薬上限を超えます```"
                # 弾薬を問題なく変動させる
                else:
                    row["now_ammunition"] = str(int(row["now_ammunition"]) + value)
                    data[idx]["now_ammunition"] = str(int(row["now_ammunition"]))
                    
                    # 結果の出力
                    result = "```弾薬:{}/{}```".format(int(row["now_ammunition"]),int(row["max_ammunition"]))

                    # データの更新
                    with open("data/weapons.csv", "w") as f:
                        header = [
                            "id", "weapons_name", "max_ammunition", "now_ammunition","now_ammunition","max_durability","now_durability"                        
                        ]
                        writer = csv.DictWriter(f, header)
                        writer.writeheader()
                        writer.writerows(data)

    return result


#?dur 耐久管理
def dur(id, value):
    result = ""
    with open("data/weapons.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        for idx, row in enumerate(data):
            if int(row["id"]) == id:
                # 耐久が0を下回る
                if int(row["now_durability"]) + value < 0:
                    result = "```耐久が足りません```"
                # 耐久が最大値を超える
                elif int(row["now_durability"]) + value > int(row["max_durability"]):
                    result = "```耐久上限を超えています```"
                # 弾薬を問題なく変動させる
                else:
                    row["now_durability"] = str(int(row["now_durability"]) + value)
                    data[idx]["now_durability"] = str(int(row["now_durability"]))

                    # 結果の出力
                    result = "```耐久:{}/{}```".format(int(row["now_durability"]),int(row["max_durability"]))

                    #データの更新
                    with open("data/weapons.csv","w") as f:
                        header = [
                            "id","weapons_name","max_ammunition","now_ammunition","max_durability","now_durability"
                        ]
                        writer = csv.DictWriter(f, header)
                        writer.writeheader()
                        writer.writerows(data)

    return result