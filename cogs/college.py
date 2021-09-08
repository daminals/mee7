# college.py
import discord, random, asyncio
from discord.ext import commands
from discord import Member

import colorama
from colorama import Fore
from colorama import Style


class College(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.WHITE + Style.BRIGHT + 'college.py is active' + Style.RESET_ALL)

    @commands.command(name='ethos')
    async def ethos(self, ctx):
        await ctx.add_reaction("✅")
        ans = "the author's character, manifested by his intelligence, confidence, trustworthiness, knowledge of the subject, and respect for the reader"
        for i in range(3):
            def check(m):
                return ctx.author == m.author #To make sure it is the only message author is getting
            msg = await self.bot.wait_for('message', timeout=90.0, check=check)
            if msg.content == ans:
                await msg.add_reaction("✅")
                await msg.reply("Correct✅")
                await msg.delete()
                return
            else:
                await msg.reply("Incorrect. Try again")
                print(ans)
                
 
    @commands.command(name='pathos')
    async def pathos(self, ctx):
        await ctx.add_reaction("✅")
        ans = "evoking of emotions in the reader and not irritating the reader with poor punctuation or grammar; it can include emotional responses the author may not have expected"
        for i in range(3):
            def check(m):
                return ctx.author == m.author #To make sure it is the only message author is getting
            msg = await self.bot.wait_for('message', timeout=90.0, check=check)
            if msg.content == ans:
                await msg.add_reaction("✅")
                await msg.reply("Correct✅")
                await msg.delete()
                return
            else:
                await msg.reply("Incorrect. Try again")
                print(ans)



    @commands.command(name='logos')
    async def logos(self, ctx):
        await ctx.add_reaction("✅")
        ans = "reasoning, that can include examples, facts, statistics, syllogisms, or statements from authoritative figures to draw conclusions"
        for i in range(3):
            def check(m):
                return ctx.author == m.author #To make sure it is the only message author is getting
            msg = await self.bot.wait_for('message', timeout=90.0, check=check)
            if msg.content == ans:
                await msg.add_reaction("✅")
                await msg.reply("Correct✅")
                await msg.delete()
                return
            else:
                await msg.reply("Incorrect. Try again")
                print(ans)
           

def setup(bot):
    bot.add_cog(College(bot))
