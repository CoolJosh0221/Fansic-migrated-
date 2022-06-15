import discord
from discord.ui import Button, View
from dotenv import load_dotenv
import os
import asyncio
from discord import Option
from datetime import timedelta, datetime
from discord.ext import commands
from discord.ext.commands import MissingPermissions

load_dotenv() #load the dotenv module to prevent tokens from being seen by others


from discord import guild
intents = discord.Intents.all()
intents.message_content = True

bot = discord.Bot(intents=intents)



@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}.")
    print("Bot is now ready!")
    #game = discord.Game("Developing...")
    await bot.change_presence(status=discord.Status.streaming, activity=discord.Streaming(url="https://www.twitch.tv/mynameisjoshes0221", name=f"in {len(bot.guilds)} servers"))

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
    if "@everyone" in message.content or "@here" in message.content:
        await message.add_reaction('📣')
    if "SPAM" in msg:
        embed = discord.Embed(
            title="Do you want to spam?",
            description="You can spam in <#941232755864391701> in the server: https://discord.gg/QwXXNGNkeh !",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url="https://cdn.discordapp.com/icons/877823624315301908/b2c3dc6917dc9779586b5166fa7eda64.png?size=4096")
        embed.set_footer(text=f"Requested by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar)
        await message.channel.send(message.author.mention, embed=embed)
        


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
        await member.send(f"You have been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
    else:
        await member.timeout_for(duration, reason = reason)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")
        await member.send(f"You have been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

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
    
@bot.slash_command(name="whois", description="Get information from a specified user.")
async def whois(ctx, user: Option(discord.Member, default=None, required = False)):
    if user == None:
        fetch_user = ctx.author
    else:
        fetch_user = user
    
            
    
    embed=discord.Embed(
        title=f'{fetch_user.name}#{fetch_user.discriminator}',
        description=fetch_user.mention,
        color=fetch_user.color,
    )
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    embed.add_field(name="Avatar URL", value=f"[Here]({fetch_user.avatar})", inline=False)
    embed.add_field(name="ID", value=str(fetch_user.id), inline=False)
    embed.add_field(name="Joined time", value=f"<t:{round(fetch_user.joined_at.timestamp())}>", inline=True)
    embed.add_field(name="Account Creation", value=f"<t:{round(fetch_user.created_at.timestamp())}>", inline=True)
    embed.set_thumbnail(url=fetch_user.avatar)
    embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} | Today at {current_time}", icon_url=ctx.author.avatar)
    embed.set_author(name="User Imformation", icon_url=fetch_user.avatar)

    await ctx.respond("", embed=embed)
    
    
@bot.slash_command(name="announce", description="Announce something in a channel")
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 20, commands.BucketType.user)  # the command can only be used once in 60 seconds
async def announce(ctx, text : Option(str, required=True),title : Option(str, required=True), value : Option(str, required=True), annchannel : Option(discord.TextChannel, required=True),):
    embed = discord.Embed(
        title = title,
        description = value,
        color = ctx.author.color,
    )
    embed.set_author(name = f"Announcement from {ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.avatar)
    embed.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon)
    sending = await ctx.respond("Sending...")
    await annchannel.send(f"{text}", embed = embed)
    await sending.edit_original_message(content="Completed!")

        
@announce.error
async def dmannounceerror(ctx,error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have administrator permissions!", ephemeral=True) 
    elif isinstance(error, commands.CommandOnCooldown):
        cooldown = error.retry_after
        await ctx.respond(f"This command is currently on cooldown. Wait {round(cooldown)} seconds to try again.", ephemeral=True)
    else:
        try:
            raise error    # raise other errors so they aren't ignored
        except Exception as e:
            await ctx.respond(f"```fix\n{e}```")
            
        embed = discord.Embed(
            title="Something went wrong!",
            description="Join [our server](https://discord.gg/QwXXNGNkeh) to report this issue.",
            color=0xFF0000
        )
        await ctx.respond(embed=embed)
        
        raise error

@bot.slash_command(name="info", description="Get the info of the bot")
async def info(ctx):
    button = Button(label="View GitHub Repository", style=discord.ButtonStyle.link, url="https://github.com/CoolJosh0221/Fansic")
    view = View()
    view.add_item(button)
    
    embed = discord.Embed(
        title="Info",
        description="The bot is made by <@!847772018928779285> \nJoin our discord server: https://discord.gg/QwXXNGNkeh",
        color=0xFF8800
    )
    embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar)
    embed.set_author(name="Bot Info")

    
    await ctx.respond(embed=embed, view=view)
    
token = str(os.getenv("TOKEN"))
bot.run(token)