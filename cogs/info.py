#informational commands
import sys
import asyncio
import aiofiles
import discord
import os
import datetime
from helpers import menu_testing 
from discord.ext import commands
from discord.ext import menus



class Information(commands.Cog):
    """Meta functions that give information about different configurations"""
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def print(self, ctx, *args):
        response = ''
        for arg in args:
            response = response + " " + arg
        await ctx.channel.send(response)

    @commands.command()
    #commands.has_permissions(add_reactions=True,embed_links=True)
    async def help(self,ctx,*cog):
        """Gets all cogs and commands of mine."""
        try:
            if not cog:
                halp=discord.Embed(title='Cog Listing and Uncatergorized Commands',
                               description='Use `!help *cog*` to find out more about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)')
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                #halp.add_field(name='Uncatergorized Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('',embed=halp)
            else:
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
                    await ctx.message.author.send('',embed=halp)
                else:
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=False)
                                found = True
                    if not found:
                        halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
                    else:
                        await ctx.message.add_reaction(emoji='✉')
                    await ctx.message.author.send('',embed=halp)
        except:
            pass

    
    @commands.command()
    async def ping(self, ctx):
        """Returns the latency"""
        ping = ctx.message
        pong = await ctx.send('**:ping_pong:** Pong!')
        delta = pong.created_at - ping.created_at
        delta = int(delta.total_seconds() * 1000)
        await pong.edit(content=f':ping_pong: Pong! ({delta} ms)')
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def hello(self, ctx):
        """Provides information on the status of the bot"""
        tit = "Hey there! I'm RemindMe Bot"
        descrip = "I'm currently in development, and my creator doesnt know anything in python and is furiously googling things on github and stack overflow."
        embed = discord.Embed(title=tit, description = descrip, color=0xa6d609)
        embed.add_field(name="Reach out if there are issues!", value="Find me at rcklss#7412", inline = False)
        embed.set_image(url="https://ih1.redbubble.net/image.1697189330.6868/st,small,845x845-pad,1000x1000,f8f8f8.jpg")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def set_alarm(self, ctx, interval):
        """Sets an alarm after a given time"""
        x = interval.split(":")
        time = int(x[0])*3600 + int(x[1])*60
        #await ctx.channel.send(interval)
        #await ctx.channel.send(x[0] + x[1])
        await ctx.channel.send("Setting a timer up for {} seconds".format(time))
        await asyncio.sleep(time)
        await ctx.channel.send("Your alarm is up!" +ctx.message.author.mention)
    
    @commands.command()
    async def poll(self, ctx, *, arg):
        args = arg.split(',')[:6]
        question = args.pop(0)
        descrip = ""
        buttonlist = []
        buttonpool = [['A', '\U0001f1e6'], ['B', '\U0001f1e7'], ['C', '\U0001f1e8'], ['D', '\U0001f1e9'], ['E', '\U0001f1ea']]
        for i in range(len(args)):
            descrip = descrip + "{}. {}\n".format(buttonpool[i][0], args[i])
            buttonlist.append(buttonpool[i][1])
        embed = discord.Embed(title = "{}'s Poll".format(ctx.author.nick), description = question)
        embed.add_field(name = "Options", value = descrip, inline = True)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        message = await ctx.send(embed = embed)
        for button in buttonlist:
            await message.add_reaction(button)


    
    @commands.command()
    async def serverinfo(self, ctx):
        """Provides information about the guild"""
        h = ctx.guild
        embed = discord.Embed(title = h.name, description = 'ID: ' + str(h.id) + "\nOwner ID: " + str(h.owner.id), color= 0xa6d609)
        embed.add_field(name="Region", value = h.region, inline = True)
        embed.add_field(name = "Owner:", value = h.owner.nick, inline = False)
        embed.add_field(name = "Number of text channels", value = str(len(h.text_channels)), inline = False)
        embed.add_field(name = "Members", value = str(len(h.members)), inline = True)
        embed.add_field(name = "Roles", value = str(len(h.roles)), inline = False)
        embed.set_thumbnail(url=h.icon_url)
        await ctx.send(embed = embed)
    
    @commands.command()
    async def serverinvite(self, ctx):
        """Creates an invite link for the server"""
        invitelink = await ctx.channel.create_invite(max_uses=1, unique=True)
        await ctx.channel.send(invitelink)
    
    @commands.command()
    async def botinvite(self, ctx):
        """Creates an invite link for the bot"""
        embed = discord.Embed(title = "Invite me", url = "http://www.tinyurl.com/3494yhdp", colour= 0xa6d609)
        embed.set_thumbnail(url = "https://i.pinimg.com/originals/a4/0f/00/a40f00befb8c2947b26146e834a8a9f8.jpg")
        await ctx.channel.send(embed = embed)
    
    @commands.command()
    async def fun_with_embeds(self, ctx):
        embed = discord.Embed(title = "*title with asteriks*", description = "*description*")
        embed.add_field(name = "this is the first name", value = "this is the first embed", inline = False)
        embed.add_field(name = "this is the second name", value = " `{}` ".format("this is the second embed"), inline = False)
        embed.add_field(name = "this is the third name", value = "<this is the third embed>", inline = True)
        embed.add_field(name = "this is the fourth name", value = "//this is the fourth embed//", inline = True)
        await ctx.channel.send(embed = embed)
    
    @commands.command()
    async def feedback(self, ctx, *, arg):
        async with aiofiles.open('feedback.txt', 'w') as file:
            await file.write('{}: {}'.format(ctx.author.id, arg))



def setup(bot):
    bot.add_cog(Information(bot))