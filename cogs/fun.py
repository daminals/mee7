# fun.py
import discord, random
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
        if random.randint(0, 100) > 97:
            print("supposed to be emote just so yk")
            if '<:upvote:776161705960931399>' not in message.reaction:
                await message.add_reaction(random.choice(emojis))

    # ----------------------------------------------------
    @commands.command()
    async def stank(self,ctx):
        await ctx.channel.send('lmao imagine not having a !stank command')


def setup(bot):
    bot.add_cog(Extra(bot))
