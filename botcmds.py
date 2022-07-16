import discord
import random
from discord.ui import Button, View, InputText, Modal
from dotenv import load_dotenv
import os
import asyncio
import asyncpg
from discord import Option
from datetime import timedelta, datetime
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from better_profanity import profanity

    
load_dotenv() #load the dotenv module to prevent tokens from being seen by others
profanity.load_censor_words()


from discord import guild
intents = discord.Intents.all()
intents.message_content = True

bot = discord.Bot(intents=intents)


async def connect():
    sql = str(os.getenv("SQL"))
    conn = await asyncpg.connect(sql)
    
    



@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}.")
    print("Bot is now ready!")
    print("================================================================\n\n")
    for guild in bot.guilds:
        print(guild.name)
        link = await guild.text_channels[0].create_invite()
        print(link)
    while True:
        await bot.change_presence(status=discord.Status.streaming, activity=discord.Streaming(url="https://www.twitch.tv/mynameisjoshes0221", name=f"in {len(bot.guilds)} servers"))
        await asyncio.sleep(20)

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
    if "HEHE" in msg:
        await message.add_reaction('😂')
        await message.channel.send('haha')
    if "SAD" in msg:
        await message.channel.send(':(')
    if "CHECKMATE" in msg:
        await message.add_reaction('<:checkmate_black_256x:983718638022426634>')
    if "@everyone" in message.content or "@here" in message.content:
        await message.add_reaction('📣')
    # if "SPAM" in msg:
    #     embed = discord.Embed(
    #         title="Do you want to spam?",
    #         description="You can spam in <#941232755864391701> in the server: https://discord.gg/QwXXNGNkeh !",
    #         color=discord.Colour.blurple(),
    #     )
    #     embed.set_image(url="https://cdn.discordapp.com/icons/877823624315301908/b2c3dc6917dc9779586b5166fa7eda64.png?size=4096")
    #     embed.set_footer(text=f"Requested by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar)
    #     await message.channel.send(message.author.mention, embed=embed)
        
    if profanity.contains_profanity(message.content):
        if message.author.guild_permissions.moderate_members:
            return
        
        
        await message.delete()
        await message.channel.send(f"========================\n{profanity.censor(message.content, '#')} \n\n - **{message.author.name}#{message.author.discriminator}**")
        embed = discord.Embed(
            title="Don't swear/curse!",
            description="Do not swear/curse anymore otherwise we will punish you!",
            color=discord.Colour.red()
        )
        
        await message.channel.send(content=message.author.mention, embed=embed)
        with open('swear.txt', 'w') as f:
            f.write(message.content)
        file = discord.File("swear.txt")
        await message.guild.owner.send(f"{message.author.name}#{message.author.discriminator} sweared/cursed id = {message.author.id}", file=file)
        
        

        
        
        


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
async def announce(ctx, text : Option(str, required=False),title : Option(str, required=True), value : Option(str, required=True), annchannel : Option(discord.TextChannel, channel_types=[discord.ChannelType(5)], required=True),):
    print(annchannel.id)
    embed = discord.Embed(
        title = title,
        description = value,
        color = ctx.author.color,
    )
    embed.set_author(name = f"Announcement from {ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.avatar)
    embed.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon)
    sending = await ctx.respond("Sending...", ephemeral = True)
    await annchannel.send(f"{text}", embed = embed)
    await sending.edit_original_message(content="Sended!")

        
@announce.error
async def announceerror(ctx,error):
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

@bot.slash_command(name="nitrogen", description="Gift you nitro.")
async def nitrogen(ctx):
    embed = discord.Embed(
        title="You've been gifted a subscription!",
        description=f"{ctx.author.name}#{ctx.author.discriminator} gifted you **nitro classic** for ***1 year***!",
        color=0x5964f3
    )
    embed.set_thumbnail(url="https://www.nukebot.org/Nitro.png")
    
    embed2 = discord.Embed(
        title="You've been gifted a subscription!",
        description="Hmm, it seems someone already claimed this gift.",
        color=0x5964f3
    )
    embed2.set_thumbnail(url="https://www.nukebot.org/Nitro.png")
    button=Button(label="Accept", style=discord.ButtonStyle.green, emoji="<a:the_nitro:986455622260244510>")
    button2=Button(label="Accept", style=discord.ButtonStyle.green, emoji="<a:the_nitro:986455622260244510>", disabled=True)
    async def button_callback(interaction):
        await interaction.response.edit_message(embed=embed2, view=view2)
        await interaction.followup.send("https://imgur.com/NQinKJB", ephemeral=True)
        
    
    button.callback = button_callback
    view = View()
    view2 = View()
    view2.add_item(button2)
    view.add_item(button)
    await ctx.respond("✅", ephemeral=True)
    await ctx.send(embed=embed, view=view)
    
    
    
# @bot.slash_command(name="gcreate", description="Create a giveaway (interactive setup)")
# async def gcreate(ctx):
#     embed=discord.Embed(
#         title="What do you want to giveaway?",
#         description="Example: `1 x Nitro`",
#         color=discord.Colour.orange()
#     )
    
#     timeout=discord.Embed(
#         title="Your Time Ran Out!",
#         description="Please try again using /gcreate",
#         color=discord.Color.red()
#     )
#     await ctx.respond(embed=embed)
#     def name(m):
#         return m.author == ctx.author and m.channel == ctx.channel
        
        
#     try:
#         msg = await bot.wait_for('message', check=name, timeout=60.0)
#     except asyncio.TimeoutError:
#         await ctx.channel.send(embed=timeout)
#         return
    
    
#     embed=discord.Embed(
#         title="Which channel should it be?",
#         description="Simply mention the channel.",
#         color=discord.Colour.orange()
#     )
    
    
#     await ctx.channel.send(embed=embed)
    
#     async def channel(m):
        
    
#     try:
#         gchannel = await bot.wait_for('message', check=channel, timeout=60.0)
#     except asyncio.TimeoutError:
#         await ctx.channel.send(embed=timeout)
#         return
    
#     name = msg.content
#     #channel = bot.get_channel(int(gchannel.content))
    
    
@bot.slash_command(name="gstart", description="Start a giveaway")
async def gstart(ctx, gchannel: Option(discord.TextChannel, required=True), prize: Option(str, required=True), time: Option(int, "Time (seconds)", required=True)):
    await ctx.respond("Giveaway created.", ephemeral=True)
    end_time = round(datetime.timestamp(datetime.now()) + time)
    embed=discord.Embed(
        title=prize,
        description=f"React with <a:tada2:987204661838753792> to enter!\nEnds in: <t:{end_time}:R>\nHosted by {ctx.author.mention}",
        color=discord.Color.orange()
    )
    embed.set_author(name="GIVEAWAY TIME!", icon_url="https://i.imgur.com/DDric14.png")
    giveaway_msg = await gchannel.send("<a:tada3:987204676292313108> **GIVEAWAY STARTED** <a:tada3:987204676292313108>", embed=embed)
    await giveaway_msg.add_reaction("<a:tada2:987204661838753792>")
    
    await asyncio.sleep(time)
    new_message = await gchannel.fetch_message(giveaway_msg.id)
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    entrants = discord.Embed(
        title=None,
        description=f"**{len(users)}** entrants ↗"
    ) 
    
    if users == []:
        await gchannel.send("No valid entrants, so a winner could not be determined!", embed=entrants)
        return
    
    winner = random.choice(users)
    embed = discord.Embed(
        title=prize,
        description=f"Winner: {winner.mention}\nEnds in: <t:{end_time}:R>\nHosted by {ctx.author.mention}",
        color=discord.Color.orange()
    )
    
    embed.set_author(name="GIVEAWAY TIME!", icon_url="https://i.imgur.com/DDric14.png")
    await giveaway_msg.edit("<a:tada3:987204676292313108> **GIVEAWAY ENDED** <a:tada3:987204676292313108>", embed=embed)
    
    ann = await gchannel.send(f"**Congrats!** {winner.mention}, you won **{prize}**!", embed=entrants)
    congrats = ["🇨", "🇴", "🇳", "🇬", "🇷", "🇦", "🇹", "🇸"]
    
    
    for emoji in congrats:
        await ann.add_reaction(emoji)
        
        
@bot.slash_command(name="suggest", description="Make a suggestion for the bot.", )
async def suggest(ctx, suggestion: Option(str, required=True)):
    channel = bot.get_channel(996944121073782914)
    embed = discord.Embed(title = f"Suggestion by {ctx.author.name}#{ctx.author.discriminator}:", 
                          description=f"{ctx.author.mention}: {suggestion}",
                          color = ctx.author.color,)
    embed.set_footer(text=ctx.guild, icon_url=ctx.guild.icon)
    msg = await channel.send(embed = embed)
    await ctx.respond("We've posted your suggestion in our support server!",ephemeral=True)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")


@bot.slash_command(name="say", description="Make the bot say something.",)
@commands.has_permissions(moderate_members = True)
async def say(ctx, msg: Option(str, required=True)):
    await ctx.channel.send(msg)
    await ctx.respond("Message sent.", ephemeral=True)


@bot.slash_command(name = "lock", description="Lock the channel")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.channel.send(f'** {ctx.channel.mention} Channel has been locked **')

    await ctx.respond("Channel has been locked",ephemeral=True)

@bot.slash_command(name = "unlock", description="Unlock the channel")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=True)
    await ctx.channel.send(f'** {ctx.channel.mention} Channel has been unlocked **')

    await ctx.respond("Channel has been unlocked", ephemeral=True)
    
@bot.slash_command(name = "invite", description="Invite the bot to your server!")
async def invite(ctx):
    await ctx.respond("[Click here to invite the bot to your server](https://discord.com/api/oauth2/authorize?client_id=918477034232119306&permissions=8&scope=bot%20applications.commands)")
    
# for file in os.listdir("./cogs"):
#     if file.endswith(".py"):
#         bot.load_extension("cogs." + file[:-3])
    
token = str(os.getenv("TOKEN"))
bot.run(token)