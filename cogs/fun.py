import discord
import random
import asyncio
from discord.ext import commands, tasks



class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def muteroulette(self, ctx):
        if random.randint(1,6)==3:
            await ctx.message.author.edit(mute = True)
            await ctx.send("Unlucky! You have been muted for a minute.")
            await asyncio.sleep(60)
            await ctx.message.author.edit(mute = False)
        else:
            await ctx.send("You got away this time!")


def setup(bot):
    bot.add_cog(Fun(bot))
    
    