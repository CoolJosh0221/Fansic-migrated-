from datetime import timedelta
from discord.ext import commands
import discord
from typing import Optional
from discord import Option
from discord.ext.commands import MissingPermissions


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="timeout", description="mutes/timeouts a member")
    @commands.has_permissions(moderate_members=True)
    async def timeout(
        self,
        ctx,
        member: Option(discord.Member, required=True),
        reason: Option(str, required=False),
        days: Option(int, max_value=27, default=0, required=False),
        hours: Option(int, default=0, required=False),
        minutes: Option(int, default=0, required=False),
        seconds: Option(int, default=0, required=False),
    ):  # setting each value with a default value of 0 reduces a lot of the code
        if member.id == ctx.author.id:
            await ctx.respond("You can't timeout yourself!")
            return
        if member.guild_permissions.moderate_members:
            await ctx.respond("You can't do this, this person is a moderator!")
            return
        duration = timedelta(days=days, hours=hours,
                             minutes=minutes, seconds=seconds)
        # added to check if time exceeds 28 days
        if duration >= timedelta(days=28):
            await ctx.respond(
                "I can't mute someone for more than 28 days!", ephemeral=True
            )  # responds, but only the author can see the response
            return
        if reason == None:
            await member.timeout_for(duration)
            await ctx.respond(
                f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>."
            )
            await member.send(
                f"You have been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>."
            )
        else:
            await member.timeout_for(duration, reason=reason)
            await ctx.respond(
                f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'."
            )
            await member.send(
                f"You have been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'."
            )

    @timeout.error
    async def timeouterror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond(
                "You can't do this! You need to have moderate members permissions!"
            )
        else:
            raise error

    @commands.slash_command(name="unmute", description="unmutes/untimeouts a member")
    @commands.has_permissions(moderate_members=True)
    async def unmute(
        self,
        ctx,
        member: Option(discord.Member, required=True),
        reason: Option(str, required=False),
    ):
        if reason == None:
            await member.remove_timeout()
            await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
        else:
            await member.remove_timeout(reason=reason)
            await ctx.respond(
                f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'."
            )

    @unmute.error
    async def unmuteerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond(
                "You can't do this! You need to have moderate members permissions!"
            )
        else:
            raise error


def setup(bot):
    bot.add_cog(Mod(bot))
