#based.py
# i promise im actually trying to be organized and not a complete mess i promise
import discord,time,random
from discord.ext import commands
from discord import Member
import sys, os.path
sys.path.append(os.path.abspath('../'))
from bot import firebase, FIREBASE_NAME

class Based(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('exec.py is active')
        
    @commands.Cog.listener()
    async def on_message(self, message):
        #TODO: ADD A MIRROR IMAGE, AND PUT THE USERNAME AND DISCRIMINATOR ON IT
        if "mirror mirror on the wall, who is the upvotedest of them all" in message.content.lower():
            basedCount = firebase.get('/' + FIREBASE_NAME + '/upvotecount/', '')
            basedest = 0
            basedestp = ""
            for based_users in basedCount.items():
                #await message.channel.send(based_users)
                user, count = based_users
                thePerson = self.bot.get_user(int(user))
                if thePerson in message.guild.members:
                    if count > basedest:
                        basedest = count
                        basedestp = thePerson
                        #await message.channel.send(f"{basedest}, {basedestp}")
            await message.reply(f"well of course, ***{basedestp.mention}*** is the most upvoted of them all!")
            return
        
        if "mirror mirror on the wall, who is the basedest of them all" in message.content.lower():
            basedCount = firebase.get('/' + FIREBASE_NAME + '/basedcount/', '')
            basedest = 0
            basedestp = ""
            for based_users in basedCount.items():
                #await message.channel.send(based_users)
                user, count = based_users
                thePerson = self.bot.get_user(int(user))
                if thePerson in message.guild.members:
                    if count > basedest:
                        basedest = count
                        basedestp = thePerson
                        #await message.channel.send(f"{basedest}, {basedestp}")
            await message.reply(f"well of course, ***{basedestp.mention}*** is the most based of them all!")
            retribution = firebase.get('/' + FIREBASE_NAME + '/basedcount/' + str(message.author.id), '')
            retribution = int(retribution) - 1
            basedStartCount = firebase.put('/' + FIREBASE_NAME + '/basedcount', str(message.author.id), retribution)
            return
        
    # ------------- Leaderboard -----------------------------
        
    @commands.command(name='based')
    async def based(self,ctx, server_track="no id"):
        if server_track == "no id":
            server_track = ctx.guild
        else:
            server_track = self.bot.get_guild(int(server_track))
        id_ = ctx.author.id
        basedCount = firebase.get('/' + FIREBASE_NAME + '/basedcount/', '')
        based_leader = []
        countss = []
        for based_users in basedCount.items():
            #await ctx.send(based_users)
            user, count = based_users
            thePerson = self.bot.get_user(int(user))
            if thePerson in server_track.members:
                lname = str(thePerson.name) + '#' + str(thePerson.discriminator) + ':' + str(count) + '\n'
                based_leader.append([count, lname])
        based_leader = sorted(based_leader)
        based_leader = based_leader[::-1]
        leaderboard = "```"
        for i in based_leader:
            leaderboard += i[1]
        await ctx.send(leaderboard + '```')

    @commands.command(name='upvote')
    async def upvote(self, ctx, server_track="no id"):
        if server_track == "no id":
            server_track = ctx.guild
        else:
            server_track = self.bot.get_guild(int(server_track))
        id_ = ctx.author.id
        basedCount = firebase.get('/' + FIREBASE_NAME + '/upvotecount/', '')
        based_leader = []
        countss = []
        for based_users in basedCount.items():
            #await ctx.send(based_users)
            user, count = based_users
            thePerson = self.bot.get_user(int(user))
            if thePerson in server_track.members:
                lname = str(thePerson.name) + '#' + str(thePerson.discriminator) + ':' + str(count) + '\n'
                based_leader.append([count, lname])
        based_leader = sorted(based_leader)
        based_leader = based_leader[::-1]
        leaderboard = "```"
        for i in based_leader:
            leaderboard += i[1]
        await ctx.send(leaderboard + '```')
        
        
    # ------------ Trades and Bartering ----------------------
    
    @commands.command(name="giveu")
    async def giveu(self, ctx, recip: discord.Member, amount):
        amount = int(amount)
        if amount < 0:
            await ctx.send("Sorry, you can't give negative upvotes???")
            return
        ctx_id = ctx.author.id
        r_id = recip.id
        upCountCTX = int(firebase.get('/' + FIREBASE_NAME + '/upvotecount/' + str(ctx_id), ''))
        upCountR = int(firebase.get('/' + FIREBASE_NAME + '/upvotecount/' + str(r_id), ''))
        if upCountCTX < amount:
            await ctx.send(f"You don't have enough upvotes. Lmao poor loser")
            return
        upCountCTX -= amount
        upCountR += amount
        UpUpdateCountCTX = firebase.put('/' + FIREBASE_NAME + '/upvotecount', str(ctx_id), upCountCTX)
        UpUpdateCountR = firebase.put('/' + FIREBASE_NAME + '/upvotecount', str(r_id), upCountR)
        
        await ctx.send(f"Transferred {amount} upvotes into {recip.mention}'s balance")
        
    @commands.command(name="giveb")
    async def giveb(self, ctx, recip: discord.Member, amount):
        amount = int(amount)
        if amount < 0:
            await ctx.send("Sorry, you can't give negative baseds???")
            return
        ctx_id = ctx.author.id
        r_id = recip.id
        upCountCTX = int(firebase.get('/' + FIREBASE_NAME + '/basedcount/' + str(ctx_id), ''))
        upCountR = int(firebase.get('/' + FIREBASE_NAME + '/basedcount/' + str(r_id), ''))
        if upCountCTX < amount:
            await ctx.send(f"You don't have enough baseds. Lmao poor loser")
            return
        upCountCTX -= amount
        upCountR += amount
        UpUpdateCountCTX = firebase.put('/' + FIREBASE_NAME + '/basedcount', str(ctx_id), upCountCTX)
        UpUpdateCountR = firebase.put('/' + FIREBASE_NAME + '/basedcount', str(r_id), upCountR)
        
        await ctx.send(f"Transferred {amount} baseds into {recip.mention}'s balance")


def setup(bot):
    bot.add_cog(Based(bot))
