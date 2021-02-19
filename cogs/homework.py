#mathematical commands
import sys
import os
import asyncio
import aiohttp
import discord
import datetime
import json
from discord.ext import commands
from discord.ext import menus
import menu_testing
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
                where each item is a list where the first item is the number, 
                 and second is a dict with key being the definition and value being a list of synonyms'''
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