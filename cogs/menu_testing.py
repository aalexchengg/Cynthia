from discord.ext import commands
from dpymenus import Page, PaginatedMenu


class Menu_Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def demo(self, ctx: commands.Context):
        page1 = Page(title='Page 1', description='First page test!')
        page1.add_field(name='Example A', value='Example B')

        page2 = Page(title='Page 2', description='Second page test!')
        page2.add_field(name='Example C', value='Example D')

        page3 = Page(title='Page 3', description='Third page test!')
        page3.add_field(name='Example E', value='Example F')

        menu = PaginatedMenu(ctx)
        menu.add_pages([page1, page2, page3])
        await menu.open()


def setup(bot):
    bot.add_cog(Menu_Testing(bot))