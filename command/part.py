import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname("module"), ".."))
sys.path.append(os.path.join(os.path.dirname("data"), ".."))

from module.dice_roll import dice


# ?part バイトコマンド
def part(kind, skill, count):
    # ファイル読み込み
    with open("data/part.csv") as f:
        reader = csv.DictReader(f)
        for data in reader:
            # 場所指定が一致している場合
            if kind == data["kind"]:
                name = data["name"]
                success_num = int(data["success_num"])
                challenge_num = int(data["challenge_num"])
                failure_gold = int(data["failure_gold"])
                success_gold = int(data["success_gold"])
                criterion = int(data["criterion"])
                continue_flag = True if data["continue_flag"] == "1" else False
                info = part_module(skill, count, name, success_num, challenge_num, failure_gold, success_gold, continue_flag, criterion)  # バイト結果
                return info

        # 場所が一致しない場合
        return "```対応するバイトがありません```"


# パート内部処理
def part_module(skill, count, name, success_num, challenge_num, failure_gold, success_gold, continue_flag, criterion):
    info = "```"
    sum = 0
    # count の回数分バイトの判定をおこなう
    for c in range(count):
        result_flag = 0  # 0:失敗 1:成功 2:ファンブル 3:100ファンブル
        success_count = 0  # 成功回数
        # challenge_num の回数分判定をおこなう
        for i in range(challenge_num):
            tmp = dice(100)
            # 成功
            if tmp <= skill and criterion < tmp:
                success_count += success_num if tmp >= skill - 5 else 1
                # 仕事成功
                if success_count >= success_num:
                    result_flag = 1
                    break
            # 失敗
            else:
                # 連続成功が条件か
                if continue_flag:
                    success_count = 0
                # ファンブル
                if tmp > 95:
                    result_flag = 2 if tmp < 100 else 3
                    break
        # 失敗
        if result_flag == 0:
            info += "{}回目: 失敗\n".format(c + 1)
            sum += failure_gold
        # 成功
        elif result_flag == 1:
            info += "{}回目: 成功\n".format(c + 1)
            sum += success_gold
        # ファンブル
        elif result_flag == 2:
            info += "{}回目: ファンブル\n".format(c + 1)
            sum += failure_gold*2
        # 100ファンブル
        elif result_flag == 3:
            info += "{}回目: 100ファンブル\n".format(c + 1)
            sum += failure_gold*2

    info += "```\n"
    info += "```{} | 報酬： {}```".format(name, sum)
    return info