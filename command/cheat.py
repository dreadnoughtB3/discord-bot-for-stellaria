current_cheats = {
  "auto": ""
}


def add_cheat(key: str, value: dict):
  current_cheats[key] = value


def get_cheat(key):
  cheat_data = current_cheats.get(key, None)
  if cheat_data != None:
    del current_cheats[key]
    return cheat_data
  else:
    return False