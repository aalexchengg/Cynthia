#mathematical commands
import sys
import os
import asyncio
import aiofiles
import aiohttp
import discord
import datetime
import json
import random
from discord.ext import commands
from discord.ext import menus
import menu_testing
import math
from scipy.stats import norm
from dotenv import load_dotenv

load_dotenv()
THESAURUS_KEY = os.getenv('THESAURUS_KEY')
DICTIONARY_KEY = os.getenv('DICTIONARY_KEY')

class Homework(commands.Cog):
    """Commands that come in handy when homework is due at midnight"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    
    #basic commands
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
    async def combo(self, ctx, arg):
        '''Provides the amount of combinations or permutations\nExample: 5c3 or 10p2'''
        if "c" in arg:
            data = arg.split("c")
            if len(data)==2 and data[0].isnumeric and data[1].isnumeric:
                answer = math.comb(int(data[0]), int(data[1]))
                await ctx.send("{} = {}".format(arg, answer))

        elif "p" in arg:
            data = arg.split("p")
            if len(data)==2 and data[0].isnumeric and data[1].isnumeric:
                answer = math.perm(int(data[0]), int(data[1]))
                await ctx.send("{} = {}".format(arg, answer))

        else:
            await ctx.send("We currently only support combinations and permutations.")
    
    @commands.command()
    async def randaplac(self, ctx):
        '''Sends a random AP Language and Composition rhetorical device.'''
        async with aiofiles.open('cogs/aplac.txt', 'r') as aplac:
            i = 1
            rand = random.randrange(1, 108)
            async for aline in aplac:
                if i == rand:
                    line = aline
                i = i+1
        embed = discord.Embed(title = "You got!", description = line)
        await ctx.send(embed = embed)
        


    #scipy stats commands
    
    @commands.command()
    async def cdf(self, ctx, loc, mean=0, standard=1):
        '''Calculates the CDF given x value, mean, and standard deviation. 
        If not given, the default for mean is 0 
        and the default for standard deviation is 1'''
        mean = float(mean)
        standard = float(standard)
        loc = float(loc)
        if mean !=0 and standard !=1:
            z = (loc-mean)/standard
        else: 
            z = loc
        answer = norm.cdf(z)
        await ctx.send("normalcdf({},{},{})  = {}".format(loc, mean, standard, answer))
    
    @commands.command()
    async def invnorm(self, ctx, area, mean = 0, standard = 1):
        '''Calculates the invnorm given an area <1, mean, and standard deviation.
        If not given, the default for mean is 0
        and he default for standard deviation is 1'''
        answer = norm.ppf(q = float(area), loc = float(mean), scale = float(standard))
        await ctx.send("invorm({},{},{}) = {}".format(area, mean, standard, answer))




    #Merriam Webster API commands. Dictionary coming soon?

    @commands.command()
    async def thesaurus(self, ctx, arg):
        '''Finds synonyms, antonyms, and related words to the word given'''

        #accessing the Merriam Webster API using the asyncio session and reading it into a list
        url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + arg + "?key=" + THESAURUS_KEY
        async with self.session.get(url) as response:
                source = await response.read()
        data = json.loads(source)
        #if the list does not even exist, the word does not exist.
        if not data or type(data[0]) is not dict:
            await ctx.send("This word is not in our thesaurus!")
        else:
            url = "https://www.merriam-webster.com/thesaurus/" + arg
            string = ''
            embed = discord.Embed(title = 'Merriam Webster Thesaurus', url = url, description = arg, color = 0xa6d609)
            #getting the basic list of synonyms in the "meta" portion of the json
            for synonym in data[0]['meta']['syns'][0]:
                string = string + synonym + "\n"
            embed.add_field(name = "List of Synonyms", value = string, inline = False)
            embed.set_footer(text = "Powered by Merriam Webster. Press the A for an advanced search.")
            message = await ctx.send(embed = embed)
            await message.add_reaction("🅰️")
            #listen for a reaction within 30 seconds. otherwise timeout.
            def check(reaction, user):
                return user != message.author and str(reaction.emoji) == ("🅰️")
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check = check, timeout = 30.0)
            except asyncio.TimeoutError:
                pass
            else:
                liste = []
                '''takes the merriam webster json and formats it into a list, 
                where each item is a dictionary with the key being the definition
                and the value being the synonyms that correspond to it'''
                for i in data:
                    for j in i['def'] [0]['sseq']:
                        try:
                            key =  j[0][1]['dt'][0][1]
                            value = [item['wd'] for item in j[0][1]['syn_list'][0]]
                            liste.append({key:value})
                        except:
                            pass
                pages = menu_testing.TemporaryMenu(source = menu_testing.ThesaurusSource(liste, arg), clear_reactions_after = True)
                await pages.start(ctx)
                
def setup(bot):
    bot.add_cog(Homework(bot))