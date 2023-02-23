import discord
from discord.ext import commands
import json

def fetchconfig(key):
    with open('config.json') as f:
        data = json.load(f)
        print(key)
        value = data[0][key]
        return value

    # --

def update_config(key, new_value):
    with open('config.json', 'r') as f:
        data = json.load(f)

    data[0][key] = new_value

    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)


class Configs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_owner_role(self, ctx, new_role:discord.Role):
        update_config("ownerRole", str(new_role.id))
        await ctx.send(f"Ändrade `ownerRole` till {new_role.mention}")

    @commands.command()
    async def set_admin_role(self, ctx, new_role:discord.Role):
        update_config("adminRole", str(new_role.id))
        await ctx.send(f"Ändrade `adminRole` till {new_role.mention}")

    @commands.command()
    async def set_moderator_role(self, ctx, new_role:discord.Role):
        update_config("moderatorRole", str(new_role.id))
        await ctx.send(f"Ändrade `moderatorRole` till {new_role.mention}")

    @commands.command()
    async def test(self, ctx):
        value = fetchconfig("errorEmoji")
        await ctx.send(value)

    @commands.command()
    async def set_muted_role(self, ctx, new_role:discord.Role):
        update_config("mutedRole", str(new_role.id))
        await ctx.send(f"Ändrade `mutedRole` till {new_role.mention}")
    
    @commands.command()
    async def set_check_emoji(self, ctx, new_emoji:discord.Emoji):
        update_config("checkEmoji", str(new_emoji.id))
        await ctx.send(f"Ändrade `checkEmoji` till {new_emoji}")

    @commands.command()
    async def set_error_emoji(self, ctx, new_emoji:discord.Emoji):
        update_config("errorEmoji", str(new_emoji.id))
        await ctx.send(f"Ändrade `errorEmoji` till {new_emoji}")

    @commands.command()
    async def set_info_emoji(self, ctx, new_emoji:discord.Emoji):
        update_config("infoEmoji", str(new_emoji.id))
        await ctx.send(f"Ändrade `infoEmoji` till {new_emoji}")  

async def setup(bot):
    await bot.add_cog(Configs(bot))