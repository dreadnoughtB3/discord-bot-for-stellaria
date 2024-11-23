import re
import random
import math
from sympy import sympify, Integer, Float

PATTERN = r"([+\-*/()<>]=?|<=|<-|>=|!=)"
EXCLUDE_LIST = ["", "(", ")", "+", "-", "*", "/", "<=", ">=", "<-", ">-"]


def simple_dice(dice_notation: str) -> tuple[int, str]:
    """
    ダイスを振り、合計値と各ダイスの出目を返す。

    Args:
        dice_notation (str): ダイス記法（例: "3d6", "1d10"）

    Returns:
        tuple[int, str]: 合計値と出目を表す文字列
    """
    try:
        # 記法を分割（例: "3d6" -> num_dice=3, dice_sides=6）
        num_dice, dice_sides = map(int, dice_notation.lower().split("d"))
        if num_dice <= 0 or dice_sides <= 0:
            raise ValueError("ダイスの数や面数は1以上である必要があります。")

        # ダイスを振る
        rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]

        # 合計値と出目を返す
        return sum(rolls), ", ".join(map(str, rolls))
    except (ValueError, IndexError):
        raise ValueError("無効なダイス記法です。例: '3d6' や '1d10'")


def bool_to_int(val: bool) -> int:
    if val:
        return 1
    else:
        return 0


def dice_roll(expression: str):
    dice_results = {}
    str_result = ""
    parts = [token for token in re.split(PATTERN, expression) if token.strip()]

    try:
        for index, part in enumerate(parts):
            if part not in EXCLUDE_LIST and "d" in part:
                total, result = simple_dice(part)
                dice_results[index] = [total, result]

        calc_formula = ""

        for index, part in enumerate(parts):
            if "d" in part:
                calc_formula += str(dice_results[index][0])
                str_result += f"{part} ({dice_results[index][1]})"
            else:
                if part == "(":
                    str_result += " ("
                elif part == ")":
                    str_result += ")"
                elif part in EXCLUDE_LIST:
                    str_result += f" {part} "
                else:
                    str_result += part
                calc_formula += part
        calc_result = sympify(calc_formula)
        if not isinstance(calc_result, (Integer, Float)):
            calc_result = bool_to_int(calc_result)
        else:
            calc_result = math.floor(calc_result)
        return (str_result, calc_result)
    except Exception as e:
        return (None, e)
