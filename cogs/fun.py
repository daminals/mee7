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
        if random.randint(0, 100) > 97 and not ('https://' in message.content or len(message.attachments) > 0):
            await message.add_reaction(random.choice(emojis))

    # ----------------------------------------------------
    @commands.command()
    async def stank(self,ctx):
        await ctx.channel.send('lmao imagine not having a !stank command')
        
    @commands.command()
    async def dm(self,ctx, userid, *, message):    
        me = self.bot.get_user(577668867380477962)
        if ctx.author == me:
            userid = int(userid)
            user = self.bot.get_user(userid)
            await user.send(message)

def setup(bot):
    bot.add_cog(Extra(bot))
