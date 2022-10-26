import asyncio
from datetime import timedelta
from customized_functions.handle_error import handle_error
from discord.commands import SlashCommandGroup

from discord.ext import commands
import discord
from typing import Optional
from discord import Option
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv
import motor.motor_asyncio
import os

load_dotenv("../.env")
config_items = ['swear/curse detector']


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    settings = SlashCommandGroup("settings", "Settings Commands")

    async def get_config_items(ctx: discord.AutocompleteContext):
        return [items for items in config_items if items.startswith(ctx.value.lower())]

    @settings.command(name="config", description="Change the setting.")
    @commands.has_permissions(administrator=True)
    async def toggle(self, ctx,
                     setting: Option(str, description="The setting name you want to change.", required=True, autocomplete=get_config_items),

                     option: Option(str, description="The settings to change.", required=True)):
        settings_db = self.bot.cluster["bot"]["settings"]
        if setting == 'swear/curse detector':
            pass


def setup(bot):
    bot.add_cog(Settings(bot))
