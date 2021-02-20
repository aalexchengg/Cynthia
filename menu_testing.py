from discord.ext import menus
import discord
import asyncio

class ThesaurusSource(menus.ListPageSource):
    def __init__(self, data, word):
        self.word = word
        self.data = data
        super().__init__(data, per_page = 1)

    async def format_page(self, menu, entries):

        for k,v in entries.items():
            url = "https://www.merriam-webster.com/thesaurus/" + self.word
            embed = discord.Embed(title = "Merriam Webster Advanced Thesaurus Search: " + self.word, url = url, description = "Definition: " + k, color = 0xa6d609 )
            embed.add_field(name = "List of synonyms", value = '\n'.join(syn for syn in v), inline = True)
            embed.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Merriam-Webster_logo.svg/1200px-Merriam-Webster_logo.svg.png")
            footer = "Powered by Merriam Webster. \tPage " + str(menu.current_page + 1) + "/" + str(len(self.data))
            embed.set_footer(text = footer)
        return embed

class MangaSource(menus.ListPageSource):
    def __init__(self, description, covers):
        self.description = description
        self.covers = covers
        super().__init__(covers, per_page = 1)
    
    async def format_page(self, menu, entries):
        description = "Author: {}\nArtist: {}\n".format(self.description['Author'], self.description['Artist'])
        if self.description['LastChapter'] is None:
            description = description + "Status: Ongoing"
        else:
            description = description + "{} Chapters".format(self.description['LastChapter'])
        embed = discord.Embed(title = self.description['Title'], description = description, url = "https://mangadex.org/title/{}".format(self.description['id']))
        embed.add_field(name = "Synopsis", value = self.description['Description'])
        embed.set_thumbnail(url = self.description['MainCover'])
        embed.set_image(url = entries)
        embed.set_footer(text = "Page {}/{}".format(str(menu.current_page+1), str(len(self.covers))))
        return embed
    

class TemporaryMenu(menus.MenuPages):
    def __init__(self, source, **kwargs):
        super().__init__(source, clear_reactions_after=True)
    async def start(self, ctx, *, channel=None, wait=False):
        await super().start(ctx, channel = channel, wait = wait)
        await asyncio.sleep(60)
        try:
            await super().stop()
        except:
            pass
    