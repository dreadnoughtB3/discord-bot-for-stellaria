import json
import os

enemies_data = {}
skills_data = {}


def init_enemy_data():
    global enemies_data, skills_data

    for filename in os.listdir("data/contents/enemies/"):
        if filename.endswith(".json"):
            filepath = os.path.join("data/contents/enemies/", filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                enemies_data.update(data["enemies"])
                skills_data.update(data["skills"])

            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error loading {filename}: {e}")


def create_enemy(enemy_key: str, enemy_level: int, enemy_num: int = None):
    enemy_data = enemies_data[enemy_key]
    if enemy_num:
        data_string = f'```ENEMY：{enemy_data["name"]}ｘ{enemy_num}\n'
    else:
        data_string = f'```ENEMY：{enemy_data["name"]}\n'

    data_string += (
        '――――――――――――――――――――――\n'
        f'HP：{enemy_data["hp"]}/{enemy_data["hp"]}\n'
        f'物理防護点：{enemy_data["phys_def"]}\n'
        f'魔法防護点：{enemy_data["magic_def"]}\n'
        f'物理ダメージカット率：{enemy_data["phys_cut"]}\n'
        f'魔法ダメージカット率：{enemy_data["magic_cut"]}\n'
        f'攻撃命中値：{enemy_data["atk_acur"]}\n'
        f'回避命中値：{enemy_data["ave_acur"]}\n'
        '――――――――――――――――――――――\n\n'
        f'攻撃手段：1d{enemy_data["skill_num"]}\n'
    )

    for index, skill in enumerate(enemy_data["skills"], 1):
        skill_data = skills_data[skill]
        data_string += f"{index} - {skill_data['name']}\n"
        data_string += f"{skill_data['desc']}\n\n"
    data_string += "――――――――――――――――――――――```"
    return data_string
