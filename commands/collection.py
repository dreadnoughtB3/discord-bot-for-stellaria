import csv

from modules.dice_roll import dice
from modules.judge import is_range


# ?gather 採取コマンド
def gather(kind, count, skill):
    if not skill.isdecimal() or not count.isdecimal():
        return "引数が不正です"

    skill = int(skill)
    count = int(count)

    # ファイル読み込み
    with open("data/gather.csv", encoding="shift_jis") as f:
        reader = csv.DictReader(f)
        for data in reader:
            # 場所指定が一致している場合
            if kind == data["kind"]:
                area = "採取場所：" + data["area"]  # 場所名称
                info = data["info"]  # 採取物情報
                result = collection_module(info, kind, count, skill)  # 採取結果
                return area + "\n" + result
        # 場所が一致しない場合
        return "```対応する採取場所がありません```"


# ?fell 伐採コマンド
def fell(kind, count, skill):
    if not skill.isdecimal() or not count.isdecimal():
        return "引数が不正です"

    skill = int(skill)
    count = int(count)

    # ファイル読み込み
    with open("data/fell.csv", encoding="shift_jis") as f:
        reader = csv.DictReader(f)
        for data in reader:
            # 場所指定が一致している場合
            if kind == data["kind"]:
                area = "伐採場所：" + data["area"]  # 場所名称
                info = data["info"]  # 伐採物情報
                result = collection_module(info, kind, count, skill)  # 採取結果
                return area + "\n" + result
        # 場所が一致しない場合
        return "```対応する伐採場所がありません```"


# ?mine 採掘コマンド
def mine(kind, count, skill):
    if not skill.isdecimal() or not count.isdecimal():
        return "引数が不正です"

    skill = int(skill)
    count = int(count)

    # ファイル読み込み
    with open("data/mine.csv", encoding="shift_jis") as f:
        reader = csv.DictReader(f)
        for data in reader:
            # 場所指定が一致している場合
            if kind == data["kind"]:
                area = "採掘場所：" + data["area"]  # 場所名称
                info = data["info"]  # 採掘物情報
                result = collection_module(info, kind, count, skill)  # 採取結果
                return area + "\n" + result
        # 場所が一致しない場合
        return "```対応する採掘場所がありません```"


# 採取物の情報を与えて判定をおこなう
def collection_module(info, kind, count, skill):
    args = info.split("/")
    item = [0] * len(args)
    # count回の繰り返し
    for i in range(count):
        # 採取判定
        if dice(100) <= skill:
            # 採取物判定
            tmp = dice(100)
            for j, arg in enumerate(args):
                if is_range(tmp, arg.split("：")[0]):
                    item[j] += 1
    # 成果物出力
    result = "```"
    for j, arg in enumerate(args):
        result += "{}×{} ".format(arg.split("：")[1], item[j])
    result += "| 成功回数:{}```".format(sum(item))
    return result
