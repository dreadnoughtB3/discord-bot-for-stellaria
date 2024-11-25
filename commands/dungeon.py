import json
from random import choice
from modules.dice_roll import dice
from commands.enemies import create_enemy

current_party = {}
dungeon_data = {}


def init_dungeon_data():
    global dungeon_data
    data = open("data/contents/dungeon.json", "r", encoding="utf-8")
    json_data = json.load(data)
    dungeon_data = json_data


def get_party_data(channel_id: int):
    return current_party.get(channel_id, None)


def create_party_data(channel_id: int, dungeon_id: str, member_num: int) -> bool:
    if channel_id in current_party:
        return False
    if dungeon_id not in dungeon_data:
        return False
    elif 0 >= member_num >= 5:
        return False
    else:
        current_party[channel_id] = {
            "dungeon_id": dungeon_id,
            "party": {"member_num": member_num},
            "progress": 0,
            "inventory": {},
        }
        return dungeon_data[dungeon_id]["name"]


def delete_party_data(channel_id: int) -> bool:
    try:
        del current_party[channel_id]
        return True
    except KeyError:
        return False


def next_process(channel_id: int):
    party_data = get_party_data(channel_id)
    if not party_data:
        return False
    dungeon_id = party_data["dungeon_id"]
    dungeon_name = dungeon_data[dungeon_id]["name"]

    # もし最大進捗度まで到達したら
    if dungeon_data[dungeon_id]["max_progress"] == party_data["progress"]:
        return "> クリア！"
    current_party[channel_id]["progress"] = party_data["progress"] + 1

    event_res = dice(100)
    # 回復ポイント
    if event_res >= 95:
        name = "安らぎの広間"
        description = "罠や敵の気配が無い、静謐で美しい広間に出た。ここで暫く休んでいけば、大きく回復できそうな予感がする。"
        effect = (
            "HP、MP、スタミナのいずれか一つを選択し、最大値の半分を回復することが可能"
        )
    # グッドイベント
    elif 95 > event_res >= 75:
        good_event_num = dungeon_data[dungeon_id]["good_event_num"]
        res = dice(good_event_num)
        event_data = dungeon_data[dungeon_id]["good_events"][f"e{res}"]
        name = event_data["name"]
        description = event_data["text"]
        effect = event_data["effect"]
    # バッドイベント
    elif 75 > event_res >= 55:
        bad_event_num = dungeon_data[dungeon_id]["bad_event_num"]
        res = dice(bad_event_num)
        event_data = dungeon_data[dungeon_id]["bad_events"][f"e{res}"]
        name = event_data["name"]
        description = event_data["text"]
        effect = event_data["effect"]
    # 接敵
    elif 55 > event_res >= 20:
        current_progress = str(party_data["progress"])
        if len(current_progress) == 1:
            list_key = "0"
        else:
            list_key = current_progress[0]
        enemy_key_list = dungeon_data[dungeon_id]["enemies"][list_key]
        enemy_key = choice(enemy_key_list)
        enemy_level = int(list_key) + 1
        enemy_data = create_enemy(enemy_key, enemy_level)
        enemy_num = dice(party_data["party"]["member_num"])
        name = "接敵！"
        description = "モンスターと接敵した。これを倒さねば先へ進めないだろう。"
        effect = f"以下の敵ｘ{enemy_num}と戦闘\n{enemy_data}"
    # なにもない
    else:
        name = "何もなし"
        description = "何も起きなかった"
        effect = "なし"

    send_message = (
        f"> ⋙進行中のダンジョン：**『{dungeon_name}』**\n"
        "> ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣\n"
        f"> **イベント：{name}**\n"
        f"> **内容：** \n{description}\n"
        f"> **効果：** \n{effect}"
    )
    return send_message
