import csv
import pandas as pd
import os
import sys
from datetime import timezone, timedelta, datetime

sys.path.append(os.path.join(os.path.dirname("data"), ".."))

from module.dice_roll import dice, multi_dice
from module.judge import is_range

# ?register 登録コマンド
def register(id, world, max_stamina, now_stamina,):
    timecount = "0"
    with open("data/register.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 同一のデータが登録されている
            if int(row["id"]) == id and row["world"] == world:
                return "```既に登録されています```"

    with open("data/register.csv", "a") as f:
        header = [
            "id", "world", "now_stamina", "max_stamina","timecount"
        ]
        writer = csv.DictWriter(f, header)
        data = {
            "id": id,
            "world": world,
            "now_stamina": now_stamina,
            "max_stamina": max_stamina,
            "timecount":timecount,
        }
        writer.writerow(data)

    return "```世界:{} スタミナ:{}  | 登録完了```".format(world, max_stamina)

def staminaup(row):
    if row["timecount"] >= 30:
        if row["max_stamina"] > row["now_stamina"]:
            return 1
    else:
        return 0

#スタミナ自動反映
def staminaloop():
    file_path = "data/register.csv"
    df = pd.read_csv(file_path,index_col=0) #read Date
    df["now_stamina"] = df.apply(lambda row:row["now_stamina"] + 1 if staminaup(row) else row["now_stamina"], axis=1)
    df["timecount"] = df["timecount"].apply(lambda x:0 if x >= 30 else x + 1) #60count reset　timecount(= x)が30以上ならば、0を代入。違えば、同じ値をそのまま代入する。
    df.to_csv(file_path)

    return


# ?sutaC スタミナチェックコマンド
def sutaC(id, world):
    result = ""
    with open("data/register.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        # データの探索
        for idx, row in enumerate(data):
            # 操作対象 同じidか判定
            if int(row["id"])==id and row["world"] == world:

                return "```スタミナ:{}／{}```".format(row["now_stamina"], row["max_stamina"])


# ?stamina スタミナ管理コマンド
def stamina(id, world, value):
    result = ""
    with open("data/register.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        # データの探索
        for idx, row in enumerate(data):
            # 操作対象 同じidか判定
            if int(row["id"]) == id and row["world"] == world:
                # スタミナ減少が0を下回る
                if int(row["now_stamina"]) + value < 0:
                    result = "```スタミナが足りません```"
                # スタミナ増加が最大値を超える
                elif int(row["now_stamina"]) + value > int(row["max_stamina"]):
                    result = "```スタミナ上限を超えます```"
                # スタミナを問題なく変動させる
                else:
                    row["now_stamina"] = str(int(row["now_stamina"]) + value)
                    data[idx]["now_stamina"] = str(int(row["now_stamina"]))
                    
                    # 結果の出力
                    result = "```スタミナ:{}/{}```".format(int(row["now_stamina"]),int(row["max_stamina"]))

                    # データの更新
                    with open("data/register.csv", "w") as f:
                        header = [
                                       "id", "world", "now_stamina", "max_stamina", "timecount"      
                        ]
                        writer = csv.DictWriter(f, header)
                        writer.writeheader()
                        writer.writerows(data)

    return result


def QUdeta(id, saku, sosa, max_stamina):
    with open("data/QUcharacter.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 同一のデータが登録されている
            if int(row["id"]) == id:
                return "```既に登録されています```"

    with open("data/QUcharacter.csv", "a") as f:
        header = [
            "id", "saku", "sosa", "max_stamina", "now_stamina", 
        ]
        writer = csv.DictWriter(f, header)
        data = {
            "id": id,
            "saku": saku,
            "sosa": sosa,
            "max_stamina": max_stamina,
            "now_stamina": max_stamina,
        }
        writer.writerow(data)

    return "```索敵:{} 捜索:{} スタミナ:{}  | クエスト用登録完了```".format(saku, sosa, max_stamina)

#クエスト探索（捜索）
def QUsosa(id,num_sosa):
     # ファイル読み込み(捜索用)
     with open("data/QUsosa.csv") as input_file:
        reader = csv.DictReader(input_file)
        for data in reader:
              if num_sosa == data["num"]:
               # ファイル読み込み(判定用)
                with open("data/QUcharacter.csv") as f:
                 reader = csv.DictReader(f)
                 char = [row for row in reader]#csvファイルを1行ずつ読み込む定型文
                # データの探索
                 for idx, row in enumerate(char):

                  row["now_stamina"] = str(int(row["now_stamina"]) - int(num_sosa))

                  # 操作対象 同じidか判定
                if int(row["id"])==id:
                  # スタミナ減少が0を下回る
                    if int(row["now_stamina"]) < 0:
                      result = "```スタミナが足りません```"
                      return result

                tmp = dice(100)

                if tmp < 95:

                      if tmp <= int(row["sosa"]):
                          name = data["name"]  # 種類
                          a = data["a"]
                          b = data["b"]
                          c = data["c"]
                          d = data["d"]

                          result = QUsosa_module(name, a, b, c, d)  # 捜索結果
                          result += "```現在のスタミナ:{}```".format(row["now_stamina"])

                                        # データの更新
                          with open("data/QUcharacter.csv", "w") as f:
                              header = [
                                              "id","saku","sosa","max_stamina","now_stamina"
                                          ]
                              writer = csv.DictWriter(f, header)
                              writer.writeheader()
                              writer.writerows(char)

                              return result
                      else:                                        # データの更新
                          with open("data/QUcharacter.csv", "w") as f:
                              header = [
                                              "id","saku","sosa","max_stamina","now_stamina"
                                          ]
                              writer = csv.DictWriter(f, header)
                              writer.writeheader()
                              writer.writerows(char)
                              result = "貴方は捜索に失敗してしまった…"
                              result += "```現在のスタミナ:{}```".format(row["now_stamina"])
                              return result
                else:
                                        # データの更新
                          with open("data/QUcharacter.csv", "w") as f:
                              header = [
                                              "id","saku","sosa","max_stamina","now_stamina"
                                          ]
                              writer = csv.DictWriter(f, header)
                              writer.writeheader()
                              writer.writerows(char)
                          result = "ファンブル！貴方の即座に敵に遭遇する。（敵の内容は索敵1の結果を参照すること）"
                          result += "```現在のスタミナ:{}```".format(row["now_stamina"])
                return result
        return "指定の数値が誤りです。"# 捜索の情報を与えて判定をおこなう
def QUsosa_module(name, a, b, c, d):
    a_info = a.split("：") if not a == "" else ["0","-"]
    b_info = b.split("：") if not b == "" else ["0","-"]
    c_info = c.split("：") if not c == "" else ["0","-"]
    d_info = d.split("：") if not d == "" else ["0","-"]

    # ダイス判定
    tmp = dice(100)
    if is_range(tmp, a_info[0]):
        result = a_info[1]
    elif is_range(tmp, b_info[0]):
        result = b_info[1]
    elif is_range(tmp, c_info[0]):
        result = c_info[1]
    elif is_range(tmp, d_info[0]):
        result = d_info[1]

    # 成果物出力
    return result
# ?sutaC スタミナチェックコマンド
def sutaC(id, world):
    result = ""
    with open("data/register.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        # データの探索
        for idx, row in enumerate(data):
            # 操作対象 同じidか判定
            if int(row["id"])==id and row["world"] == world:

                return "```スタミナ:{}／{}```".format(row["now_stamina"], row["max_stamina"])


# ?QUend クエストを終了する
def QUend(id):
    result = ""
    with open("data/QUcharacter.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        # データの探索
        for idx, row in enumerate(data):
            # 操作対象 同じidか判定
            if int(row["id"]) == id:
                # スタミナをリセット
                    row["now_stamina"] = str(int(row["max_stamina"]))
                    data[idx]["now_stamina"] = str(int(row["now_stamina"]))
                    
                    # 結果の出力
                    result = "```スタミナ:{}/{}```".format(int(row["now_stamina"]),int(row["max_stamina"]))

                    # データの更新
                    with open("data/QUcharacter.csv", "w") as f:
                        header = [
                                  "id","saku","sosa", "max_stamina","now_stamina"  
                        ]
                        writer = csv.DictWriter(f, header)
                        writer.writeheader()
                        writer.writerows(data)

    return result

