from discord.ext import commands
from utils.check_guild import check_allowed_guild


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_allowed_guild()
    @commands.command(name="overwrite_stock")
    async def tea(self, ctx):
        files = ctx.message.attachments
        if len(files) != 2:
            return

        await ctx.send("データを上書きしました")


async def setup(bot):
    await bot.add_cog(Admin(bot))
