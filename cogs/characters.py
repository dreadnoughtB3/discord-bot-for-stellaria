from discord.ext import commands
from utils.check_guild import check_allowed_guild
from utils.db import add_character, get_character


class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_allowed_guild()
    @commands.command(name="create")
    async def create_chracter(self, ctx, name: str, avatar: str):
        res = add_character(ctx.author.id, name, avatar)
        await ctx.send(f"{res}番でキャラクターを追加しました")

    @check_allowed_guild()
    @commands.command(name="send")
    async def send_message(self, ctx, character_idx: str = None, content: str = None, channel_id: str = None):
        status, name, avatar_url = get_character(ctx.author.id, character_idx)
        if not status:
            await ctx.send("キャラクターが存在しません")
            return
        if channel_id and channel_id.isdecimal():
            channel = self.bot.get_channel(int(channel_id))
        else:
            channel = ctx.channel
        if not channel:
            await ctx.send("チャンネルが存在しません")
            return
        webhook = await channel.create_webhook(name="tmp")
        await webhook.send(
            content=content, username=name, wait=True, avatar_url=avatar_url
        )
        await webhook.delete()


async def setup(bot):
    await bot.add_cog(Character(bot))
