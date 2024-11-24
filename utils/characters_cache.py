webhook_characters = {}


def get_character_cache(owner_id: int, character_idx: str):
    print(webhook_characters)
    try:
        return webhook_characters[owner_id][character_idx]
    except KeyError:
        return False


def delete_character_cache(owner_id: int, character_idx: str):
    print(webhook_characters)
    try:
        del webhook_characters[owner_id][character_idx]
    except KeyError:
        return False


def set_character_cache(owner_id: int, character_idx: str, name: str, avatar: str):
    print(webhook_characters)
    if owner_id in webhook_characters:
        webhook_characters[owner_id][character_idx] = {"name": name, "avatar": avatar}
    else:
        webhook_characters[owner_id] = {character_idx: {"name": name, "avatar": avatar}}
