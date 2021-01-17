# fun.py
import discord, random, asyncio
from discord.ext import commands

emojis = ["😎", "😍", "😂", "🥶", "😱", "😳", "🤢", "🥱", "🤐", "🤯", "🤠", "💀", "🤏", "👀", "🌵", "⚡️", "💦", "🎉",
          "🥳", "😈", "🤡", "✅", "❌", "🤔", "🙄", "🥺", "🤧", "🆗", "💰", "🥰", "😜", "💪", "🤙", "👑", "✈️", "🇺🇸",
          "⛓", "🔪","😕","👺","🐸","💅","🤦‍♀️","💆‍♀️","🧏‍♀️","💁‍♀️","🤒","🤮","🤥","🤤","😬","😰","🤭","🤫","😓","🥺"]

# testing file lol

class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('fun.py is active')

    @commands.Cog.listener()
    async def on_message(self, message):
        if random.randint(0, 100) > 97 and 'https://' not in message.content:
            await message.add_reaction(random.choice(emojis))

    # ----------------------------------------------------
    @commands.command()
    async def stank(self,ctx):
        await ctx.channel.send('lmao imagine not having a !stank command')
        
    """    
    @commands.command()
    async def dm(self,ctx, userid, *, message):
        await self.bot.wait_until_ready()
        userid = int(userid)
        print([userid,message])
        user = self.bot.get_user(userid)
        await ctx.send(f'<@{userid}>')
        await user.send(message)
    """

def setup(bot):
    bot.add_cog(Extra(bot))
