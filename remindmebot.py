# remindmebot.py

import os
import discord
import logging
import menu_testing
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
intents.members = True
#intents.presence = True

bot = commands.Bot(command_prefix="*", help_command=None,intents = intents, activity=discord.Activity(type= discord.ActivityType.playing, name = "with ur mom"))
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.command()
async def print(ctx, *args):
    response = ''
    for arg in args:
        response = response + " " + arg
    await ctx.channel.send(response)
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == 'megu':
        await message.add_reaction("👍")
        await message.channel.send(file=discord.File("gifs/megumin.gif"))
    elif 'obama' in message.content:
        embed = discord.Embed(title = "You have summoned", description = "", color = 0x3b3b6d)
        embed.set_image(url="https://i.ytimg.com/vi/hPGFpaQb360/maxresdefault.jpg")
        await message.channel.send(embed = embed)
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
    
    
    



        


bot.load_extension("cogs.info")
bot.load_extension("cogs.homework")
bot.load_extension("cogs.manga")
bot.load_extension("cogs.fun")
bot.run(TOKEN)
