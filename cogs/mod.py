import asyncio
from datetime import timedelta
from http import client
from customized_functions.handle_error import handle_error

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

        if member.top_role.position >= ctx.guild.get_member(self.bot.user.id).top_role.position:
            await ctx.respond("Failed: My role is lower than that member!")

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
            result = handle_error(error)
            await ctx.respond(f"```fix\n{result[0]}```", embeds=result[1])

    @commands.slash_command(name="unmute", description="unmutes/untimeouts a member")
    @commands.has_permissions(moderate_members=True)
    async def unmute(
        self,
        ctx,
        member: Option(discord.Member, required=True),
        reason: Option(str, required=False),
    ):
        if member.top_role.position >= ctx.guild.get_member(self.bot.user.id).top_role.position:
            await ctx.respond("Failed: My role is lower than that member!")
            return
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
            result = handle_error(error)
            await ctx.respond(f"```fix\n{result[0]}```", embeds=result[1])

    @commands.slash_command(name="lock", description="Lock the channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.channel.send(f"** {ctx.channel.mention} Channel has been locked **")

        await ctx.respond("Channel has been locked", ephemeral=True)

    @commands.slash_command(name="unlock", description="Unlock the channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.channel.send(f"** {ctx.channel.mention} Channel has been unlocked **")

        await ctx.respond("Channel has been unlocked", ephemeral=True)

    @commands.slash_command(name="kick", description="Kicks a member from the server")
    @commands.has_permissions(moderate_members=True)
    async def kick(self, ctx, member: Option(discord.Member, required=True), reason: Option(str) = None):
        if reason == None:
            reason = "No reason provided"
        if member.guild_permissions.moderate_members:
            await ctx.respond("You can't do this, this person is a moderator!")
            return
        if ctx.author == member:
            await ctx.respond("You can't kick yourself, leave this server instead 😆")
            return
        if member not in ctx.guild.members:
            await ctx.respond("You can't kick a user that is not in this server!")
            return
        if member.top_role.position >= ctx.guild.get_member(self.bot.user.id).top_role.position:
            await ctx.respond("Failed: My role is lower than that member!")
            return
        if member in ctx.guild.members:
            await ctx.guild.kick(member)
            await ctx.respond(f'User {member.mention} has been kicked for {reason} by {ctx.author.mention}')

    @kick.error
    async def kickerror(self, ctx, error):
        print(error.original)
        if isinstance(error, MissingPermissions):
            await ctx.respond(
                "You can't do this! You need to have moderate members permissions!"
            )
        else:
            result = handle_error(error)
            await ctx.respond(f"```fix\n{result[0]}```", embeds=result[1])

    @commands.slash_command(name="clear", description="Delete a channel's messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: Option(int, required=True, description="Amount of messages to clear.")):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared by {ctx.author.mention}')

    @clear.error
    async def timeouterror(self, ctx, error):
        print(error.original)
        if isinstance(error, MissingPermissions):
            await ctx.respond(
                "You can't do this! You need to have manage messages permissions!"
            )
        else:
            result = handle_error(error)
            await ctx.respond(f"```fix\n{result[0]}```", embeds=result[1])


def setup(bot):
    bot.add_cog(Mod(bot))
