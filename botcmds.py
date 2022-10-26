import motor.motor_asyncio
from customized_functions.handle_error import handle_error
import asyncio
import os
import random
import logging
from datetime import datetime, timedelta

from better_profanity import profanity
from dotenv import load_dotenv

import discord
from discord import Option
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ui import Button, InputText, Modal, View
import sys

import logging.handlers
load_dotenv()  # load the dotenv module to prevent tokens from being seen by others


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(
    '[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

profanity.load_censor_words(whitelist_words=['god'])


intents = discord.Intents.all()
intents.message_content = True


bot = discord.Bot(intents=intents)
bot.cluster = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://josh:{str(os.getenv('mongo_pwd'))}@fansic.dwvvufz.mongodb.net/?retryWrites=true&w=majority&authSource=admin", serverSelectionTimeoutMS=5000)
print(bot.cluster.info)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}.")
    print("Bot is now ready!")
    print("================================================================\n\n")

    while True:
        try:
            await bot.get_channel(1018080842507108362).send(file=discord.File("discord.log"), content="\n")
            f = open('discord.log', 'r+')
            f.truncate(0)
            f.close()
        except discord.errors.HTTPException:
            pass

        await bot.change_presence(
            status=discord.Status.streaming,
            activity=discord.Streaming(
                url="https://www.twitch.tv/mynameisjoshes0221",
                name=f"in {len(bot.guilds)} servers",
            ),
        )
        await asyncio.sleep(20)


@bot.event
async def on_message(message):
    msg = message.content
    msg = msg.upper()
    if message.author.bot:
        return
    if "XD" in msg:
        await message.channel.send("XDD")
    if "WOW" in msg:
        await message.channel.send("Oh wow.")
    if "HEHE" in msg:
        await message.add_reaction("😂")
        await message.channel.send("haha")
    if "SAD" in msg:
        await message.channel.send(":(")
    if "CHECKMATE" in msg:
        await message.add_reaction("<:checkmate_black_256x:983718638022426634>")
    if "@everyone" in message.content or "@here" in message.content:
        await message.add_reaction("📣")

    if profanity.contains_profanity(message.content):
        if message.author.guild_permissions.moderate_members:
            return

        await message.delete()
        await message.channel.send(
            f"========================\n{profanity.censor(message.content, '#')} \n\n - **{message.author.name}#{message.author.discriminator}**"
        )
        embed = discord.Embed(
            title="Don't swear/curse!",
            description="Do not swear/curse anymore otherwise we will punish you!",
            color=discord.Colour.red(),
        )

        await message.channel.send(content=message.author.mention, embed=embed)
        with open("swear.txt", "w") as f:
            f.write(message.content)
        file = discord.File("swear.txt")
        await message.guild.owner.send(
            f"{message.author.name}#{message.author.discriminator} sweared/cursed id = {message.author.id}",
            file=file,
        )


testing_servers = [877823624315301908]


@bot.slash_command(
    guild_ids=testing_servers, name="check", description="Check if I am online"
)
async def check(ctx):
    await ctx.respond(f"**I am working!** \n\nLatency: {bot.latency*1000} ms.")


@bot.slash_command(name="whois", description="Get information from a specified user.")
async def whois(ctx, user: Option(discord.Member, default=None, required=False)):
    if user == None:
        fetch_user = ctx.author
    else:
        fetch_user = user

    embed = discord.Embed(
        title=f"{fetch_user.name}#{fetch_user.discriminator}",
        description=fetch_user.mention,
        color=fetch_user.color,
    )
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    embed.add_field(
        name="Avatar URL", value=f"[Here]({fetch_user.avatar})", inline=False
    )
    embed.add_field(name="ID", value=str(fetch_user.id), inline=False)
    embed.add_field(
        name="Joined time",
        value=f"<t:{round(fetch_user.joined_at.timestamp())}>",
        inline=True,
    )
    embed.add_field(
        name="Account Creation",
        value=f"<t:{round(fetch_user.created_at.timestamp())}>",
        inline=True,
    )
    embed.set_thumbnail(url=fetch_user.avatar)
    embed.set_footer(
        text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} | Today at {current_time}",
        icon_url=ctx.author.avatar,
    )
    embed.set_author(name="User Imformation", icon_url=fetch_user.avatar)

    await ctx.respond("", embed=embed)


@bot.slash_command(name="announce", description="Announce something in a channel")
@commands.has_permissions(administrator=True)
@commands.cooldown(
    1, 20, commands.BucketType.user
)  # the command can only be used once in 20  seconds
async def announce(
    ctx,
    title: Option(str, required=True),
    value: Option(str, required=True),
    annchannel: Option(
        discord.TextChannel, channel_types=[discord.ChannelType(5)], required=True
    ),
    text: Option(str, required=False),
):
    embed = discord.Embed(
        title=title,
        description=value,
        color=ctx.author.color,
    )
    embed.set_author(
        name=f"Announcement from {ctx.author.name}#{ctx.author.discriminator}",
        icon_url=ctx.author.avatar,
    )
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon)
    sending = await ctx.respond("Sending...", ephemeral=True)
    if text == None:
        await annchannel.send(embed=embed)
    else:
        await annchannel.send(f"{text}", embed=embed)
    await sending.edit_original_message(content="Sended!")


@announce.error
async def announceerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond(
            "You can't do this! You need to have administrator permissions!",
            ephemeral=True,
        )
    elif isinstance(error, commands.CommandOnCooldown):
        cooldown = error.retry_after
        await ctx.respond(
            f"This command is currently on cooldown. Wait {round(cooldown)} seconds to try again.",
            ephemeral=True,
        )
    else:
        result = handle_error(error)
        await ctx.respond(f"```fix\n{result[0]}```", embeds=result[1])


@bot.slash_command(name="info", description="Get the info of the bot")
async def info(ctx):
    button = Button(
        label="View GitHub Repository",
        style=discord.ButtonStyle.link,
        url="https://github.com/CoolJosh0221/Fansic",
    )
    view = View()
    view.add_item(button)

    embed = discord.Embed(
        title="Info",
        description="The bot is made by <@!847772018928779285> \nJoin our discord server: https://discord.gg/QwXXNGNkeh",
        color=0xFF8800,
    )
    embed.set_footer(
        text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
        icon_url=ctx.author.avatar,
    )
    embed.set_author(name="Bot Info")

    await ctx.respond(embed=embed, view=view)


@bot.slash_command(name="nitrogen", description="Gift you nitro.")
async def nitrogen(ctx):
    embed = discord.Embed(
        title="You've been gifted a subscription!",
        description=f"{ctx.author.name}#{ctx.author.discriminator} gifted you **nitro classic** for ***1 year***!",
        color=0x5964F3,
    )
    embed.set_thumbnail(url="https://www.nukebot.org/Nitro.png")

    embed2 = discord.Embed(
        title="You've been gifted a subscription!",
        description="Hmm, it seems someone already claimed this gift.",
        color=0x5964F3,
    )
    embed2.set_thumbnail(url="https://www.nukebot.org/Nitro.png")
    button = Button(
        label="Accept",
        style=discord.ButtonStyle.green,
        emoji="<a:the_nitro:986455622260244510>",
    )
    button2 = Button(
        label="Accept",
        style=discord.ButtonStyle.green,
        emoji="<a:the_nitro:986455622260244510>",
        disabled=True,
    )

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


@bot.slash_command(name="gstart", description="Start a giveaway")
async def gstart(
    ctx,
    gchannel: Option(discord.TextChannel, required=True),
    prize: Option(str, required=True),
    time: Option(int, "Time (seconds)", required=True),
):
    await ctx.respond("Giveaway created.", ephemeral=True)
    end_time = round(datetime.timestamp(datetime.now()) + time)
    embed = discord.Embed(
        title=prize,
        description=f"React with <a:tada2:987204661838753792> to enter!\nEnds in: <t:{end_time}:R>\nHosted by {ctx.author.mention}",
        color=discord.Color.orange(),
    )
    embed.set_author(name="GIVEAWAY TIME!",
                     icon_url="https://i.imgur.com/DDric14.png")
    giveaway_msg = await gchannel.send(
        "<a:tada3:987204676292313108> **GIVEAWAY STARTED** <a:tada3:987204676292313108>",
        embed=embed,
    )
    await giveaway_msg.add_reaction("<a:tada2:987204661838753792>")

    await asyncio.sleep(time)
    new_message = await gchannel.fetch_message(giveaway_msg.id)
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    entrants = discord.Embed(
        title=None, description=f"**{len(users)}** entrants ↗")

    if users == []:
        await gchannel.send(
            "No valid entrants, so a winner could not be determined!", embed=entrants
        )
        return

    winner = random.choice(users)
    embed = discord.Embed(
        title=prize,
        description=f"Winner: {winner.mention}\nEnds in: <t:{end_time}:R>\nHosted by {ctx.author.mention}",
        color=discord.Color.orange(),
    )

    embed.set_author(name="GIVEAWAY TIME!",
                     icon_url="https://i.imgur.com/DDric14.png")
    await giveaway_msg.edit(
        "<a:tada3:987204676292313108> **GIVEAWAY ENDED** <a:tada3:987204676292313108>",
        embed=embed,
    )

    ann = await gchannel.send(
        f"**Congrats!** {winner.mention}, you won **{prize}**!", embed=entrants
    )
    congrats = ["🇨", "🇴", "🇳", "🇬", "🇷", "🇦", "🇹", "🇸"]

    for emoji in congrats:
        await ann.add_reaction(emoji)


@bot.slash_command(
    name="suggest",
    description="Make a suggestion for the bot.",
)
async def suggest(ctx, suggestion: Option(str, required=True)):
    channel = bot.get_channel(996944121073782914)
    embed = discord.Embed(
        title=f"Suggestion by {ctx.author.name}#{ctx.author.discriminator}:",
        description=f"{ctx.author.mention}: {suggestion}",
        color=ctx.author.color,
    )
    embed.set_footer(text=ctx.guild, icon_url=ctx.guild.icon)
    msg = await channel.send(embed=embed)
    await ctx.respond(
        "We've posted your suggestion in our support server!", ephemeral=True
    )
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")


@bot.slash_command(
    name="say",
    description="Make the bot say something.",
)
@commands.has_permissions(moderate_members=True)
async def say(ctx, msg: Option(str, required=True)):
    await ctx.channel.send(msg)
    await ctx.respond("Message sent.", ephemeral=True)


@say.error
async def say_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond(
            "You can't do this! You need to have moderate members permissions!"
        )
    else:
        result = handle_error(error)
        await ctx.respond(f"```fix\n{result[0]}```", embeds=result[1])


@bot.slash_command(name="invite", description="Invite the bot to your server!")
async def invite(ctx):
    await ctx.respond(
        "[Click here to invite the bot to your server](https://discord.com/api/oauth2/authorize?client_id=918477034232119306&permissions=8&scope=bot%20applications.commands) "
    )

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension("cogs." + file[:-3])


token = str(os.getenv("TOKEN"))
bot.run(token)
