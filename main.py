# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import discord
import ast
from dotenv import load_dotenv
import os
from discord.ext import tasks
from datetime import datetime
from command.cheat import add_cheat
from command.b import b
from command.r import r
from command.part import part
from command.auto import auto
from command.collection import gather, fell, mine
from command.gacha import gacha
from command.repair import repair
from command.weapons import weapons, amm, check, dur
from command.register import register , staminaloop , sutaC , stamina , QUdeta , QUsosa,QUend
from timer.stock_make import stock_make
from timer.trade_make import trade_make
from server import server_thread


client = discord.Client(intents=discord.Intents.all())
load_dotenv(verbose=True)
TOKEN = os.environ.get("TOKEN")


def isint(s):  # 整数値かどうかを判定する関数
    try:
        int(s, 10)  # 試しにint関数で文字列を変換
    except ValueError:
        return False  # 失敗すれば False
    else:
        return True  # 上手くいけば True


# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    staminaloop()
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '00:00' or now == '12:00':
    # 交易投稿
        trade_make()
        channel = client.get_channel(992623803291144244) # Stella
        await channel.send(file=discord.File("output/trade.jpg"))
    if now == '00:00':
        embed_f, embed_n = stock_make()
        # ファンタジア株
        channel = client.get_channel(992086009061843056) # Stella
        await channel.send(file=discord.File("output/stock_f.jpg"))
        await channel.send(embed=embed_f)
        # ノクターン株
        channel = client.get_channel(946667883168153610) # Stella
        await channel.send(file=discord.File("output/stock_n.jpg"))
        await channel.send(embed=embed_n)


#ループ処理実行
@client.event
async def on_ready():
    loop.start()


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # チートコマンド
    if message.content.startswith("!cheat"):
        args = message.content.split(" ")
        if len(args) == 1:
            await message.channel.send("> [CHEAT] [ERROR] : チートを使用するコマンドを指定してください")
            return
        ## auto
        if args[1] == "auto":
            if len(args) != 16:
                await message.channel.send("> [CHEAT] [ERROR] : 引数が不足しています ")
                return
            try:
                params = {
                    "pedigree": ast.literal_eval(args[2]),
                    "element": args[3].strip("[]").split(","),
                    "past0": args[4].strip("[]").split(","),
                    "past1": args[5].strip("[]").split(","),
                    "past2": args[6].strip("[]").split(","),
                    "STR": ast.literal_eval(args[7]),
                    "INT": ast.literal_eval(args[8]),
                    "DEX": ast.literal_eval(args[9]),
                    "MND": ast.literal_eval(args[10]),
                    "SIZ": ast.literal_eval(args[11]),
                    "VIT": ast.literal_eval(args[12]),
                    "APP": ast.literal_eval(args[13]),
                    "ART": ast.literal_eval(args[14]),
                    "BUS": ast.literal_eval(args[15])
                }
            except Exception as e:
                print(e)
                await message.channel.send("> [CHEAT] [ERROR] : 引数が不正です")
                return
            add_cheat("auto", params)
            send_message = "> **[CHEAT]: autoコマンド**\n> 以下のパラメータで設定しました:\n```"
            for k,v in params.items():
                send_message += f"{k}: {v}\n"
            send_message += "```"
            await message.channel.send(send_message)


    # ダイスロール
    if message.content.startswith("!r"):
        arg = message.content.split(" ")
        if len(arg) == 1:
            send_message = "使用者:<@{}>\n".format(message.author.id) + r()
            await message.channel.send(send_message)
        elif len(arg) == 2:
            send_message = "使用者:<@{}>\n".format(message.author.id) + r(arg[1])
            await message.channel.send(send_message)
        elif len(arg) == 3:
            send_message = "使用者:<@{}>\n".format(message.author.id) + r(arg[1], arg[2])
            await message.channel.send(send_message)


    # 個別ダイスロール
    if message.content.startswith("!b"):
        arg = message.content.split(" ")
        if len(arg) == 2:
            send_message = "使用者:<@{}>\n".format(message.author.id) + b(arg[1])
            await message.channel.send(send_message)
        elif len(arg) == 3:
            send_message = "使用者:<@{}>\n".format(message.author.id) + b(arg[1], arg[2])
            await message.channel.send(send_message)


    # バイト
    if message.content.startswith("!part"):
        arg = message.content.split(" ")
        if len(arg) == 4:
            if arg[1].startswith("f") or arg[1].startswith("n"):
                kind = arg[1]
                if arg[2].isdecimal():
                    skill = int(arg[2])
                    if arg[3].isdecimal():
                        count = int(arg[3])
                        send_message = "使用者:<@{}>\n".format(message.author.id) + part(kind, skill, count)
                        await message.channel.send(send_message)


    # キャラメイク
    if message.content == "!auto":
        lifepath, mainstatus, calstatus, substatus = auto()
        send_message = "使用者:<@{}>\n".format(message.author.id) + lifepath + "\n" + mainstatus + "\n" + calstatus + "\n" + substatus
        await message.channel.send(send_message)


    # 採取
    if message.content.startswith("!gather"):
        arg = message.content.split(" ")
        if len(arg) == 4:
            if arg[1].startswith("f") or arg[1].startswith("n") or arg[1].startswith("event"):
                kind = arg[1]
                if arg[2].isdecimal():
                    count = int(arg[2])
                    if arg[3].isdecimal():
                        skill = int(arg[3])
                        send_message = "使用者:<@{}>\n".format(message.author.id) + gather(kind, count, skill)
                        await message.channel.send(send_message)


    # 伐採
    if message.content.startswith("!fell"):
        arg = message.content.split(" ")
        if len(arg) == 4:
            if arg[1].startswith("f") or arg[1].startswith("n"):
                kind = arg[1]
                if arg[2].isdecimal():
                    count = int(arg[2])
                    if arg[3].isdecimal():
                        skill = int(arg[3])
                        send_message = "使用者:<@{}>\n".format(message.author.id) + fell(kind, count, skill)
                        await message.channel.send(send_message)


    # 採掘
    if message.content.startswith("!mine"):
        arg = message.content.split(" ")
        if len(arg) == 4:
            if arg[1].startswith("f") or arg[1].startswith("n"):
                kind = arg[1]
                if arg[2].isdecimal():
                    count = int(arg[2])
                    if arg[3].isdecimal():
                        skill = int(arg[3])
                        send_message = "使用者:<@{}>\n".format(message.author.id) + mine(kind, count, skill)
                        await message.channel.send(send_message)


    # ガチャ
    if message.content.startswith("!gacha"):
        arg = message.content.split(" ")
        if len(arg) == 3:
            if arg[1].startswith("f") or arg[1].startswith("n"):
                kind = arg[1]
                if arg[2].isdecimal():
                    count = int(arg[2])
                    send_message = "使用者:<@{}>\n".format(message.author.id) + gacha(kind, count)
                    await message.channel.send(send_message)


    # 修理
    if message.content.startswith("!repair"):
        arg = message.content.split(" ")
        if len(arg) == 5:
            if arg[1].isdecimal():
                count = int(arg[1])
                if arg[2].isdecimal():
                    skill = int(arg[2])
                    if arg[3].isdecimal():
                        now_durability = int(arg[3])
                        if arg[4].isdecimal():
                            max_durability = int(arg[4])
                            send_message = "使用者:<@{}>\n".format(message.author.id) + repair(count, skill, now_durability, max_durability)
                            await message.channel.send(send_message)


    # 装備登録 ?weapons 武器名 最大装填弾数 現在の装填弾数　最大耐久　現在の耐久
    if message.content.startswith("!weapons"):
        arg = message.content.split(" ")
        if len(arg) == 6:
            weapons_name = arg[1]
            if arg[2].isdecimal():
                max_ammunition = arg[2]
                if arg[3].isdecimal():
                    now_ammunition = arg[3]
                    if arg[4].isdecimal():
                        max_durability = arg[4]
                        if arg[5].isdecimal():
                            now_durability = arg[5]
                            send_message = "使用者:<@{}>\n".format(message.author.id) + weapons(message.author.id, weapons_name, max_ammunition, now_ammunition, max_durability, now_durability)
                            await message.channel.send(send_message)


    # 装備変更
    if message.content.startswith("!change"):
        arg = message.content.split(" ")
        if len(arg) == 3:
            send_message = "使用者:<@{}>\n".format(message.author.id) + change(message.author.id, value)
            await message.channel.send(send_message)


    # 弾薬管理
    if message.content.startswith("!amm"):
        arg = message.content.split(" ")
        if len(arg) == 2:
             if isint(arg[1]):
                value = int(arg[1])
                send_message = "使用者:<@{}>\n".format(message.author.id) + amm(message.author.id, value)
                await message.channel.send(send_message)

  # 弾薬管理
    if message.content.startswith("!dur"):
        arg = message.content.split(" ")
        if len(arg) == 2:
             if isint(arg[1]):
                value = int(arg[1])
                send_message = "使用者:<@{}>\n".format(message.author.id) + dur(message.author.id, value)
                await message.channel.send(send_message)


    # 武器の状態確認
    if message.content.startswith("!check"):
        arg = message.content.split(" ")
        if len(arg) == 1:
            send_message = "使用者:<@{}>\n".format(message.author.id) + check(message.author.id)
            await message.channel.send(send_message)


    # 登録
    if message.content.startswith("!register"):
        arg = message.content.split(" ")
        if len(arg) == 4:
            if arg[1] == "f" or arg[1] == "n":
                world = arg[1]
                if arg[2].isdecimal():
                    max_stamina = arg[2]
                    now_stamina = arg[3]
                    send_message = "使用者:<@{}>\n".format(message.author.id) + register(message.author.id, world, max_stamina, now_stamina)
                    await message.channel.send(send_message)


    # スタミナ管理
    if message.content.startswith("!stamina"):
        arg = message.content.split(" ")
        if len(arg) == 3:
            if arg[1] == "f" or arg[1] == "n":
                world = arg[1]
                if isint(arg[2]):
                    value = int(arg[2])
                    send_message = "使用者:<@{}>\n".format(message.author.id) + stamina(message.author.id, world, value)
                    await message.channel.send(send_message)


    # スタミナの状態確認
    if message.content.startswith("!sutaC"):
        arg = message.content.split(" ")
        if len(arg) == 2:
            if arg[1] == "f" or arg[1] == "n":
                world = arg[1]
                send_message = "使用者:<@{}>\n".format(message.author.id) + sutaC(message.author.id, world)
                await message.channel.send(send_message)


    # クエスト用データ登録
    if message.content.startswith("!QUdeta"):
        arg = message.content.split(" ")
        if len(arg) == 4:
            saku = arg[1]
            sosa = arg[2]
            max_stamina = arg[3]
            send_message = "使用者:<@{}>\n".format(message.author.id) + QUdeta(message.author.id, saku, sosa, max_stamina)
            await message.channel.send(send_message)


    # クエスト開始
    if message.content.startswith("!QUsosa"):
        arg = message.content.split(" ")
        if len(arg) == 2:
            num_sosa = arg[1]
            send_message = "使用者:<@{}>\n".format(message.author.id) + QUsosa(message.author.id, num_sosa)
            await message.channel.send(send_message)


    # クエスト用のキャラクタ―情報をリセット
    if message.content.startswith("!QUend"):
        arg = message.content.split(" ")
        if len(arg) == 1:
            send_message = "使用者:<@{}>\n".format(message.author.id) + QUend(message.author.id)
            await message.channel.send(send_message)

    if message.content.startswith("!tea"):
        arg = message.content.split(" ")
        if len(arg) == 1:
            send_message = "https://tenor.com/view/tea-tea-time-black-tea-crockery-finechina-gif-19858737"
            await message.channel.send(send_message)

    if message.content.startswith("!cake"):
        arg = message.content.split(" ")
        if len(arg) == 1:
            send_message = "https://tenor.com/view/lemon-meringue-pie-pies-dessert-pie-gif-2665188071120448341"
            await message.channel.send(send_message)

client.run(TOKEN)
