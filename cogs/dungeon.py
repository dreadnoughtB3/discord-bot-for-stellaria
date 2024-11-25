from discord.ext import commands
from utils.check_guild import check_allowed_guild
from commands import dungeon
from commands.enemies import create_enemy
from modules.dice_roll import dice


class Dungeon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_allowed_guild()
    @commands.command(name="dungeon")
    async def dungeon_handler(
        self, ctx, action: str = "next", arg1: str = None, arg2: str = None
    ):
        channel_id = ctx.channel.id
        match action:
            # ダンジョン開始
            case "start":
                if not arg1:
                    await ctx.send("> ダンジョンIDが不正です")
                    return
                if not arg2 or not arg2.isdecimal():
                    await ctx.send("> パーティーメンバー数が不正です")
                    return
                res = dungeon.create_party_data(channel_id, arg1, int(arg2))
                if res:
                    send_message = '### **=====** 𝓦𝓮𝓵𝓬𝓸𝓶𝓮 𝓽𝓸 𝓓𝓾𝓷𝓰𝓮𝓸𝓷 **=====**\n'\
                        f'> **ダンジョン名: 『{res}』**\n'\
                        f'> **チャンネル名: {ctx.channel.name}**'
                    await ctx.send(send_message)
                else:
                    await ctx.send("> ダンジョンの開始に失敗しました")
            # ダンジョン終了
            case "end":
                res = dungeon.delete_party_data(channel_id)
                if res:
                    await ctx.send("> ダンジョンを終了しました")
                else:
                    await ctx.send("> ダンジョンの終了に失敗しました")
            # 先に進む
            case "next":
                res = dungeon.next_process(channel_id)
                if res:
                    await ctx.send(res)
                else:
                    await ctx.send("> 進行処理に失敗しました")
            # 手動結果
            case "event":
                if arg1 != "shld":
                    await ctx.send("> イベントデータが存在しません")
                    return
                res = create_enemy("eny6", 0, dice(4))
                await ctx.send(res)
            case _:
                await ctx.send("> 操作が不正です")


async def setup(bot):
    await bot.add_cog(Dungeon(bot))
