#exec.py
import discord,time,random
from discord.ext import commands
from discord import Member


class Exec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('exec.py is active')

    async def mute(self, ctx, user, reason):
        role = discord.utils.get(ctx.guild.roles, name="Muted")  # retrieves muted role returns none if there isn't
        if not role:  # checks if there is muted role
            try:  # creates muted role
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels:  # removes permission to view and send in the channels
                    await channel.set_permissions(muted, send_messages=False,read_message_history=False,read_messages=False)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role") # self-explainatory
            await user.add_roles(muted) # adds newly created muted role




    @commands.command()
    async def kick(self, ctx, member: Member, *, reason=None):
        await self.bot.wait_until_ready()
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for: {reason}')

    @commands.command()
    async def ban(self, ctx, member: Member, *, reason=None):
        await self.bot.wait_until_ready()
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for: {reason}')

    @commands.command()
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

    @commands.command()
    async def mute(self, ctx, *, member):
        await self.mute(ctx, member)

    @commands.command()
    async def unmute(self, ctx, member):
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted") # removes muted role
        await ctx.send(f"{member.mention} has been unmuted")
        return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument')
            return
        elif isinstance(error, commands.CommandNotFound):
            await ctx.add_reaction("😳")
            await ctx.send('404 Command Not Found')
        else:
            await ctx.send(f'{error} error occured')




def setup(bot):
    bot.add_cog(Exec(bot))
