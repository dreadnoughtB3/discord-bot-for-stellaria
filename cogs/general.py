from discord.ext import commands
from utils.check_guild import check_allowed_guild
from modules.roll import dice_roll
from commands.part import part
from commands.auto import auto
from commands.collection import fell, mine, gather
from commands.gacha import gacha
from commands.repair import repair


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_allowed_guild()
    @commands.command(name="r")
    async def roll(self, ctx, expression: str = "1d100", *, desc: str = "Result"):
        result, total = dice_roll(expression)
        if result is not None:
            send_message = f"<@{ctx.author.id}> \N{Game Die}\n**{desc}**: {result}\n**Total**: {total}"
            await ctx.send(send_message)
        else:
            await ctx.send("**Error**: 不明なエラーが発生しました")

    @check_allowed_guild()
    @commands.command(name="rr")
    async def multi_roll(self, ctx, count: str, expression: str, *, desc: str = None):
        # カウントが整数ではない
        if not count.isdecimal():
            await ctx.send("**Error**: 不明なエラーが発生しました")
            return

        count = int(count)
        if 0 >= count > 100:
            await ctx.send("**Error**: Dice count is too many.")
            return

        send_message = f"<@{ctx.author.id}> \N{Game Die}\n"
        if desc != None:
            send_message += f"{desc}: Rolling {count} iterations...\n"
        else:
            send_message += f"Rolling {count} iterations...\n"
        totals = 0

        for i in range(count):
            result, total = dice_roll(expression)
            if result is not None:
                send_message += f"{result} = `{total}`\n"
                totals += total
            else:
                await ctx.send("**Error**: 不明なエラーが発生しました")
                return
        send_message += f"{totals} total."
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="part")
    async def part(self, ctx, kind, skill, count):
        send_message = f"使用者:<@{ctx.author.id}>\n" + part(kind, skill, count)
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="auto")
    async def charamake(self, ctx):
        send_message = f"使用者:<@{ctx.author.id}>\n" + auto()
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="gather")
    async def gather(self, ctx, kind, count, skill):
        send_message = f"使用者:<@{ctx.author.id}>\n" + gather(kind, count, skill)
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="fell")
    async def fell(self, ctx, kind, count, skill):
        send_message = f"使用者:<@{ctx.author.id}>\n" + fell(kind, count, skill)
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="mine")
    async def mine(self, ctx, kind, count, skill):
        send_message = f"使用者:<@{ctx.author.id}>\n" + mine(kind, count, skill)
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="gacha")
    async def gacha(self, ctx, kind, count):
        send_message = f"使用者<@{ctx.author.id}>" + gacha(kind, count)
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="repair")
    async def repair(self, ctx, count, skill, now, max):
        send_message = f"使用者<@{ctx.author.id}>" + repair(count, skill, now, max)
        await ctx.send(send_message)


async def setup(bot):
    await bot.add_cog(General(bot))
