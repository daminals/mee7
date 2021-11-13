#exec.py
import discord,time,random
from discord.ext import commands
from discord import Member

import colorama, ffmpy
from colorama import Fore
from colorama import Style
import asyncio

#TODO: Invite command
#TODO: make unban command actually work

class Exec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.RED + Style.BRIGHT +'exec.py is active' + Style.RESET_ALL)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        await self.bot.wait_until_ready()
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for: {reason}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5, Channel=''):
        await self.bot.wait_until_ready()
        if Channel == '':
            Channel = ctx.channel
        else:
            Channel = self.bot.get_channel(Channel)

        await Channel.purge(limit=amount+1)
        await Channel.send(f'Cleared by {ctx.author.mention}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason=None):
        await self.bot.wait_until_ready()
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for: {reason}')
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def nuke(self, ctx):
        reason = "nuke"
        guild = ctx.guild
        for i in guild.members:
            try:
                await self.ban(self, i, delete_message_days=0)
            except:
                print("failed for " + i.display_name)
            await asyncio.sleep(1.5)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        await self.bot.wait_until_ready()
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument')
            return
        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("😳")
            return
        elif isinstance(error, ffmpy.FFRuntimeError):
            await ctx.message.add_reaction("😳")
            return
        else:
            print(Fore.RED + Style.BRIGHT + f'\n--------------------\n{error} error occurred\n\n\n\n' + Style.RESET_ALL)



def setup(bot):
    bot.add_cog(Exec(bot))
