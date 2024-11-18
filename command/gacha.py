import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname("module"), ".."))
sys.path.append(os.path.join(os.path.dirname("data"), ".."))

from module.dice_roll import dice
from module.judge import is_range


# ?gacha ガチャコマンド
def gacha(kind, count):
    # ファイル読み込み
    with open("data/gacha.csv") as f:
        reader = csv.DictReader(f)
        for data in reader:
            # 種類指定が一致している場合
            if kind == data["kind"]:
                name = data["name"]  # 種類
                dice_num = int(data["dice_num"])  #ダイス目
                N = data["N"]
                R = data["R"]
                SR = data["SR"]
                SSR = data["SSR"]
                UR = data["UR"]
                result = gacha_module(count, name, dice_num, N, R, SR, SSR, UR)  # ガチャ結果
                return result
        # 種類が一致しない場合
        return "```対応するガチャがありません```"


# ガチャの情報を与えて判定をおこなう
def gacha_module(count, name, dice_num, N, R, SR, SSR, UR):
    N_info = N.split("：") if not N == "" else ["0","-"]
    R_info = R.split("：") if not R == "" else ["0","-"]
    SR_info = SR.split("：") if not SR == "" else ["0","-"]
    SSR_info = SSR.split("：") if not SSR == "" else ["0","-"]
    UR_info = UR.split("：") if not UR == "" else ["0","-"]
    dice_list = []
    item = {"N":0, "R":0, "SR":0, "SSR":0, "UR":0}
    # count回の繰り返し
    for i in range(count):
        # ダイス判定
        tmp = dice(dice_num)
        if is_range(tmp, N_info[0]):
            item["N"] += 1
        elif is_range(tmp, R_info[0]):
            item["R"] += 1
        elif is_range(tmp, SR_info[0]):
            item["SR"] += 1
        elif is_range(tmp, SSR_info[0]):
            item["SSR"] += 1
        elif is_range(tmp, UR_info[0]):
            item["UR"] += 1
        dice_list.append(tmp)

    # 成果物出力
    result = "```{} | ガチャ回数：{}```".format(name, count)
    result += "```{}```".format(dice_list)
    result += "```  N : {} × {}\n".format(N_info[1], item["N"])
    result += "  R : {} × {}\n".format(R_info[1], item["R"])
    result += " SR : {} × {}\n".format(SR_info[1], item["SR"])
    result += "SSR : {} × {}\n".format(SSR_info[1], item["SSR"])
    result += " UR : {} × {}```".format(UR_info[1], item["UR"])
    return result