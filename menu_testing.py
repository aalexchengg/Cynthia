from discord.ext import menus
import discord
import discord
import asyncio
import aiohttp
import json

'''Thesaurus Helper Classes and Methods'''
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

'''Manga description and covers helper methods'''
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


'''Reading Manga helper methods and classes'''
class ChapterSource(menus.ListPageSource):
    def __init__(self, data):
        print(data)
        self.title = data['data']['title']
        self.id = data['data']['id']
        self.chapter = data['data']['chapter']
        self.hash = data['data']['hash']
        self.server = data['server'].replace("\\", "")
        self.pages = data['data']['pages']
        super().__init__(self.pages, per_page = 1)

    async def format_page(self, menu, entries):
        embed = discord.Embed(title = self.title, url = "https://mangadex.org/chapter/{}/{}".format(self.id, menu.current_page), description = "Chapter {}".format(self.chapter))
        embed.set_image(url = "{}{}/{}".format(self.server, self.hash, entries))
        embed.set_footer(text = "Page {}/{}".format(menu.current_page, len(self.pages)))
        return embed


class MangaReadSource():
    '''The master source that holds the references to all the chapters upon request, it outputs a Chaptersource'''
    def __init__(self, source):
        self.source = source
        self.session = aiohttp.ClientSession()
        self.current_chapter = 0
        self.chapter_index = 0

    async def get_chapter_source(self, arg):
        #now get the chapter using its index
        self.current_chapter = self.source[arg]
        self.chapter_index = arg
        async with self.session.get("https://api.mangadex.org/v2/chapter/{}".format(self.current_chapter[0])) as response:
            source = response.read()
        pages = json.loads(source)
        return ChapterSource(pages)

    async def get_max_chapters(self):
        return len(self.source)

    async def get_current_index(self):
        return self.chapter_index
    
    async def get_current_chapter(self):
        return self.current_chapter

class MangaMenu(menus.MenuPages):
    def __init__(self, mastersource, chapter_source, init_chapter):
        self.mastersource = mastersource
        self.source = chapter_source
        super().__init__(self.source, clear_reactions_after = True)

    async def change_checked_source(self, index):
        max_chapters = self.mastersource.get_max_chapters
        try:
            if max_chapters is None:
                await self.change_source(index)
            elif max_chapters > index >= 0:
                await self.change_source(index)
        except IndexError:
            pass

    async def change_source(self, index):
        await super().change_source(self.mastersource.get_chapter_source(index))
    
    def _skip_double_triangle_buttons(self):
        max_pages = self.source.get_max_pages()
        if max_pages is None:
            return True
        return max_pages <= 2
    
    @menus.button('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f',
            position=menus.First(0), skip_if=_skip_double_triangle_buttons)
    async def go_to_previous_chapter(self, payload):
        """go to the first page"""
        await self.change_checked_source(self.mastersource.get_current_index()-1)

    @menus.button('\N{BLACK LEFT-POINTING TRIANGLE}\ufe0f', position=menus.First(1))
    async def go_to_previous_page(self, payload):
        """go to the previous page"""
        await self.show_checked_page(self.current_page - 1)

    @menus.button('\N{BLACK RIGHT-POINTING TRIANGLE}\ufe0f', position=menus.Last(0))
    async def go_to_next_page(self, payload):
        """go to the next page"""
        await self.show_checked_page(self.current_page + 1)

    @menus.button('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f',
            position=menus.Last(1), skip_if=_skip_double_triangle_buttons)
    async def go_to_last_page(self, payload):
        """go to the last page"""
        # The call here is safe because it's guarded by skip_if
        await self.mastersource.change_checked_source(self.mastersource.get_current_index()-1)

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f', position=menus.Last(2))
    async def stop_pages(self, payload):
        """stops the pagination session."""
        self.stop()



class TemporaryMenu(menus.MenuPages):
    def __init__(self, source, **kwargs):
        super().__init__(source, **kwargs)
    async def start(self, ctx, *, channel=None, wait=False):
        await super().start(ctx, channel = channel, wait = wait)
        await asyncio.sleep(120)
        try:
            await super().stop()
        except:
            pass
    
class Test:
    def __init__(self, key, value):
        self.key = key
        self.value = value
