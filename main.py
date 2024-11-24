"""main file"""

import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from scripts.diffLogger import logging_delete, logging_edit
from modules.get_datetime import get_japan_current_time
from scripts.stock_make import stock_make
from scripts.trade_make import trade_make
from scripts.check_file_exist import check_stock_data

from server import server_thread

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)
load_dotenv(verbose=True)
TOKEN = os.environ.get("TOKEN")


# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = get_japan_current_time().strftime("%H:%M")
    if now == "00:00" or now == "12:00":
        # 交易投稿
        trade_make()
        channel = bot.get_channel(992623803291144244)  # Stella
        await channel.send(file=discord.File("outputs/trade.jpg"))
    if now == "00:00":
        embed_f, embed_n = stock_make()
        # ファンタジア株
        channel = bot.get_channel(992086009061843056)  # Stella
        await channel.send(file=discord.File("outputs/stock_f.jpg"))
        await channel.send(embed=embed_f)
        # ノクターン株
        channel = bot.get_channel(946667883168153610)  # Stella
        await channel.send(file=discord.File("outputs/stock_n.jpg"))
        await channel.send(embed=embed_n)


@bot.event
async def on_ready():
    """Bot起動時に実行される処理"""
    print(f"{bot.user}: 起動完了")
    await bot.tree.sync()
    check_stock_data()  # 株価用CSVデータが存在しない場合は初期化する
    loop.start()


@bot.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_message_edit(before, after):
    if before.author.id == 344181098818830338:
        channel = bot.get_channel(1308387319002169404)
        send_message = logging_edit(before, after)
        await channel.send(send_message)


@bot.event
async def on_message_delete(message):
    if message.author.id == 344181098818830338:
        channel = bot.get_channel(1308387319002169404)
        send_message = logging_delete(message)
        await channel.send(send_message)


if __name__ == "__main__":
    server_thread()
    bot.run(TOKEN)  # Botを起動
