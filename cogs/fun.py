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
        
    @commands.command()
    async def dm(self,ctx, userid, *, message):
        print([userid,message])
        user = self.bot.get_user(userid)
        user2 = int(userid)
        user2 = self.bot.get_user(user2)
        print(user)
        #await ctx.send('<@577668867380477962>')
        #await user.send(message)
        await user2.send(message)


def setup(bot):
    bot.add_cog(Extra(bot))
