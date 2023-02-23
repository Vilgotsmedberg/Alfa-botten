import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()


class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension('cogs.modcommands')
        await self.load_extension('cogs.configs')

bot = MyBot(command_prefix='!', intents=intents)

@bot.event
async def on_connect():
    print(f"Logged in as {bot.user}")

@bot.command()
async def prefix(ctx, prefix):
    bot.command_prefix = prefix
    await ctx.send(f"Ändrade kommandoprefixet till `{prefix}`")

@bot.command()
async def ping(ctx):
    await ctx.send("Hello!")


bot.run(TOKEN)