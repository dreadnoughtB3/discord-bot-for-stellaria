from discord.ext import commands

ALLOWED_SERVERS = [938415626534404106, 1308044156517617675]


def get_guild_ids():
    return ALLOWED_SERVERS


def check_allowed_guild():
    async def predicate(ctx):
        if ctx.guild and ctx.guild.id in ALLOWED_SERVERS:
            return True
        return False

    return commands.check(predicate)
