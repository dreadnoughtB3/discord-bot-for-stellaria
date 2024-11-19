import os
import sys
from command.cheat import get_cheat

sys.path.append(os.path.join(os.path.dirname("module"), ".."))

from module.dice_roll import dice

def pastreroll(seq):
    return len(seq) != len(set(seq))

# ?auto キャラメイクコマンド
def auto():
    cheat = get_cheat("auto")
    if cheat:
        return create_cheat_data(cheat)

    # ライフパス

    lifepath = "```名前:\n"
    lifepath += "レベル:0\n"
    lifepath += "家柄:[{}, {}, {}, {}, {}]\n".format(dice(100), dice(100),
                                                   dice(100), dice(100),
                                                   dice(100))
    lifepath += "種族:\n"
    lifepath += "年代:\n"
    lifepath += "出自:\n"
    lifepath += "性別:\n"
    lifepath += "属性:{}属性 or {}属性\n".format(element_dice(), element_dice())
    lifepath += "人種:\n"
    lifepath += "[過去]\n"
    past0 = [past0_dice(), past0_dice(), past0_dice()]
    past1 = [past1_dice(), past1_dice(), past1_dice()]
    past2 = [past2_dice(), past2_dice(), past2_dice()]
    lifepath += "0章:{0[0]} or {0[1]} or {0[2]}\n".format(past0)
    lifepath += "1章:{0[0]} or {0[1]} or {0[2]}\n".format(past1)
    lifepath += "2章:{0[0]} or {0[1]} or {0[2]}```".format(past2)

    if pastreroll(past0):
        lifepath += "```振り直し結果：【{}】```".format(past0_dice())
    if pastreroll(past1):
        lifepath += "```振り直し結果：【{}】```".format(past1_dice())
    if pastreroll(past2):
        lifepath += "```振り直し結果：【{}】```".format(past2_dice())

    # メインステータス
    STR = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    INT = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    DEX = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    MND = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    SIZ = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    VIT = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    APP = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    ART = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    BUS = [dice(45) + 5, dice(45) + 5, dice(45) + 5, dice(45) + 5]
    mainstatus = "```筋力:[{0[0]: <2}, {0[1]: <2}, {0[2]: <2}, {0[3]: <2}]\n".format(STR)
    mainstatus += "知力:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(INT)
    mainstatus += "敏捷:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(DEX)
    mainstatus += "精神:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(MND)
    mainstatus += "体格:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(SIZ)
    mainstatus += "生命:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(VIT)
    mainstatus += "容姿:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(APP)
    mainstatus += "芸術:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(ART)
    mainstatus += "商才:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(BUS)
    mainstatus += "信仰:```"

    # 導出ステータス
    calstatus = "```HP:\n"
    calstatus += "MP:\n"
    calstatus += "幸運:\n"
    calstatus += "スタミナ:\n"
    calstatus += "気絶点:\n"
    calstatus += "依存点:\n"
    calstatus += "魅力:\n"
    calstatus += "知識:\n"
    calstatus += "SAN:\n"
    calstatus += "基礎技能P:\n"
    calstatus += "母国語(初期判定値70):\n"
    calstatus += "AB:\n"
    calstatus += "白兵:1d 魔法:1d```"

    # サブステータス
    substatus = "```サブステータス:\n"
    substatus += "膂力:\n"
    substatus += "叡智:\n"
    substatus += "体力:\n"
    substatus += "持久力:\n"
    substatus += "技量:\n"
    substatus += "神聖:\n"
    substatus += "商売:```"

    return lifepath, mainstatus, calstatus, substatus


def element_dice():
    tmp = dice(100)
    if tmp >= 1 and tmp < 10:
        return "地"
    elif tmp >= 10 and tmp < 20:
        return "花"
    elif tmp >= 20 and tmp < 30:
        return "雪"
    elif tmp >= 30 and tmp < 40:
        return "氷"
    elif tmp >= 40 and tmp < 50:
        return "水"
    elif tmp >= 50 and tmp < 60:
        return "風"
    elif tmp >= 60 and tmp < 70:
        return "炎"
    elif tmp >= 70 and tmp < 80:
        return "雷"
    elif tmp >= 80 and tmp < 90:
        return "光"
    elif tmp >= 90 and tmp < 100:
        return "夜"
    else:
        return "双"


def past0_dice():
    tmp = dice(8)
    if tmp == 1:
        return "凡庸"
    elif tmp == 2:
        return "生存"
    elif tmp == 3:
        return "悲哀"
    elif tmp == 4:
        return "愚行"
    elif tmp == 5:
        return "才能"
    elif tmp == 6:
        return "血統"
    elif tmp == 7:
        return "復讐"
    else:
        return "不要"


def past1_dice():
    tmp = dice(6)
    if tmp == 1:
        return "孤独"
    elif tmp == 2:
        return "平凡"
    elif tmp == 3:
        return "愛情"
    elif tmp == 4:
        return "禁断"
    elif tmp == 5:
        return "特別"
    else:
        return "苦痛"


def past2_dice():
    tmp = dice(6)
    if tmp == 1:
        return "暴力"
    elif tmp == 2:
        return "矜持"
    elif tmp == 3:
        return "風詠"
    elif tmp == 4:
        return "勤勉"
    elif tmp == 5:
        return "失意"
    else:
        return "憧憬"


def create_cheat_data(cheat_data: dict):
    lifepath = "```名前:\n"
    lifepath += "レベル:0\n"

    lifepath += f"家柄:[{cheat_data['pedigree'][0]}, {cheat_data['pedigree'][1]}, {cheat_data['pedigree'][2]}, {cheat_data['pedigree'][3]}, {cheat_data['pedigree'][4]}]\n"

    lifepath += "種族:\n"
    lifepath += "年代:\n"
    lifepath += "出自:\n"
    lifepath += "性別:\n"

    lifepath += "属性:{}属性 or {}属性\n".format(cheat_data["element"][0], cheat_data["element"][1])

    lifepath += "人種:\n"
    lifepath += "[過去]\n"
    past0 = cheat_data["past0"]
    past1 = cheat_data["past1"]
    past2 = cheat_data["past2"]
    lifepath += "0章:{0[0]} or {0[1]} or {0[2]}\n".format(past0)
    lifepath += "1章:{0[0]} or {0[1]} or {0[2]}\n".format(past1)
    lifepath += "2章:{0[0]} or {0[1]} or {0[2]}```".format(past2)

    # メインステータス
    STR = cheat_data["STR"]
    INT = cheat_data["INT"]
    DEX = cheat_data["DEX"]
    MND = cheat_data["MND"]
    SIZ = cheat_data["SIZ"]
    VIT = cheat_data["VIT"]
    APP = cheat_data["APP"]
    ART = cheat_data["ART"]
    BUS = cheat_data["BUS"]

    mainstatus = "```筋力:[{0[0]: <2}, {0[1]: <2}, {0[2]: <2}, {0[3]: <2}]\n".format(STR)
    mainstatus += "知力:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(INT)
    mainstatus += "敏捷:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(DEX)
    mainstatus += "精神:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(MND)
    mainstatus += "体格:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(SIZ)
    mainstatus += "生命:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(VIT)
    mainstatus += "容姿:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(APP)
    mainstatus += "芸術:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(ART)
    mainstatus += "商才:[{0[0]: >2}, {0[1]: >2}, {0[2]: >2}, {0[3]: >2}]\n".format(BUS)
    mainstatus += "信仰:```"

    # 導出ステータス
    calstatus = "```HP:\n"
    calstatus += "MP:\n"
    calstatus += "幸運:\n"
    calstatus += "スタミナ:\n"
    calstatus += "気絶点:\n"
    calstatus += "依存点:\n"
    calstatus += "魅力:\n"
    calstatus += "知識:\n"
    calstatus += "SAN:\n"
    calstatus += "基礎技能P:\n"
    calstatus += "母国語(初期判定値70):\n"
    calstatus += "AB:\n"
    calstatus += "白兵:1d 魔法:1d```"

    # サブステータス
    substatus = "```サブステータス:\n"
    substatus += "膂力:\n"
    substatus += "叡智:\n"
    substatus += "体力:\n"
    substatus += "持久力:\n"
    substatus += "技量:\n"
    substatus += "神聖:\n"
    substatus += "商売:```"
    
    return lifepath, mainstatus, calstatus, substatus