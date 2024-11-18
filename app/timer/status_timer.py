import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname("data"), ".."))

from datetime import timezone, timedelta, datetime


# スタミナ自動回復
def stamina_timer():
    now = datetime.now(timezone(timedelta(hours=+9), "JST")).strftime("%H:%M")
    with open("data/register.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        for idx, row in enumerate(data):
            # スタミナ回復時刻である
            if row["stamina_time"] == now:
                # スタミナ回復
                if int(row["now_stamina"]) < int(row["max_stamina"]):
                    data[idx]["now_stamina"] = str(
                        int(data[idx]["now_stamina"]) + 1)
                # スタミナ回復時刻の更新
                if int(data[idx]["now_stamina"]) < int(row["max_stamina"]):
                    data[idx]["stamina_time"] = datetime.now(
                        timezone(timedelta(hours=+9, minutes=+30),
                                 "JST")).strftime("%H:%M")
                else:
                    data[idx]["stamina_time"] = None

    # データ更新
    with open("data/register.csv", "w") as f:
        header = [
            "id", "world", "now_stamina", "max_stamina", "now_gold",
            "max_gold", "now_qp", "max_qp", "now_food", "stamina_time",
            "food_time"
        ]
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(data)


# 満腹度自動減少
def food_timer():
    now = datetime.now(timezone(timedelta(hours=+9), "JST")).strftime("%H:%M")
    with open("data/register.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        for idx, row in enumerate(data):
            # 満腹度減少時刻である
            if row["food_time"] == now:
                # 満腹度減少
                if int(row["now_food"]) < int(row["max_food"]):
                    data[idx]["now_stamina"] = str(
                        int(data[idx]["now_food"]) + 1)
                # 満腹度減少時刻の更新
                if int(data[idx]["now_food"]) > 0:
                    data[idx]["food_time"] = datetime.now(
                        timezone(timedelta(hours=+17),
                                 "JST")).strftime("%H:%M")
                else:
                    data[idx]["food_time"] = None

    # データ更新
    with open("data/register.csv", "w") as f:
        header = [
            "id", "world", "now_stamina", "max_stamina", "now_gold",
            "max_gold", "now_qp", "max_qp", "now_food", "stamina_time",
            "food_time"
        ]
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(data)