from modules.dice_roll import dice


# ?repair 修理コマンド
def repair(count, skill, now, max):
    for val in [count, skill, now, max]:
        if not val.isdecimal():
            return "引数が不正です"

    count, skill, now, max = map(int, [count, skill, now, max])

    sum = 0
    item = [0, 0, 0, 0]
    # 修理判定
    for i in range(count):
        tmp = dice(100)
        # 成功
        if tmp <= skill:
            # クリティカル
            if tmp >= skill - 5:
                item[2] += 1
            # 通常成功
            else:
                item[0] += 1
        # 失敗
        else:
            # ファンブル
            if tmp > 95:
                item[3] += 1
            # 通常失敗
            else:
                item[1] += 1

    sum = item[0] + item[2] * 2 - item[3] * 2
    after = now + sum if now + sum < max else max
    result = "修理回数:{0}\n```成功×{1[0]} 失敗×{1[1]} クリティカル×{1[2]} ファンブル×{1[3]} | 耐久変動:{2} | 現在の装備耐久:{3}/{4}```".format(
        count, item, sum, after, max)
    return result
