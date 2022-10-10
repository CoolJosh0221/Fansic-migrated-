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


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    settings = SlashCommandGroup("settings", "Settings Commands")

    config_items = ['swear/curse detector']

    @settings.command(name="toggle", description="Toggle settings on/off")
    @commands.has_permissions(administrator=True)
    async def toggle(self, ctx, setting: Option(str, description="The setting name you want to toggle on/off.", required=True, autocomplete=config_items)):
        if setting == 'swear/curse detector':
            pass


def setup(bot):
    bot.add_cog(Settings(bot))
