from discord.ext import commands
from utils.check_guild import check_allowed_guild


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_allowed_guild()
    @commands.command(name="tea")
    async def tea(self, ctx):
        send_message = "https://tenor.com/view/tea-tea-time-black-tea-crockery-finechina-gif-19858737"
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="cake")
    async def cake(self, ctx):
        send_message = "https://tenor.com/view/lemon-meringue-pie-pies-dessert-pie-gif-2665188071120448341"
        await ctx.send(send_message)

    @check_allowed_guild()
    @commands.command(name="pizza")
    async def pizza(self, ctx):
        send_message = "https://tenor.com/view/wtf-so-delicious-yummy-grr-i-want-more-pizza-lover-gif-26149617"
        await ctx.send(send_message)


async def setup(bot):
    await bot.add_cog(Fun(bot))
