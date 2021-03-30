import discord
import random
import asyncio
#import postgres
from discord.ext import commands, tasks

roster = {
            "astra": "<:astra:824807342754365480>",
            "brim": "<:brim:824807345024401408>",
            "breach": "<:breach:824807344475078738>",
            "cypher": "<:cypher:824807344990584843>",
            "jett": "<:jett:824807345157963807>",
            "killjoy": "<:killjoy:824807345150230598>",
            "omen": "<:omen:824807344835133501>",
            "phoenix" : "<:phoenix:824807345246699552>",
            "raze": "<:raze:824807345262821396>",
            "reyna" : "<:reyna:824807344714154055>",
            "sage" : "<:sage:824807344898179123>",
            "skye": "<:skye:824807345326391366>",
            "sova": "<:sova:824807345318002708>",
            "viper": "<:viper:824807345069490207>",
            "yoru" : "<:yoru:824807345250762782>"}
lock = {}

class Fun(commands.Cog):
    """Some fun commands to try out!"""


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def profile(self, ctx):
        await self.bot.get_cog("Postgres").create_user(ctx.author.id)
    
    @commands.command()
    async def badjoke(self, ctx, member: discord.Member=None):
        #get the user from postgres based on their user id
        #if they break the threshold with this bad joke, automatically call mute roulette and reset counter to 0
        #else, add one to their badjoke counter
        pass

    
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
    async def valorant(self, ctx, stack = 5):
        if stack > 5 or stack < 1: stack = 5
       
        map_choice = random.choice(['Ascent', 'Bind', 'Haven', 'Icebox', 'Split'])
        lineup = random.sample(list(roster), stack)
        agents = ""
        for agent in lineup:
            agents = agents + roster[agent]
        await ctx.send('Your Random {} Stack'.format(stack))
        await ctx.send(agents)
        await ctx.send("Your Randomly Chosen Map: {}".format(map_choice))
    
    @commands.command()
    async def lock(self, ctx, *args):
        try:
            for arg in args:
                lock[arg] = roster.pop(arg)
                await ctx.send("Agent {} locked.".format(arg.capitalize()))
        except:
            await ctx.send("Could not find this agent!")
    
    @commands.command()
    async def unlock(self, ctx, *args):
        try:
            for arg in args:
                roster[arg] = lock.pop(arg)
                await ctx.send("Agent {} unlocked.".format(arg.capitalize()))
        except:
            await ctx.send("Could not find this agent!")
    
    @commands.command()
    async def unlockall(self, ctx):
        if(len(lock)>0):
            for item in lock:
                roster[item] = lock.pop(item)
            await ctx.send("All agents unlocked.")
        else:
            await ctx.send("No agents have been locked.")
    
    @commands.command()
    async def locked(self, ctx):
        if(len(lock)!=0):
            embed = discord.Embed(title = "Locked Agents", description = '\n'.join(agent for agent in lock))
            await ctx.send(embed = embed)
        else:
            await ctx.send("No agents locked.")
    
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
                message = message + random.choice(carti_list) 
                checker = random.randint(1,3)
                threshold = 0
            else:
                threshold = threshold + 1
            message = message + + " " + (''.join(random.choice((str.upper, str.lower))(c) for c in word))
        await ctx.send(message)
        



            


def setup(bot):
    bot.add_cog(Fun(bot))
    
    