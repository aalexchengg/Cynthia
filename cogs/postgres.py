import discord
import asyncpg
from discord.ext import commands

class Postgres(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def create_user(self, id):
        async with self.bot.pool.acquire() as connection:
            await connection.execute('INSERT INTO users (id, badjokecounter) VALUES ($1, 0)',id)
        #await bot.connection.execute('')
    
    async def update_user(self, id, badjokeincrement = 0, datingprogress = None):
        async with self.bot.pool.acquire() as con:
            async with con.transaction():
                test = await con.cursor(
                    'SELECT * FROM users WHERE id=$1',id)
                

    async def get_user_by_id(self, id):
        pass

    async def get_users_by_category(self, category):
        pass
    





def setup(bot):
    bot.add_cog(Postgres(bot))