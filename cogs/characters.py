import discord
from typing import Union
from discord.ext import commands
from discord import app_commands
from utils.check_guild import check_allowed_guild
from utils.db import add_character, get_character, delete_character
from utils.characters_cache import (
    get_character_cache,
    delete_character_cache,
    set_character_cache,
)


class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_allowed_guild()
    @commands.command(name="create")
    async def create_chracter(self, ctx, name: str = None, avatar: str = None):
        if not name or not avatar:
            await ctx.send("> 必要な情報が不足しています")
            return
        res = add_character(ctx.author.id, name, avatar)
        set_character_cache(ctx.author.id, str(res), name, avatar)
        await ctx.send(f"> {res}番でキャラクターを追加しました")

    @check_allowed_guild()
    @commands.command(name="send")
    async def send_message(
        self,
        ctx,
        character_idx: str = None,
        content: str = None,
        channel_id: str = None,
    ):
        if not character_idx or not character_idx.isdecimal() or not content:
            await ctx.send("> 引数が不正です")
            return

        cache = get_character_cache(ctx.author.id, character_idx)
        # キャッシュが存在する場合
        if cache:
            name = cache["name"]
            avatar_url = cache["avatar"]
            status = True
        # 存在しない場合
        else:
            status, name, avatar_url = get_character(ctx.author.id, character_idx)
        if not status:
            await ctx.send("> キャラクターが存在しません")
            return

        # 取得したデータをキャッシュに保存
        if not cache:
            set_character_cache(ctx.author.id, character_idx, name, avatar_url)

        if channel_id and channel_id.isdecimal():
            channel = self.bot.get_channel(int(channel_id))
        else:
            channel = ctx.channel
        if not channel:
            await ctx.send("> チャンネルが存在しません")
            return

        webhook = await channel.create_webhook(name="tmp")
        content += f"\n-# 送信者: {ctx.author.name}"
        await webhook.send(
            content=content, username=name, wait=True, avatar_url=avatar_url
        )
        await webhook.delete()

    @check_allowed_guild()
    @commands.command(name="delete")
    async def delete_character(self, ctx, character_idx: str = None):
        if not character_idx or not character_idx.isdecimal():
            await ctx.send("> キャラクターIDが不正です")
            return

        res = delete_character(ctx.author.id, character_idx)
        if res:
            delete_character_cache(ctx.author.id, character_idx)
            await ctx.send(f"> {character_idx}番のキャラクターを削除しました")
        else:
            await ctx.send("> 不明なエラーが発生しました")

    @app_commands.command(
        name="say", description="Say something with webhook character."
    )
    async def slash_send(
        self,
        interaction: discord.Interaction,
        character_idx: int,
        content: str,
        target: Union[discord.TextChannel, discord.Thread] = None,
    ):
        cache = get_character_cache(interaction.user.id, character_idx)
        # キャッシュが存在する場合
        if cache:
            name = cache["name"]
            avatar_url = cache["avatar"]
            status = True
        # 存在しない場合
        else:
            status, name, avatar_url = get_character(interaction.user.id, character_idx)
        if not status:
            await interaction.response.send_message(
                "> キャラクターが存在しません", ephemeral=True
            )
            return

        # 取得したデータをキャッシュに保存
        if not cache:
            set_character_cache(interaction.user.id, character_idx, name, avatar_url)

        # ターゲットが指定されており、スレッドかテキストチャンネルの場合
        if isinstance(target, discord.TextChannel):
            channel = self.bot.get_channel(target.id)
        elif isinstance(target, discord.Thread):
            channel = self.bot.get_channel(target.parent_id)
        else:
            channel = self.bot.get_channel(interaction.channel_id)

        webhook = await channel.create_webhook(name="tmp")
        content += f"\n-# 送信者: {interaction.user.name}"
        if isinstance(target, discord.Thread):
            await webhook.send(
                content=content,
                username=name,
                wait=True,
                avatar_url=avatar_url,
                thread=target,
            )
        else:
            await webhook.send(
                content=content, username=name, wait=True, avatar_url=avatar_url
            )
        await webhook.delete()
        await interaction.response.send_message(
            "> 送信しました", ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Character(bot))
