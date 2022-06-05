import discord
from dotenv import load_dotenv
import os
import asyncio

load_dotenv() #load the dotenv module to prevent tokens from being seen by others


from discord import guild

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}.")
    print("Bot is now ready!")


testing_servers = [877823624315301908]

@bot.slash_command(guild_ids=testing_servers, name="check", description="Check if I am online")
async def check(ctx):
    await ctx.respond(f"**I am working!** \n\nLatency: {bot.latency*1000} ms.")
    
token = str(os.getenv("TOKEN"))
    
bot.run(token)