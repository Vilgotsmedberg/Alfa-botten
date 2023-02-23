import discord
from discord.ext import commands
import json
from datetime import date
import datetime

dictionary = {
    "976374657346467": {
        "warning1": {
            "reason": "memes in general",
            "date": "2023-02-18",
            "moderator": "Krösus sork#5072"
        }
    }
}
json_object = json.dumps(dictionary, indent=2)

def fetchconfig(key):
    with open('config.json') as f:
        data = json.load(f)
        value = data[0][key]
        return value



def getWarnings(discord_id):
    with open('warnings.json') as f:
        data = json.load(f)

    id_to_find = discord_id

    warnings = data.get(id_to_find)

    warning_messages = []
    reasons = []
    dates = []
    moderators = []

    if warnings:
        for warning in warnings.values():

            warning_message = f"Reason: {warning['reason']}, Date: {warning['date']}"
            reason = f"{warning['reason']}"
            date = f"{warning['date']}"
            moderator = f"{warning['moderator']}"

            warning_messages.append(warning_message)
            reasons.append(reason)
            dates.append(date)
            moderators.append(moderator)

    return warning_messages, reasons, dates, moderators;
       
def userInList(discord_id):
    f = open('warnings.json')
    data = json.load(f)
    if discord_id in data:
        return True
    else:
        return False


def addUser(discord_id, moderator, *, reason=None):
    with open("warnings.json", "r") as infile:

        time = datetime.datetime.now()
        x = f"{date.today()} {time.hour}.{time.minute}"

        all_dictionaries = json.load(infile)
        
        if discord_id in all_dictionaries:
            # User already has warnings, add a new one to the list
            num_warnings = len(all_dictionaries[discord_id])
            all_dictionaries[discord_id][f"warning{num_warnings+1}"] = {"reason": reason, "date": f"{x}", "moderator": f"{moderator}"}
        else:
            # User has no warnings, create a new list with one warning
            all_dictionaries[discord_id] = {"warning1": {"reason": reason, "date": f"{x}", "moderator": f"{moderator}"}}
        
        with open("warnings.json", "w") as outfile:
            json.dump(all_dictionaries, outfile, indent=2)


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    
    @commands.command()
    async def kick(self, ctx, member:discord.Member, *, reason=None):
        try:
            await member.kick()
            emoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("checkEmoji")))
            embed = discord.Embed(title = f'{emoji} Kickade {member.name}', description=f'{member.mention} har blivit kickad!', color=0x2ecc71)
            embed.set_footer(text= f"Kickad av {ctx.message.author.name}", icon_url=f"{ctx.message.author.avatar}")
            embed.set_thumbnail(url =f"{member.avatar}")

            if reason != None:
                embed.add_field(name="Anledning:", value=f"`{reason}`", inline=False)

            await ctx.send(embed=embed)

        except:
            value = int(fetchconfig("errorEmoji"))
            emoji = discord.utils.get(ctx.guild.emojis, id=value)
            embed = discord.Embed(title = f"{emoji} Fel", description=f"Kunde inte kicka {member.mention}", color=0xe74c3c)

            await ctx.send(embed=embed)

    @commands.command()
    async def ban(self, ctx, member:discord.Member, *, reason=None):
        try:
            await member.ban()
            emoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("checkEmoji")))
            embed = discord.Embed(title = f' {emoji} Bannade {member.name}', description=f'{member.mention} har blivit bannad!', color=0x2ecc71)
            embed.set_footer(text= f"Bannad av {ctx.message.author.name}", icon_url=f"{ctx.message.author.avatar}")
            embed.set_thumbnail(url =f"{member.avatar}")

            if reason != None:
                embed.add_field(name="Anledning:", value=f"`{reason}`", inline=False)

            await ctx.send(embed=embed)

        except:
            value = int(fetchconfig("errorEmoji"))
            emoji = discord.utils.get(ctx.guild.emojis, id=value)
            embed = discord.Embed(title = f"{emoji} Fel", description=f"Kunde inte banna {member.mention}", color=0xe74c3c)

            await ctx.send(embed=embed)
        
    @commands.command()
    async def mute(self, ctx, member:discord.Member, *, reason=None):
        value = int(fetchconfig("mutedRole"))

        role = discord.utils.get(ctx.guild.roles, id=value)
        await member.add_roles(role)

        
        emoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("checkEmoji")))
        embed = discord.Embed(title = f" {emoji} Mutade {member.name}", description=f"{member.mention} har blivit mutad!", color =0x2ecc71)
        embed.set_footer(text= f"Mutad av {ctx.message.author.name}", icon_url=f"{ctx.message.author.avatar}")
        embed.set_thumbnail(url =f"{member.avatar}")

        if reason != None:
            embed.add_field(name = "Anledning:", value = f"`{reason}`", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def unmute(self, ctx, member:discord.Member):
        value = int(fetchconfig("mutedRole"))
        role = discord.utils.get(ctx.guild.roles, id=value) 
        if role in member.roles:
            await member.remove_roles(role)
            emoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("checkEmoji")))
            embed = discord.Embed(title = f"{emoji} Unmutade {member.name}", description=f"{member.mention} har blivit unmutad!", color =0x2ecc71)
            embed.set_footer(text= f"Unmutad av {ctx.message.author.name}", icon_url=f"{ctx.message.author.avatar}")
            embed.set_thumbnail(url =f"{member.avatar}")

            await ctx.send(embed=embed)

        else:
            value = int(fetchconfig("errorEmoji"))
            emoji = discord.utils.get(ctx.guild.emojis, id=value) 
            embed = discord.Embed(title = f"{emoji} Fel", description=f"{member.mention} är inte mutad", color=0xe74c3c)
                   
            await ctx.send(embed=embed)

    @commands.command()
    async def lock(self, ctx, *, channel:discord.TextChannel=None):
        checkEmoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("checkEmoji")))
        if channel == None:
            await ctx.message.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = discord.Embed(title = f"{checkEmoji} Stängde ner {ctx.message.channel.mention}")
            await ctx.send(embed=embed)
        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = discord.Embed(title = f"{checkEmoji} Stängde ner {channel.mention}")
            await ctx.send(embed=embed)
    
    @commands.command()
    async def unlock(self, ctx, *, channel:discord.TextChannel=None):
        checkEmoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("checkEmoji")))
        if channel == None:
            await ctx.message.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            embed = discord.Embed(title = f"{checkEmoji} Låste upp {ctx.message.channel.mention}")
            await ctx.send(embed=embed)
        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            embed = discord.Embed(title = f"{checkEmoji} Låste upp {channel.mention}")
            await ctx.send(embed=embed)
    
    @commands.command()
    async def warn(self, ctx, user:discord.Member, *, reason=None):
        emoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("checkEmoji")))
        embed = discord.Embed(title = f"{emoji} {user.name} har blivit varnad!", color= 0x2ecc71)
        moderator = ctx.message.author
        if reason==None:
            addUser(str(user.id), moderator=moderator)
            await ctx.send(embed=embed)
        else:
            addUser(str(user.id), moderator=moderator ,reason=reason)
            embed.description = f"Anledning: `{reason}`"
            await ctx.send(embed=embed)


    @commands.command()
    async def warns(self, ctx, user:discord.Member):
        if userInList(str(user.id)) == True:
            warning_messages, reasons, dates, moderators = getWarnings(f"{user.id}")
            embed = discord.Embed(title = f"Varningar - {user}", color=0xe67e22)

            for i in range(0, len(reasons)):
                embed.add_field(name = f"{i+1} - Datum:", value=f"{dates[i]}", inline=True)
                embed.add_field(name = f"Anledning:", value=f"`{reasons[i]}`", inline=True)
                embed.add_field(name = "Moderator:", value= f"{moderators[i]}", inline=True)
            
            await ctx.send(embed=embed)
        
        else:
            emoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("infoEmoji")))
            embed = discord.Embed(description = f"{emoji} {user} har inte några varningar", color=0x3498db)
            await ctx.send(embed=embed)

    @commands.command()
    async def unwarn(self, ctx, user: discord.Member, warning_num: int):
        with open("warnings.json", "r") as infile:
            all_dictionaries = json.load(infile)

            # Check if the user has any warnings
            if str(user.id) not in all_dictionaries:
                emoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("errorEmoji")))
                embed = discord.Embed(title = f"{emoji} {user.name} har inte några varningar", color=0xe74c3c)
                await ctx.send(embed=embed)
                return

            # Check if the warning number is valid
            num_warnings = len(all_dictionaries[str(user.id)])
            if warning_num < 1 or warning_num > num_warnings:
                await ctx.send(f"Invalid warning number. {user.mention} has {num_warnings} warnings.")
                return

            # Remove the specified warning
            del all_dictionaries[str(user.id)][f"warning{warning_num}"]
            if num_warnings == 1:
                # If this was the last warning, remove the user from the dictionary entirely
                del all_dictionaries[str(user.id)]
            else:
                # If there are other warnings, shift their indices down to fill the gap
                for i in range(warning_num + 1, num_warnings + 1):
                    all_dictionaries[str(user.id)][f"warning{i-1}"] = all_dictionaries[str(user.id)][f"warning{i}"]
                    del all_dictionaries[str(user.id)][f"warning{i}"]

            with open("warnings.json", "w") as outfile:
                json.dump(all_dictionaries, outfile, indent=2)
            
            emoji = discord.utils.get(ctx.guild.emojis, id=int(fetchconfig("checkEmoji")))
            embed = discord.Embed(title = f"{emoji} Tog bort varning `#{warning_num}` från {user}", color=0x2ecc71)
            await ctx.send(embed=embed)





async def setup(bot):
    await bot.add_cog(ModCommands(bot))