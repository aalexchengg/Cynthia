import discord
from discord.ext import commands
from discord.ext import menus
import aiohttp
import asyncio
import menu_testing
from dotenv import load_dotenv
import os
import json
import pandas as pd

class Manga(commands.Cog):

    def __init__(self, bot):
        load_dotenv()
        MANGADEX_SESSION = os.getenv("MANGADEX_SESSION")
        MANGADEX_REMEMBERME = os.getenv("MANGADEX_REMEMBERME") 
        self.bot = bot
        self.session = aiohttp.ClientSession(cookies = {"mangadex_session": MANGADEX_SESSION, "mangadex_rememberme_token" : MANGADEX_REMEMBERME})
    
    @commands.command()
    async def manga(self, ctx, id):
        async with self.session.get("https://api.mangadex.org/v2/manga/{}/covers".format(id)) as response:
            source = await response.read()
        covers = json.loads(source)
        #create a list of the covers
        cl = []
        for cover in covers['data']:
            cl.append(cover['url'])

        async with self.session.get("https://api.mangadex.org/v2/manga/{}".format(id)) as response:
            source = await response.read()
        descrip = json.loads(source)
        #description list; list of description data
        dd = {
            "id": descrip['data']['id'],
            "Title": descrip['data']['title'], 
            "Author": descrip['data']['author'][0], 
            "Artist": descrip['data']['artist'][0],
            "Description": descrip['data']['description'].split('\r\n')[0],
            "LastChapter" : descrip['data']['lastChapter'],
            "MainCover": descrip['data']['mainCover']}
        pages = menu_testing.TemporaryMenu(source = menu_testing.MangaSource(dd, cl), clear_reactions_after = True)
        await pages.start(ctx)


    @commands.command()
    async def read(self, ctx, id, chapter):
        #gets the master list of all the chapters
        async with self.session.get("https://api.mangadex.org/v2/manga/{}/chapters".format(id)) as response:
            source = await response.read()
        chapters = json.loads(source)['data']['chapters']
        df = pd.DataFrame(chapters)
        df = df[df['language']=='gb']
        final = df.values.tolist()
        id = -1
        id = next(final.index(item) for item in final if item[5]==chapter)
        if id == -1:
            id = 0
            await ctx.send("Chapter is not available. Now redirecting to latest chapter.")
        async with self.session.get("https://api.mangadex.org/v2/chapter/{}".format(final[id][0])) as response:
            chaptersource = await response.read()
        pages = json.loads(chaptersource)  
        menupages = menu_testing.MangaMenu(mastersource = menu_testing.MangaReadSource(final), chapter_source = menu_testing.ChapterSource(pages), init_chapter = chapter)
        await menupages.start(ctx)
        #first find the chapter
        #then load the images into a list
        #send to a menu and then start the menu










def setup(bot):
    bot.add_cog(Manga(bot))