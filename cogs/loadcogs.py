# loadcogs.py
import discord, random, os
from discord.ext import commands


class LoadCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('loadcogs.py is active')

    @commands.Cog.listener()
    async def load(self, ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.load_extension(f'cogs.{filename[:-3]}')

    @commands.Cog.listener()
    async def unload(self, ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.unload_extension(f'cogs.{filename[:-3]}')

    @commands.Cog.listener()
    async def reload(self,ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.unload_extension(f'cogs.{filename[:-3]}')
                self.bot.load_extension(f'cogs.{filename[:-3]}')


def setup(bot):
    bot.add_cog(LoadCogs(bot))
