#mathematical commands
import sys
import os
import asyncio
import aiohttp
import discord
import datetime
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
THESAURUS_KEY = os.getenv('THESAURUS_KEY')
DICTIONARY_KEY = os.getenv('DICTIONARY_KEY')

class Homework(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    
    @commands.command()
    async def add(self, ctx, *args):
        '''adds a bunch of integers together\n
           Example: *add 5 2 --> 7'''
        sum = 0
        for arg in args:
            j = arg
            if(j.strip('-').isnumeric()):
                sum = sum + int(arg)
            else:
                await ctx.send("please only send integers!")
        await ctx.send("The sum of these is " + str(sum))
    @commands.command()
    async def thesaurus(self, ctx, arg):
        '''Finds synonyms, antonyms, and related words to the word given'''
        url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + arg + "?key=" + THESAURUS_KEY
        async with self.session.get(url) as response:
                source = await response.read()
        data = json.loads(source)
        if not data:
            await ctx.send("This word does not exist! Please try again.")
        else:
            string = ''
            embed = discord.Embed(title = 'Merriam Webster Thesaurus', description = arg, color = 0xa6d609)
            for synonym in data[0]['meta']['syns'][0]:
                string = string + synonym + "\n"
            embed.add_field(name = "List of Synonyms", value = string, inline = False)
            embed.set_footer(text = "Powered by Merriam Webster.")
            await ctx.send(embed = embed)
        

    
    

def setup(bot):
    bot.add_cog(Homework(bot))