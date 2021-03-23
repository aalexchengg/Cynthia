# remindmebot.py

import os
import discord
import logging
import menu_testing
import asyncpg
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
POSTGRES = os.getenv('POSTGRES_PASSWORD')
DATABASE = os.getenv('DATABASE_NAME')
intents = discord.Intents.all()
intents.members = True
#intents.presence = True
credentials = {'user': 'postgres', 'password': POSTGRES, 'database': DATABASE, 'host': '127.0.0.1'}
cogs = ['info', 'homework', 'manga', 'fun']

bot = commands.Bot(command_prefix="*", help_command=None,intents = intents, activity=discord.Activity(type= discord.ActivityType.playing, name = "with ur mom"))
bot.connection = await asyncpg.connect(**credentials)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

emojidict = {
    "paimon": "<:paimon:813847764353679361>", 
    "ruka": "<:ruka:813852212752023564>", 
    "baka": "<:baka2:817526241665876008>",
    "falco": '<:yaeger:817525678689353760>', 
    'susandrew': '<:susandrew:817525680258285568>'}



@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == 'megu':
        await message.add_reaction("👍")
        await message.channel.send(file=discord.File("gifs/megumin.gif"))
    elif 'obama' in message.content.lower():
        embed = discord.Embed(title = "You have summoned", description = "", color = 0x3b3b6d)
        embed.set_image(url="https://i.ytimg.com/vi/hPGFpaQb360/maxresdefault.jpg")
        await message.channel.send(embed = embed)
    elif 'biden' in message.content.lower():
        embed = discord.Embed(title = "You have summoned", description = "", color = 0x3b3b6d)
        embed.set_image(url = "https://i.pinimg.com/280x280_RS/4f/14/d2/4f14d20f0d8b1fb78e4ff2417d5a05ee.jpg")
        await message.channel.send(embed = embed)
    elif message.content.lower() in emojidict:
        await message.channel.send(emojidict[message.content.lower()])
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send("Command not found || Use *help to see the list of commands!")
        return
    
    if isinstance(error, commands.UserInputError):
        await ctx.channel.send("Invalid input.")
        return
    
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send("This command is on cooldown! Please try again in {:.2f} seconds".format(error.retry_after))
        return
    
    if isinstance(error, commands.DisabledCommand):
        await ctx.channel.send("This command has been disabled.")
        return
    
    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        await ctx.send(_message)
        return
    
    #print("Ignoring Exception in command {}:".format(ctx.command), file = "discord.log")
    else:
        raise error
    
    
    
for cog in cogs:
    bot.load_extension("cogs.{}".format(cog))
bot.run(TOKEN)
