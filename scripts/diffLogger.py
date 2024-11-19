from module.get_datetime import get_japan_current_time

def logging_edit(before, after) -> str:
  msg = "> ### [LOGGER] メッセージ変更検知\n"
  msg += f"> 変更時刻： {get_japan_current_time()}\n"
  msg += f"> チャンネル： {before.channel.name}\n"
  msg += f"> メッセージ： {after.jump_url}\n"
  msg += "> ―――――[変更前]―――――\n"
  msg += f"{before.content}\n"
  msg += "> ―――――[変更後]―――――\n"
  msg += f"{after.content}\n"

  return msg

def logging_delete(message) -> str:
  msg = "> ### [LOGGER] メッセージ削除検知\n"
  msg += f"> 削除時刻： {get_japan_current_time()}\n"
  msg += f"> チャンネル： {message.channel.name}\n"
  msg += "> ―――――[削除内容]―――――\n"
  msg += f"{message.content}\n"

  return msg