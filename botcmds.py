import discord
from dotenv import load_dotenv
import os
import asyncio
from discord import Option
from datetime import timedelta
from discord.ext import commands
from discord.ext.commands import MissingPermissions

load_dotenv() #load the dotenv module to prevent tokens from being seen by others


from discord import guild
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)



@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}.")
    print("Bot is now ready!")
    game = discord.Game("Developing...")
    await bot.change_presence(status=discord.Status.dnd, activity=game)

@bot.event
async def on_message(message):
    msg = message.content
    msg = msg.upper()
    if message.author.bot:
        return
    if "XD" in msg:
        await message.channel.send('XDD')
    if "WOW" in msg:
        await message.channel.send('Oh wow.')
    if "LOL" in msg:
        await message.channel.send('🤣')
    if "HEHE" in msg:
        await message.add_reaction('😂')
        await message.channel.send('haha')
    if "SAD" in msg:
        await message.channel.send(':(')
    if "CHECKMATE" in msg:
        await message.add_reaction('<:checkmate_black_256x:983718638022426634>')
    if "HA" in msg:
        await message.channel.send('HA')
    if "@everyone" in msg or "@here" in msg:
        await message.add_reaction('📣')


testing_servers = [877823624315301908]

@bot.slash_command(guild_ids=testing_servers, name="check", description="Check if I am online")
async def check(ctx):
    await ctx.respond(f"**I am working!** \n\nLatency: {bot.latency*1000} ms.")


@bot.slash_command(name = 'timeout', description = "mutes/timeouts a member")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself!")
        return
    if member.guild_permissions.moderate_members:
        await ctx.respond("You can't do this, this person is a moderator!")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True) #responds, but only the author can see the response
        return
    if reason == None:
        await member.timeout_for(duration)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
    else:
        await member.timeout_for(duration, reason = reason)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error

@bot.slash_command(name = 'unmute', description = "unmutes/untimeouts a member")
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
    else:
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

@unmute.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error
    
token = str(os.getenv("TOKEN"))
bot.run(token)