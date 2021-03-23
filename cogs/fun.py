import discord
import random
import asyncio
from discord.ext import commands, tasks



class Fun(commands.Cog):
    """Some fun commands to try out!"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def muteroulette(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.message.author
        if random.randint(1,6)==3:
            await member.edit(mute = True)
            await ctx.send("❌🔫Unlucky! You have been muted for a minute.")
            await asyncio.sleep(60)
            await member.edit(mute = False)
        else:
            await ctx.send("💨🔫You got away this time!")
    
    @commands.command()
    async def date(self, ctx):
        txt = 'The evening sun was sinking past Enoshima, which floated in Sagami Bay, and Sakuta looked out at the scorched red sky and sea from the windows of the Enoden train. Next to him was a senpai, holding onto the hanging straps like him… Sakurajima Mai, a beautiful woman that couldn’t help but draw eyes in the street and a popular actress that had started as a child.'
        embed = discord.Embed(title = "Bunny Girl Senpai: Dating Simulator", description = "Chapter One")
        embed.add_field(
            name="How fast is evolution?", 
            value=txt + "\n *What do you do?*\nA. Confess to her\nB. Eat her pussy and get a chocolate dessert\nC. Ask to go to the beach",
            inline=True)
        embed.set_image(url="https://static.wikia.nocookie.net/aobuta/images/2/27/LN_Vol_01-2.jpg/revision/latest/scale-to-width-down/960?cb=20181217231656")
        reactions = ['\U0001f1e6', '\U0001f1e7', '\U0001f1e8']
        message = await ctx.send(embed = embed)
        for reaction in reactions:
            await message.add_reaction(reaction)

    @commands.command()
    async def cartify(self, ctx, *args):
        carti_list = [
        '* ! +:)',
        ' :) xo !', 
        '^ 🦋*  !+', 
        '** !++', 
        ':( 💕', 
        '🖤& *', 
        '💔', 
        '..$',
         '+*', 
         'ok !',
         '++**',
         '** -',
         '🦇!!!']
        message = ""
        checker = random.randint(1,3)
        threshold = 1
        for word in args:
            if threshold == checker:
                message = message + random.choice(carti_list) + " " + (''.join(random.choice((str.upper, str.lower))(c) for c in word))
                checker = random.randint(1,3)
                threshold = 1
            else:
                message = message + " " + (''.join(random.choice((str.upper, str.lower))(c) for c in word))
                threshold = threshold + 1
        await ctx.send(message)
        



            


def setup(bot):
    bot.add_cog(Fun(bot))
    
    